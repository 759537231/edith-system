"""
ledger.py — 账本核心操作层 v2

所有写入必须走这里，禁止直接操作 JSON。

职责：
1. 元→分转换（amount_yuan → amount_fen，整数存储）
2. 报销对管理（支出录入时可指定报销金额，自动生成报销对）
3. 数据审计（收支平衡、报销配平、in_budget 校验）
4. CSV 导出（按月导出）
5. 自我学习（用户纠正 → 写入 correction_rules.json）
"""

import json, os, csv, io
from typing import Optional
from datetime import datetime

LEDGER_PATH   = os.path.expanduser('~/.qclaw/workspace/data/ledger.json')
PAIRS_PATH    = os.path.expanduser('~/.qclaw/workspace/data/reimburse_pairs.json')
RULES_PATH    = os.path.expanduser('~/.qclaw/workspace/data/correction_rules.json')

# ── 路径兼容 ──────────────────────────────────────────────────────
def _ledger_path():
    if os.path.exists(LEDGER_PATH):
        return LEDGER_PATH
    # v1 兼容
    old = os.path.join(os.path.dirname(__file__), '..', 'data', 'ledger.json')
    if os.path.exists(old):
        return old
    return LEDGER_PATH

# ── 金额转换 ─────────────────────────────────────────────────────
def _yuan_to_fen(amount_yuan):
    return int(round(amount_yuan * 100))

def _fen_to_yuan(amount_fen):
    return amount_fen / 100

# ── 辅助 ─────────────────────────────────────────────────────────
def _now():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')

def _new_id():
    return datetime.now().strftime('%Y%m%d%H%M%S')

def _load_ledger():
    with open(_ledger_path()) as f:
        return json.load(f)

