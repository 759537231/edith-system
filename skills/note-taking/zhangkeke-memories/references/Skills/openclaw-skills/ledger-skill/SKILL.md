---
name: ledger-skill
description: 家庭账本记账系统。支持手动记账、OCR截图识别、自动分类、报销对管理、月度统计、Excel导出。数据存 ~/.qclaw/workspace/data/。
metadata:
  openclaw:
    emoji: "📒"
    trigger_keywords:
      - "记账"
      - "花了"
      - "报销"
      - "查账"
      - "账单"
      - "这个月"
      - "预算"
---

# 📒 Ledger Skill — 家庭账本

## 核心定位

用户（张三）的个人记账系统。每笔支出有「预算内/预算外」区分，预算内从月度 ¥1000 扣除，超出部分单独统计。

**数据文件：**
- `~/.qclaw/workspace/data/ledger.json` — 账本（唯一写入入口）
- `~/.qclaw/workspace/data/reimburse_pairs.json` — 报销对表
- `~/.qclaw/workspace/data/correction_rules.json` — 自我学习规则

## 核心原则

**⚠️ 每次录入前必须先确认日期和时间**

OCR 截图识别时，截图上的时间戳就是唯一正确日期。**不要按收到截图的时间算，要按账单上的时间算。**

- 账单显示 "4月19日" → 日期就是 2026-04-19
- 即使截图是晚上 22:00 收到的，但账单写 "4月18日 13:51" → 日期是 2026-04-18

**录入顺序（强制）：**
1. 读取截图/消息中的**日期和时间**
2. 确认日期后才录入
3. 每笔录入后复述日期+金额，等用户确认

**默认预算内，用户说外才算外。**

---

## 触发场景

| 场景 | 用户说法 | 系统行为 |
|------|----------|----------|
| 手动记账 | "记账 XXX元 XX地方" / "花了62吃肯德基" | `add_entry()` 直接入库 |
| 报销记账 | "花了XX报销YY" / "这个报销了XX" | `add_expense_with_reimburse()` |
| 查账 | "这个月花了多少" / "预算剩多少" | `audit()` + 汇总输出 |
| 截图识别 | 用户发微信账单截图 | OCR识别 → 去重 → 逐条确认 |
| 修正 | "这笔不算预算内" / "金额错了" | `correct_entry()` |
| 导出 | "导出Excel" / "导出账单" | `export_csv()` |

---

## 核心 API

### add_entry(amount_yuan, date, merchant, etype, category, note, in_budget)

**手动记账（最常用）**

```python
import sys
sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/skills/ledger-skill/scripts'))
import ledger

result = ledger.add_entry(
    amount_yuan=-62.00,      # 负数=支出，正数=收入
    date='2026-04-13',
    merchant='肯德基',
    etype='expense',
    category='🍽 餐饮',
    note='',
    in_budget=True           # 预算内（默认）
)
```

**输出示例：**
```
✅ 已入账
  2026-04-13 肯德基 ¥-62.00（预算内）
  💰 预算剩余 ¥127.40
```

### add_expense_with_reimburse(amount_yuan, date, merchant, reimburse_amount_yuan, ...)

**报销场景**：支出时同时录入报销金额，自动生成报销对。

```python
ledger.add_expense_with_reimburse(
    amount_yuan=-75.26,      # 实际总花费
    date='2026-04-12',
    merchant='赵一鸣',
    reimburse_amount_yuan=40.00,   # 对方报销金额
    category='🍽 餐饮',
    note='零食，全额75.26，报销40，净自付35.26'
)
# → 自动生成 PAIR，差额自动计算
```

**报销对三态：**
- 支出=报销金额 → ✅ 配平
- 报销多 → ⚠️ 你赚差价的 ¥X
- 支出多 → ⚠️ 你自付 ¥X

### correct_entry(entry_id, **kwargs)

**修正条目**：金额错了、分类错了、预算内外搞混了。

```python
# 修正金额（amount_yuan 传正数，内部自动转为负数）
ledger.correct_entry('20260412194928', amount_yuan=-75.26)

# 修正分类
ledger.correct_entry('20260412194928', category='🛒 电商')

# 修正预算内外
ledger.correct_entry('20260412194928', in_budget=False)
```

### audit() → get_summary()

**全量审计 + 汇总**

