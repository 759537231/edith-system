#!/usr/bin/env python3
"""
ledger-skill 快速调用脚本
用法：python3 ledger_wrapper.py <method> [args]
"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/skills/ledger-skill/scripts'))
import ledger, json

def cmd(args):
    method = args[0] if args else 'audit'
    
    if method == 'audit':
        r = ledger.audit()
        s = r['summary']
        print(f'📊 4月账单')
        print(f'月度预算: ¥{s["budget_yuan"]:.2f}')
        print(f'预算内支出: ¥{s["in_budget_sum"]/100:.2f}（{s["in_budget_count"]}条）')
        print(f'💰 预算剩余: ¥{s["budget_remaining_yuan"]:.2f}')
        pairs = ledger.get_reimburse_pairs()
        print(f'\n报销对 {len(pairs)} 对:')
        for p in pairs:
            sign = '✅' if p['status']=='配平' else '⚠️'
            oop = p.get('out_of_pocket',0)
            oop_str = f'自付¥{oop/100:.2f}' if oop>0 else f'赚¥{abs(oop)/100:.2f}' if oop<0 else '配平'
            print(f'  {sign} {p["category"]} {oop_str}')
    elif method == 'add':
        # python3 ledger_wrapper.py add -75.26 2026-04-13 赵一鸣 零食
        amount = float(args[1]) if len(args)>1 else -float(input('金额:'))
        date   = args[2] if len(args)>2 else input('日期:')
        merchant = args[3] if len(args)>3 else input('商户:')
        cat = args[4] if len(args)>4 else ''
        r = ledger.add_entry(amount_yuan=-abs(amount), date=date, merchant=merchant,
                             etype='expense', category=cat or '📦 其他', note='', in_budget=True)
        print(f'✅ 已入账: {date} {merchant} ¥{abs(amount):.2f}')
    else:
        print(f'用法: ledger_wrapper.py [audit|add|summary|pairs]')

if __name__ == '__main__':
    cmd(sys.argv[1:])