def _save_ledger(data):
    with open(_ledger_path(), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _load_pairs():
    if os.path.exists(PAIRS_PATH):
        with open(PAIRS_PATH) as f:
            return json.load(f)
    return {'version': 1, 'pairs': [], 'updated_at': _now()}

def _save_pairs(data):
    data['updated_at'] = _now()
    with open(PAIRS_PATH, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── 预算推断（v2：默认预算内，用户说外才算外）────────────────────
def _infer_in_budget(note: str) -> Optional[bool]:
    """命中则强制 False（报销/代付/公费等），否则 None（走默认）"""
    for kw in ['预算外', '报销进出', '已报销', '代付', '公费']:
        if kw in note:
            return False
    return None

def _load_rules():
    if os.path.exists(RULES_PATH):
        return json.load(open(RULES_PATH))
    return {"rules": {}, "_meta": {"total_corrections": 0}}

def _save_rules(rules):
    rules['_meta']['updated_at'] = _now()
    rules['_meta']['total_corrections'] = len(rules['rules'])
    json.dump(rules, open(RULES_PATH,'w'), ensure_ascii=False, indent=2)

def _record_correction(note: str, in_budget: Optional[bool]):
    """用户纠正时自动记录到 correction_rules.json"""
    if not note or in_budget is None:
        return
    rules = _load_rules()
    known = list(rules['rules']) + ['预算外', '报销', '代付', '公费']
    matched = [kw for kw in known if kw in note]
    if not matched:
        return
    key = max(matched, key=len)
    if rules['rules'].get(key, {}).get('in_budget') != in_budget:
        rules['rules'][key] = {
            'in_budget': in_budget,
            'note_hint': note,
            'corrected_at': _now(),
        }
        _save_rules(rules)
        print(f"[ledger] 🧠 已学习规则: 「{key}」→ in_budget={in_budget}")

# ── type 标准化 ─────────────────────────────────────────────────
def _normalize_type(etype: str) -> str:
    """兼容 v1 '支出'/'收入' → v2 'expense'/'income'"""
    if etype in ('支出', 'expense'):
        return 'expense'
    if etype in ('收入', 'income'):
        return 'income'
    return etype

# ── 核心写入 ─────────────────────────────────────────────────────

def add_entry(
    amount_yuan: float,
    date: str,
    merchant: str,
    etype: str = 'expense',
    category: str = '📦 其他',
    note: str = '',
    in_budget: Optional[bool] = None,
    source: str = 'manual',
    reimburse_pair_id: Optional[str] = None,
    **extra
) -> dict:
    """
    添加一条账目（v2）。

    etype: 'expense' | 'income'（v1 '支出'/'收入' 自动转换）
    in_budget: True=预算内 / False=预算外 / None=非消费（收入类自动 None）
    """
    data = _load_ledger()
    amount_fen = _yuan_to_fen(amount_yuan)
    etype = _normalize_type(etype)

    # 语义推断
    inferred = _infer_in_budget(note)
    learned  = _apply_correction_rules(note)

    if learned is not None:
        final_in_budget = learned.get('in_budget', True)
    elif inferred is not None:
        if in_budget is None:
            final_in_budget = inferred
        else:
            final_in_budget = in_budget
            if inferred != in_budget:
                _record_correction(note, in_budget)
    else:
        final_in_budget = in_budget if in_budget is not None else True

    # 收入类强制 in_budget=None
    if etype == 'income':
        final_in_budget = None

    entry = {
        'id':              _new_id(),
        'date':            date,
        'merchant':        merchant,
        'amount':          amount_fen,
        'type':            etype,
        'category':        category,
        'note':            note,
        'in_budget':       final_in_budget,
        'source':          source,
        'created_at':      _now()[:-9] + datetime.now().strftime('%H:%M:%S.%f')[:-3],
        'reimburse_pair_id': reimburse_pair_id,
        **extra
    }
    data['entries'].append(entry)
    _save_ledger(data)
    return entry

def _apply_correction_rules(note: str) -> Optional[dict]:
    rules = _load_rules()
    for keyword, rule in rules['rules'].items():
        if keyword in note:
            return rule
    return None

def correct_entry(entry_id: str, **updates) -> Optional[dict]:
    """
    纠正条目，同时触发学习。

    用法：
      correct_entry(entry_id, amount_yuan=-66)          # 修正金额
      correct_entry(entry_id, note="xxx", in_budget=False)  # 修正分类
    """
    data = _load_ledger()
    entry = next((e for e in data['entries'] if e.get('id') == entry_id), None)
    if entry is None:
        return None

    # 金额转换支持 yuan
    if 'amount_yuan' in updates:
        updates['amount'] = _yuan_to_fen(updates.pop('amount_yuan'))

    # 触发学习
    note = updates.get('note', entry.get('note', ''))
    in_budget_new = updates.get('in_budget', entry.get('in_budget'))
    if 'in_budget' in updates:
        _record_correction(note, in_budget_new)

    # type 标准化
    if 'etype' in updates:
        updates['type'] = _normalize_type(updates.pop('etype'))

    entry.update(updates)
    _save_ledger(data)
    return entry

# ── 报销对管理（第二天核心）──────────────────────────────────────

def add_expense_with_reimburse(
    amount_yuan: float,
    date: str,
    merchant: str,
    reimburse_amount_yuan: Optional[float] = None,
    etype: str = 'expense',
    category: str = '📦 其他',
    note: str = '',
    source: str = 'manual',
    **extra
) -> dict:
    """
    录入一笔支出，并可选录入报销金额，自动生成报销对。

    用法：
      # 纯自费
      add_expense_with_reimburse(66, '2026-04-13', '巴方酸辣粉')

      # 有报销（全额）
      add_expense_with_reimburse(35.26, '2026-04-12', '赵一鸣', reimburse_amount_yuan=35.26)

      # 有报销（部分，对方四舍五入）
      add_expense_with_reimburse(60.43, '2026-04-11', '京东', reimburse_amount_yuan=60)

    返回 dict 含：
      - expense_entry
      - reimburse_entry（若有）
      - pair（若有）
    """
    data = _load_ledger()
    exp_fen = _yuan_to_fen(amount_yuan)
    etype = _normalize_type(etype)

    # 生成支出条目
    exp_entry = {
        'id':          _new_id(),
        'date':        date,
        'merchant':    merchant,
        'amount':      exp_fen,
        'type':        etype,
        'category':    category,
        'note':        note,
        'in_budget':   False if reimburse_amount_yuan is not None else True,
        'source':      source,
        'created_at':  _now()[:-9] + datetime.now().strftime('%H:%M:%S.%f')[:-3],
        **extra
    }

    result = {'expense_entry': exp_entry, 'reimburse_entry': None, 'pair': None}

    # 有报销金额 → 生成报销对
    if reimburse_amount_yuan is not None:
        reimb_fen = _yuan_to_fen(reimburse_amount_yuan)
        reimb_entry = {
            'id':          _new_id(),
            'date':        date,
            'merchant':    f'报销-{merchant}',
            'amount':      abs(reimb_fen),
            'type':        'income',
            'category':    '💰 报销退款',
            'note':        note,
            'in_budget':   None,
            'source':      'reimburse_pair',
            'created_at':  _now()[:-9] + datetime.now().strftime('%H:%M:%S.%f')[:-3],
            'reimburse_pair_id': None,  # 等 pair 创建后回填
            **extra
        }

        # 计算差额
        out_of_pocket = abs(exp_fen) - abs(reimb_fen)  # 正=自付，负=对方多给
        pair = {
            'id':              f'PAIR-{_new_id()}',
            'category':        merchant,
            'expense_id':      exp_entry['id'],
            'expense_amount':  exp_fen,
            'reimburse_id':    reimb_entry['id'],
            'reimburse_amount':reimb_fen,
            'out_of_pocket':   int(out_of_pocket),
            'status':          '配平' if out_of_pocket == 0 else '有差额',
            'created_at':      _now(),
        }
        exp_entry['reimburse_pair_id'] = pair['id']
        reimb_entry['reimburse_pair_id'] = pair['id']
        result['reimburse_entry'] = reimb_entry
        result['pair'] = pair

        # 更新报销对表
        pd = _load_pairs()
        pd['pairs'].append(pair)
        _save_pairs(pd)

    data['entries'].append(exp_entry)
    if reimb_entry := result.get('reimburse_entry'):
        data['entries'].append(reimb_entry)
    _save_ledger(data)

    return result


def add_reimburse_pair(
    expense_entry_id: str,
    reimburse_entry_id: str,
    category: str = '',
) -> dict | None:
    """
    手动绑定一条报销对（用于补录旧条目）。

    用法：
      add_reimburse_pair('20260410123456', '20260411098765', '逗猫棒')
    """
    data = _load_ledger()
    exp = next((e for e in data['entries'] if e.get('id') == expense_entry_id), None)
    inc = next((e for e in data['entries'] if e.get('id') == reimburse_entry_id), None)
    if not exp or not inc:
        return None

    out_of_pocket = abs(exp['amount']) - abs(inc['amount'])
    pair = {
        'id':               f'PAIR-{_new_id()}',
        'category':         category or exp.get('merchant', ''),
        'expense_id':       exp['id'],
        'expense_amount':   exp['amount'],
        'reimburse_id':     inc['id'],
        'reimburse_amount': inc['amount'],
        'out_of_pocket':    int(out_of_pocket),
        'status':           '配平' if out_of_pocket == 0 else '有差额',
        'created_at':       _now(),
    }
    exp['reimburse_pair_id'] = pair['id']
    inc['reimburse_pair_id'] = pair['id']

    pd = _load_pairs()
    pd['pairs'].append(pair)
    _save_pairs(pd)
    _save_ledger(data)
    return pair

def get_reimburse_pairs() -> list:
    return _load_pairs().get('pairs', [])

def get_pair_status(pair_id: str) -> dict | None:
    pairs = get_reimburse_pairs()
    return next((p for p in pairs if p['id'] == pair_id), None)

# ── 查询 ─────────────────────────────────────────────────────────

def get_entries(
    date_from: str = '',
    date_to: str = '',
    in_budget: bool | None = None,
    type_: str = '',
    keyword: str = '',
    pending: bool | None = None,
    rejected: bool | None = None,
):
    """查询条目，v2 兼容（type='expense'/'income'）"""
    data = _load_ledger()
    results = data['entries']
    if date_from: results = [e for e in results if e.get('date','') >= date_from]
    if date_to:   results = [e for e in results if e.get('date','') <= date_to]
    if in_budget is not None: results = [e for e in results if e.get('in_budget') == in_budget]
    if type_:     results = [e for e in results if e.get('type') == _normalize_type(type_)]
    if keyword:   results = [e for e in results
                              if keyword in e.get('note','') or keyword in e.get('merchant','')]
    if pending is True:    results = [e for e in results if e.get('pending') is True]
    elif pending is False: results = [e for e in results if not e.get('pending')]
    if rejected is True:    results = [e for e in results if e.get('rejected') is True]
    elif rejected is False: results = [e for e in results if not e.get('rejected')]
    return sorted(results, key=lambda e: (e.get('date',''), e.get('created_at','')))

def get_current_month() -> str:
    """返回当前账期 'YYYY-MM'"""
    return datetime.now().strftime('%Y-%m')

def get_summary(month: str | None = None) -> dict:
    """
    汇总，支持指定账期。
    month=None → 当前月
    """
    if month is None:
        month = get_current_month()
    entries = [e for e in get_entries(date_from=f'{month}-01') if not e.get('rejected')]

    expenses = [e for e in entries if e['type'] == 'expense']
    in_b      = [e for e in expenses if e.get('in_budget') is True]
    out_b     = [e for e in expenses if e.get('in_budget') is False]
    incomes   = [e for e in entries if e['type'] == 'income']

    data = _load_ledger()
    budget = data.get('monthly_budget', 100000)
    remaining = budget + sum(e['amount'] for e in in_b)  # 支出是负数

    pairs = get_reimburse_pairs()

    return {
        'month':             month,
        'budget':            budget,
        'budget_yuan':       budget / 100,
        'in_budget_sum':     abs(sum(e['amount'] for e in in_b)),
        'in_budget_count':   len(in_b),
        'out_budget_sum':    abs(sum(e['amount'] for e in out_b)),
        'out_budget_count':  len(out_b),
        'income_sum':        sum(e['amount'] for e in incomes),
        'income_count':      len(incomes),
        'budget_remaining':  remaining,
        'budget_remaining_yuan': remaining / 100,
        'pending_count':     sum(1 for e in entries if e.get('pending')),
        'reimburse_pairs':   len(pairs),
        'unbalanced_count':  sum(1 for p in pairs if p.get('status') != '配平'),
    }

# ── 数据审计 ─────────────────────────────────────────────────────

def audit() -> dict:
    """
    全面审计账本，返回报告。
    """
    data = _load_ledger()
    pairs = _load_pairs().get('pairs', [])
    entries = data['entries']

    issues = []

    # ① 支出必须有明确的 in_budget（True/False，不允许 None）
    for e in entries:
        if e['type'] == 'expense' and e.get('in_budget') is None:
            issues.append({
                'level': '🔴 高',
                'type': 'in_budget_missing',
                'entry_id': e.get('id'),
                'merchant': e.get('merchant'),
                'amount': e.get('amount'),
                'msg': f'支出条目的 in_budget 为 None，需明确指定',
            })

    # ② 报销对状态
    for p in pairs:
        if p.get('status') != '配平':
            oop = p.get('out_of_pocket', 0)
            if oop > 0:
                msg = f'自付 ¥{oop/100:.2f}（支出超额，需确认是否要用户补差）'
            else:
                msg = f'报销超额 ¥{abs(oop)/100:.2f}（对方多付，属用户收入）'
            issues.append({
                'level': '🟡 中',
                'type': 'pair_unbalanced',
                'pair_id': p['id'],
                'category': p.get('category'),
                'msg': msg,
            })

    # ③ 检查孤立报销收入（有 reimburse_pair_id 但不在 pairs 表）
    pair_ids = {p['id'] for p in pairs}
    for e in entries:
        rpid = e.get('reimburse_pair_id')
        if rpid and rpid not in pair_ids:
            issues.append({
                'level': '🔴 高',
                'type': 'orphan_pair_member',
                'entry_id': e.get('id'),
                'merchant': e.get('merchant'),
                'pair_id': rpid,
                'msg': '条目有 reimburse_pair_id 但不在报销对表中',
            })

    # ④ 月度预算校验
    summary = get_summary()
    if summary['budget_remaining'] < 0:
        issues.append({
            'level': '🔴 高',
            'type': 'budget_overflow',
            'msg': f'预算已超支 ¥{abs(summary["budget_remaining_yuan"]):.2f}',
        })

    return {
        'audited_at':    _now(),
        'total_entries': len(entries),
        'total_pairs':   len(pairs),
        'issues':        issues,
        'summary':       summary,
    }

# ── CSV 导出 ─────────────────────────────────────────────────────

def export_csv(month: str | None = None) -> str:
    """
    导出指定月份的 CSV。
    month=None → 当前月
    返回 CSV 字符串。
    """
    if month is None:
        month = get_current_month()
    entries = get_entries(date_from=f'{month}-01', date_to=f'{month}-31', rejected=False)
    pairs = get_reimburse_pairs()
    pair_map = {p['id']: p for p in pairs}

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        '日期', '类型', '商户', '金额(元)', '分类',
        '预算内', '报销对', '自付额(元)', '备注', '来源'
    ])

    for e in entries:
        pid = e.get('reimburse_pair_id', '')
        pair = pair_map.get(pid, {})
        oop = abs(pair.get('out_of_pocket', 0)) if pair else 0
        in_b = {True: '是', False: '否', None: 'N/A'}.get(e.get('in_budget'), '?')
        amt_sign = e['amount'] / 100
        writer.writerow([
            e.get('date', ''),
            e.get('type', ''),
            e.get('merchant', ''),
            f'{amt_sign:.2f}',
            e.get('category', ''),
            in_b,
            pid or '',
            f'{oop/100:.2f}' if oop else '',
            e.get('note', ''),
            e.get('source', ''),
        ])

    return output.getvalue()