```python
r = ledger.audit()
s = r['summary']
pairs = ledger.get_reimburse_pairs()

# 输出格式：
# 月度预算: ¥1000.00
# 预算内支出: ¥810.60（26条）
# 💰 预算剩余: ¥189.40
# 预算外支出: ¥602.89（7条）
# 报销收入: ¥165.69（6条）
```

### get_reimburse_pairs()

**报销对列表**（5对）

| ID | 商户 | 支出 | 报销 | 状态 |
|----|------|------|------|------|
| PAIR-001 | 逗猫棒 | ¥6.00 | ¥6.00 | ✅ 配平 |
| PAIR-002 | 睡衣 | ¥39.00 | ¥39.00 | ✅ 配平 |
| PAIR-003 | 京东红豆水 | ¥59.90 | ¥60.00 | ⚠️ 你赚 ¥0.10 |
| PAIR-004 | 赵一鸣零食 | ¥75.26 | ¥40.00 | ⚠️ 净自付 ¥35.26 |
| PAIR-005 | 京东¥60.43 | ¥60.43 | ¥60.00 | ⚠️ 自付 ¥0.43 |

### export_csv(month='2026-04')

**按月导出 CSV**

```python
ledger.export_csv(month='2026-04', output_dir=os.path.expanduser('~/Desktop'))
# → ~/Desktop/4月账单_2026-04.csv
```

### export_to_excel(month='2026-04')

**导出带格式 Excel**

```python
import sys
sys.path.insert(0, os.path.expanduser('~/.qclaw/workspace/data'))
import to_excel
to_excel.export_month(month='2026-04', output_dir=os.path.expanduser('~/Desktop'))
```

---

## 自动分类规则

| 商户关键词 | 分类 |
|-----------|------|
| 盒马、山姆、超市、奥乐齐、ALDI | 🍽 餐饮 |
| 肯德基、美团、KFC、麦当劳、火锅 | 🍽 餐饮 |
| 拼多多、淘宝、京东、抖音 | 🛒 电商 |
| 充电、惠迪、停车、加油站 | 🚗 出行 |
| 医院、挂号、诊所 | 🏥 医疗 |
| 退款、报销收入 | 💰 收入 |
| 其他 | 📦 其他 |

---

## 预算规则

**周预算：¥1000.00**（字段 `weekly_budget`，单位：分）

- 周期：每周收到媳妇儿转账时开始新周期（如 5.2-5.8）
- `in_budget=True` → 从预算扣除
- `in_budget=False` → 不进预算（预算外支出）
- `type=income` → 报销退款等真实收入
- 预算拨入用 `type=income`，`note` 标注"媳妇儿转账（周预算 X.X-X.X）"

**预算剩余 = weekly_budget − Σ(本周期内 in_budget=True 的支出)**

**新周期开始时**：手动录入一笔 +1000 收入，in_budget=None，note 注明周期日期范围。

---

## 自我学习规则

用户纠正条目时，自动追加规则到 `correction_rules.json`：

- 用户说「算预算外」→ 该规则自动归类为预算外
- 用户说「不算」某分类 → 规则里记录该商户下次直接分类

---

## 当前状态（2026-05-06 更新）

| 项目 | 金额 |
|------|------|
| 周预算 | ¥1,000.00 |
| 本周周期 | 5月6日 ~ 5月12日 |
| 上周期结余 | ¥230.74 |
| 媳妇儿已转账 | ¥1,000（已记录） |
| 今日已花 | 山姆¥52 + 抖音¥39.9 + 淘宝¥6.4 = ¥98.30 |
| 💰 预算剩余 | ¥901.70 |

---

## 周结转流程（用户说"结束本周"时）

当用户说"结束本周"、"开始新一轮"、"结账"等，执行以下步骤：

1. **确认结束日期**：用户说几号结束就几号结束（不一定是周日）
2. **更新账本周期**：修改 `ledger.json` 的 `week_start`/`week_end`
3. **导出桌面表格**：
   - 文件名：`本周账单_{start}至{end}.xlsx`
   - 路径：`~/Desktop/`
   - 内容：逐笔明细（序号/日期/商户/金额/备注）+ 合计 + 剩余
   - 用 openpyxl 创建，带表头样式（蓝底白字）、边框、列宽
   - **删除旧的表格文件**（如有同名或旧周期文件）
4. **重置新周期**：更新 `week_start` 为新起始日，`week_end` 先设7天后
5. **记录结余**：存入 `last_week_remaining` 字段
6. **等待收入**：告诉用户"等媳妇儿转账了告诉我"

**⚠️ 不要自己决定周期起止，用户说了算。**

**实际案例（2026-05-06）**：
- 用户说"5月5号结束本周，5月6号开始新一轮记账，把账单更新到桌面表格"
- 执行：删除旧文件 `本周账单_2026-05-02至2026-05-08.xlsx`，创建新文件 `本周账单_2026-05-02至2026-05-05.xlsx`
- 更新账本周期为 5.6-5.12
- 用户随后确认"媳妇儿已转1000，不用单独记"→ 记录收入 + 周期开始

**注意**：搜索桌面文件时，working directory 可能是已删除的旧项目目录（如 qimen_app），会导致 search_files 和 terminal 报错。用 `execute_code` + `os.walk` 或 `glob` 绕过。

---

## ⚠️ 坑：飞书文件发送（2026-05-05）

用户问余额，我心算错了，被骂"这啥玩意"。

**铁律：任何金额计算，必须用代码，不能心算。**

正确流程：
```python
import json
with open('/Users/qianmo/.qclaw/workspace/data/ledger.json', 'r') as f:
    data = json.load(f)
# 用代码筛选+求和，输出结果
```

错误流程（会导致出错）：
- 看一眼数字，心算减法
- 在回复里手写 "1000 - 575.98 = 424.02"

---

## ⚠️ 坑：不要手动算余额（2026-05-06）

**用户明确要求：用代码算，不要心算。**

错误做法：心算 "1378.02 - 251 - 193 = 934.02" → 用户说"不对 重新算 让伊迪丝算 这啥玩意这是"

正确做法：读取 ledger.json，用 Python 代码计算本周期预算内支出，输出结果。

```python
# 标准计算流程
import json
with open('~/.qclaw/workspace/data/ledger.json', 'r') as f:
    data = json.load(f)

# 筛选本周期预算内支出
total = 0
for entry in data['entries']:
    if week_start <= entry['date'] <= week_end and entry['type'] == 'expense' and entry.get('in_budget') == True:
        total += abs(entry['amount']) / 100

remaining = data['weekly_budget'] / 100 - total
```

**原则：算账用代码，不要用脑子。**

---

## ⚠️ 坑：Python 版本兼容（已修复 2026-05-04）

`ledger.py` 原本使用 `X | None` 类型注解语法（PEP 604），需要 **Python 3.10+**。macOS 系统自带 Python 3.9.6 会报错。

**症状**：`TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`

**已修复**：所有 `bool | None`、`str | None`、`dict | None`、`float | None` 已替换为 `typing.Optional[X]`，文件头已添加 `from typing import Optional`。共 13 处。

**当前环境**：
- 系统 Python：`/usr/bin/python3` → 3.9.6（不动）
- Homebrew Python：`/opt/homebrew/bin/python3` → 3.14.4（已安装 2026-05-04）

**调用方式**：
```bash
/opt/homebrew/bin/python3 -c "
import sys
sys.path.insert(0, '/Users/qianmo/Desktop/张壳壳/Skills/openclaw-skills/ledger-skill/scripts')
import ledger
# ... 调用 ledger 函数
"
```

**验证**：`/opt/homebrew/bin/python3 -c "import sys; sys.path.insert(0, '...'); import ledger"` 应无报错。

---

## ⚠️ 坑：execute_code部分失败导致重复写入（2026-05-09）

**问题**：execute_code报错退出，但数据已经写入了。第二次执行又写一遍，导致重复条目。

**案例**：
- 第一次execute_code写入7条记录，但在计算余额时报KeyError退出
- 实际上前半段（写入）已执行，7条记录已入库
- 第二次execute_code又写入7条，变成14条
- 用户发现总额翻倍

**正确做法**：
1. 写入和计算分开执行
2. 或者在写入前先检查是否已存在
3. 如果execute_code报错，先检查文件是否已修改，再决定是否重试

**修复方法**：
```python
# 检查是否有重复
duplicates = []
for i, e in enumerate(data['entries']):
    if e.get('date') == date and e.get('merchant') == merchant and abs(e.get('amount', 0)) == abs(amount):
        duplicates.append(i)

# 删除重复（保留第一条，删除后面的）
if len(duplicates) > 1:
    for i in sorted(duplicates[1:], reverse=True):
        del data['entries'][i]
```

## ⚠️ 坑：type字段为空导致不计入预算（2026-05-09）

**问题**：条目的type字段是None而不是"expense"，导致不被计入预算内支出。