def save_csv(month: str | None = None, path: str | None = None):
    """导出 CSV 并保存到文件"""
    csv_str = export_csv(month)
    if path is None:
        month = month or get_current_month()
        path = os.path.join(os.path.dirname(__file__), f'{month}-账本.csv')
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        f.write(csv_str)
    return path

# ── P2 待确认抽屉 ────────────────────────────────────────────────

def add_pending(
    amount_yuan: float, date: str, merchant: str,
    etype: str = 'expense', note: str = '',
    source: str = 'wechat_ocr', ocr_confidence: float = 0.9,
    **extra
) -> dict:
    data = _load_ledger()
    entry = {
        'id':              _new_id(),
        'date':            date,
        'merchant':        merchant,
        'amount':          _yuan_to_fen(amount_yuan),
        'type':            _normalize_type(etype),
        'note':            note,
        'pending':         True,
        'pending_at':      _now(),
        'source':          source,
        'ocr_confidence':  ocr_confidence,
        **extra
    }
    data['entries'].append(entry)
    _save_ledger(data)
    return entry

def confirm_pending(entry_id: str) -> dict | None:
    data = _load_ledger()
    entry = next((e for e in data['entries']
                  if e.get('id') == entry_id and e.get('pending')), None)
    if entry is None:
        return None
    entry['pending'] = False
    entry['confirmed_at'] = _now()
    inferred = _infer_in_budget(entry.get('note', ''))
    learned  = _apply_correction_rules(entry.get('note', ''))
    if learned:
        entry['in_budget'] = learned.get('in_budget', True)
    elif inferred is not None:
        entry['in_budget'] = inferred
    else:
        entry.setdefault('in_budget', True)
    entry.setdefault('category', '📦 其他')
    _save_ledger(data)
    return entry

def reject_pending(entry_id: str) -> dict | None:
    data = _load_ledger()
    entry = next((e for e in data['entries']
                  if e.get('id') == entry_id and e.get('pending')), None)
    if entry is None:
        return None
    entry['pending'] = False
    entry['rejected'] = True
    entry['rejected_at'] = _now()
    _save_ledger(data)
    return entry

def get_pending() -> list:
    return sorted(
        [e for e in _load_ledger()['entries'] if e.get('pending')],
        key=lambda e: e.get('pending_at', '')
    )

# ── CLI 调试入口 ─────────────────────────────────────────────────
if __name__ == '__main__':
    print("📊 账本审计报告")
    r = audit()
    s = r['summary']
    print(f"\n月份: {s['month']}")
    print(f"月度预算: ¥{s['budget_yuan']:.2f}")
    print(f"预算内支出: ¥{s['in_budget_sum']/100:.2f}（{s['in_budget_count']}条）")
    print(f"预算外支出: ¥{s['out_budget_sum']/100:.2f}（{s['out_budget_count']}条）")
    print(f"💰 预算剩余: ¥{s['budget_remaining_yuan']:.2f}")
    print(f"报销对: {s['reimburse_pairs']} 对（{s['unbalanced_count']}对未配平）")

    if r['issues']:
        print(f"\n⚠️ 问题 {len(r['issues'])} 条:")
        for iss in r['issues']:
            print(f"  {iss['level']} [{iss['type']}] {iss['msg']}")
    else:
        print("\n✅ 无问题")

    print("\n🧠 已学规则:")
    rules = _load_rules()
    for k, v in rules.get('rules', {}).items():
        print(f"  「{k}」→ in_budget={v['in_budget']}")