**案例**：
- 手动修改in_budget为True后，预算剩余没变化
- 检查发现type=None，不符合`entry.get('type') == 'expense'`条件

**正确做法**：修改条目时，同时确保type和in_budget都正确设置。

```python
# 完整修复
for e in data['entries']:
    if e.get('date') == target_date and e.get('merchant') == target_merchant:
        e['type'] = 'expense'  # 确保type
        e['in_budget'] = True  # 确保预算内
```

## ⚠️ 坑：in_budget字段为空导致不计入预算（2026-05-09）

**问题**：条目的in_budget字段是None而不是True，导致不被计入预算内支出。

**案例**：
- 肯德基30元、美团53.60元的in_budget=None
- 这两条不在预算明细中出现

**正确做法**：所有支出条目必须明确设置in_budget为True或False，不能是None。

## 用户偏好：查账输出格式

用户说"明细"时，要的是**简洁的编号列表**，一行一笔，只写日期、商户、金额，有备注加备注。

**✅ 正确格式（编号列表）**：
```
📅 5月2日 ~ 5月8日  💵 预算 ¥1000

1. 5月3日，肯德基，91.80
2. 5月3日，拼多多，5.10
3. 5月5日，美团，22.00（晚饭）

合计：769.26
剩余：230.74
```

**❌ 用户拒绝的格式**：
- 逐条列出所有字段（日期/商户/金额/分类/备注/来源/ID 太啰嗦）→ 用户说"不是这种 简单的明细"
- Markdown表格（用户觉得不够直观，说"？明细呢"）
- JSON dump

**输出结构**：表头（周期+预算）→ 编号列表（逐笔）→ 底部（合计+剩余）

**原则**：一句话一笔，不要多余的列（分类、来源、ID都不需要），有备注加括号。要简洁有力，不要啰嗦。

---

## ⚠️ 坑：重复条目（2026-05-09）

**问题**：execute_code第一次调用报错，但数据实际已写入。第二次调用又写了一遍，导致7笔变14笔。

**根因**：Python脚本执行过程中，JSON写入在报错之前就完成了。报错发生在后续计算步骤，但写入已经生效。

**检测方法**：
```python
# 记账前检查当天同一商户+相近金额是否已存在
def check_duplicate(data, date, merchant, amount_yuan):
    for e in data['entries']:
        if (e['date'] == date and 
            e['merchant'] == merchant and 
            abs(abs(e['amount'])/100 - abs(amount_yuan)) < 0.01):
            return e
    return None
```

**铁律**：execute_code报错后，先检查JSON是否已写入，再决定是否重试。

## ⚠️ 坑：条目type字段为空（2026-05-09）

**问题**：某些条目的`type`字段是`None`而不是`"expense"`，导致预算计算漏掉这些条目。

**现象**：用户说"还有两次充电没记进去"，实际已记但`type`为空，不参与计算。

**修复**：
```python
# 修复type为空的条目
for e in data['entries']:
    if e.get('type') is None and e.get('amount', 0) < 0:
        e['type'] = 'expense'
```

**预防**：每次写入新条目时，必须显式设置`type`字段，不能依赖默认值。

## 用户偏好：记账要快

用户反馈："为什么记个帐要这么麻烦"——记账必须**一句话搞定**，不能绕弯子。

**⚠️ 不要问多余的问题**

用户说"记账"，直接记。不要问：
- "这笔是预算内还是预算外？"（默认预算内）
- "你是用什么支付的？"（不重要）
- "你确定是这个金额吗？"（用户说了就是）

只有信息明显缺失时才问（比如没说金额、没说日期）。

## ⚠️ 坑：账单明细的格式（2026-05-06）

用户说"我要明细"时，想要的是**简洁列表**，不是逐笔展开的详细字段。

**错误格式**（用户说"？明细呢"表示不满意）：
```
第1笔
  日期：2026-05-03
  商户：肯德基
  金额：¥91.80
  分类：🍽 餐饮
  备注：无
  来源：manual
  ID：20260503110800000001
```

**正确格式**（简洁表格）：
```
| 日期 | 商户 | 金额 |
|------|------|------|
| 05-03 | 肯德基 | 91.80 |
| 05-03 | 拼多多 | 5.10 |
```

**规则**：
- "明细" = 简洁列表（日期|商户|金额）
- "详细明细" = 每笔展开所有字段
- 默认给简洁表格，用户说"详细"才展开

## ⚠️ 坑：计算余额必须用代码（2026-05-06）

用户记账后问余额，我手算出了错（漏了新记的账、加法算错）。用户纠正："不对 重新算 让伊迪丝算 这啥玩意这是"。

**规则：计算余额永远用代码读 ledger.json 算，不要手算。** 哪怕看起来简单，也跑一遍 Python。手算出错比多花 2 秒跑代码严重得多。

**正确流程**：
1. 用户说"记账 X块 XX地方"
2. 直接写入 JSON，不废话
3. 回复"✅ 已入账：日期 商户 ¥金额（预算内/外）💰 预算剩余 ¥XXX"

**错误流程**（用户反感）：
- 先查skill → 读skill内容 → 发现兼容问题 → 修代码 → 才能记账
- 每次都确认一堆细节
- 输出冗长的JSON或技术细节

**原则：简单记账直接改 JSON，不走 ledger.py 的复杂流程。只有复杂场景（报销、修正、审计）才调用完整 API。

## ⚠️ 坑：重复条目检测（2026-05-07）

用户记账"拼多多13.58厕所垫子"，但同一天已有"拼多多13.58地垫"。用户确认是重复的，要求删除。

**规则：记账前检查当天同一商户+相近金额是否已存在。如果存在，先问用户是否重复。**

## ⚠️ 坑：execute_code"假失败"导致重复写入（2026-05-09）

**问题**：execute_code报错（如KeyError），但数据已经写入JSON文件。第二次执行时又写一遍，导致条目翻倍。

**案例**：记账7笔，第一次execute_code报KeyError（代码bug），但前几行的json.dump已经执行。修复bug后重跑，7笔变14笔，预算剩余从603.70变成305.70。

**正确流程**：
```
execute_code报错
  → 不要直接修复后重跑
  → 先读取JSON，检查条目是否已写入
  → 如果已写入，只修复计算逻辑，不重复写入
  → 如果未写入，才重新执行完整流程
```

**自检代码**：
```python
# 执行写入前，先记录当前条目数
before_count = len(data['entries'])
# ... 写入操作 ...
after_count = len(data['entries'])
if after_count > before_count + expected_count:
    print(f"⚠️ 检测到重复写入！期望{expected_count}条，实际增加{after_count - before_count}条")
```

```python
# 记账前检查重复
def check_duplicate(data, date, merchant, amount_yuan):
    for e in data['entries']:
        if (e['date'] == date and 
            e['merchant'] == merchant and 
            abs(abs(e['amount'])/100 - abs(amount_yuan)) < 0.01):
            return e
    return None
```

## ⚠️ 坑：用户说"不用单独记"也要记（2026-05-07）

用户说"媳妇儿转了1000，不用单独记了"——意思是不用问细节，但**收入还是要记录到ledger.json**。不记的话预算计算会出错。

**规则：用户说"不用记"的收入 = 不用问，直接记。**

## ⚠️ 坑：日期错误修正（2026-05-05）

用户发现账本中有 5月6日和 5月7日的记录，但今天才是 5月5日。这是因为我错误地使用了未来的日期。

**规则：记账时必须检查日期，确保不超过当前日期。**

**修正方法**：
```python
import json
from datetime import datetime

# 读取账本
with open('/Users/qianmo/.qclaw/workspace/data/ledger.json', 'r') as f:
    data = json.load(f)

# 获取当前日期
today = datetime.now().strftime('%Y-%m-%d')

# 修正日期错误的记录
for entry in data['entries']:
    if entry['date'] > today:
        entry['date'] = today
        entry['updated_at'] = datetime.now().isoformat()

# 保存修正后的账本
with open('/Users/qianmo/.qclaw/workspace/data/ledger.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## ⚠️ 坑：飞书文件发送（2026-05-05）

飞书不支持直接通过 send_message 发送文件附件。需要通过 IM API 上传+发送。

**正确流程**：
1. 获取 tenant_access_token
2. 上传文件到飞书（POST /im/v1/files）
3. 发送文件消息（POST /im/v1/messages）

**示例代码**：
```python
import requests
import json

# 1. 获取 tenant_access_token
token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
token_data = {
    "app_id": "cli_a97f63c797381cc4",
    "app_secret": "3E2xIZg1XiB6mk5S5sJtthPz4IUmBu2c"
}
token_resp = requests.post(token_url, json=token_data)
tenant_token = token_resp.json()['tenant_access_token']

# 2. 上传文件
upload_url = "https://open.feishu.cn/open-apis/im/v1/files"
headers = {"Authorization": f"Bearer {tenant_token}"}
files = {"file": ("filename.xlsx", open("file.xlsx", "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
upload_resp = requests.post(upload_url, headers=headers, files=files)
file_key = upload_resp.json()['data']['file_key']

# 3. 发送文件消息
send_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
send_data = {
    "receive_id": "oc_6f0ea7a70225f5283fe5488e2ae7a750",
    "msg_type": "file",
    "content": json.dumps({"file_key": file_key})
}
send_resp = requests.post(send_url, headers=headers, json=send_data)
```

---

## 文件结构

```
~/.qclaw/workspace/data/
├── ledger.json              ← 账本（写入入口）
├── reimburse_pairs.json     ← 报销对表（5对）
├── correction_rules.json    ← 自我学习规则
└── to_excel.py             ← Excel 导出工具

~/.openclaw/workspace/skills/ledger-skill/
├── SKILL.md                 ← 本文件
└── scripts/
    └── ledger.py            ← 核心操作层（632行）
```

## 架构优化建议

### 合并工具调用

**问题**：每次记账都需要多次工具调用（读取账本 → 计算余额 → 写入账本 → 发送消息），导致延迟。

**优化方案**：使用 `execute_code` 合并多个操作：

```python
import json
import requests
from datetime import datetime

# 一次性完成所有操作
def add_entry_and_send(amount_yuan, date, merchant, category, note="", in_budget=True):
    # 1. 读取账本
    with open('/Users/qianmo/.qclaw/workspace/data/ledger.json', 'r') as f:
        data = json.load(f)
    
    # 2. 创建新条目
    entry = {
        "id": datetime.now().strftime('%Y%m%d%H%M%S'),
        "date": date,
        "amount": int(amount_yuan * 100),  # 转为分
        "currency": "CNY",
        "type": "expense" if amount_yuan < 0 else "income",
        "merchant": merchant,
        "merchant_std": merchant,
        "payment_method": "",
        "description": note,
        "category": category,
        "subcat": "",
        "in_budget": in_budget,
        "reimbursable": False,
        "reimbursed": False,
        "reimbursed_date": None,
        "reimbursement_id": None,
        "tags": [],
        "source": "manual",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "version": 1
    }
    
    # 3. 写入账本
    data['entries'].append(entry)
    with open('/Users/qianmo/.qclaw/workspace/data/ledger.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 4. 计算余额
    week_start = '2026-05-02'
    week_end = '2026-05-08'
    budget_expenses = []
    for entry in data['entries']:
        if week_start <= entry['date'] <= week_end:
            if entry['type'] == 'expense' and entry.get('in_budget') == True:
                budget_expenses.append(entry)
    
    total = sum(abs(entry['amount']) / 100 for entry in budget_expenses)
    remaining = data['weekly_budget'] / 100 - total
    
    # 5. 返回结果
    return {
        "success": True,
        "entry": entry,
        "remaining": remaining
    }
```

### 飞书文件发送优化

**问题**：飞书不支持直接发送文件附件，需要多次 API 调用。

**优化方案**：使用 `execute_code` 合并飞书 API 调用：

```python
import requests
import json

def send_file_to_feishu(file_path, chat_id, message=""):
    # 1. 获取 tenant_access_token
    token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    token_data = {
        "app_id": "cli_a97f63c797381cc4",
        "app_secret": "3E2xIZg1XiB6mk5S5sJtthPz4IUmBu2c"
    }
    token_resp = requests.post(token_url, json=token_data)
    tenant_token = token_resp.json()['tenant_access_token']
    
    # 2. 上传文件
    upload_url = "https://open.feishu.cn/open-apis/im/v1/files"
    headers = {"Authorization": f"Bearer {tenant_token}"}
    files = {"file": (file_path.split('/')[-1], open(file_path, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    upload_resp = requests.post(upload_url, headers=headers, files=files)
    file_key = upload_resp.json()['data']['file_key']
    
    # 3. 发送文件消息
    send_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    send_data = {
        "receive_id": chat_id,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key})
    }
    send_resp = requests.post(send_url, headers=headers, json=send_data)
    
    # 4. 发送文本消息（如果有）
    if message:
        text_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
        text_data = {
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": message})
        }
        text_resp = requests.post(text_url, headers=headers, json=text_data)
    
    return {
        "success": True,
        "file_key": file_key,
        "message_id": send_resp.json()['data']['message_id']
    }
```