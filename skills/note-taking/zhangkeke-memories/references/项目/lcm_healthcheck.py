#!/usr/bin/env python3
"""
LCM 健康监控 — 检测会话上下文膨胀，超标自动告警
运行方式: python3 lcm_healthcheck.py
退出码: 0=健康 1=警告 2=危险
"""

import sqlite3
import os
import json
import sys
from datetime import datetime

DB_PATH = os.path.expanduser("~/.qclaw/memory/lossless/lcm.db")

# 阈值配置
THRESHOLDS = {
    "summary_tokens_warn": 80_000,    # 单会话摘要 >80K tokens 警告
    "summary_tokens_danger": 150_000, # 单会话摘要 >150K tokens 危险
    "msg_tokens_warn": 500_000,       # 单会话消息 >500K tokens 警告
    "msg_tokens_danger": 2_000_000,   # 单会话消息 >2M tokens 危险
    "db_size_warn_mb": 100,           # 数据库文件 >100MB 警告
    "db_size_danger_mb": 200,         # 数据库文件 >200MB 危险
    "total_summary_tokens_warn": 200_000,  # 全局摘要总量 >200K 警告
}

def check_lcm():
    if not os.path.exists(DB_PATH):
        print("⚠️ LCM 数据库不存在")
        return 1

    db_size_mb = os.path.getsize(DB_PATH) / 1024 / 1024
    max_level = 0  # 0=OK, 1=warn, 2=danger
    alerts = []

    # 数据库大小检查
    if db_size_mb > THRESHOLDS["db_size_danger_mb"]:
        alerts.append(f"🔴 数据库文件 {db_size_mb:.1f}MB 超过危险阈值 {THRESHOLDS['db_size_danger_mb']}MB")
        max_level = 2
    elif db_size_mb > THRESHOLDS["db_size_warn_mb"]:
        alerts.append(f"🟡 数据库文件 {db_size_mb:.1f}MB 超过警告阈值 {THRESHOLDS['db_size_warn_mb']}MB")
        max_level = max(max_level, 1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 全局摘要总量
    cur.execute("SELECT COALESCE(SUM(token_count), 0) as total FROM summaries")
    total_summary_tokens = cur.fetchone()["total"]
    if total_summary_tokens > THRESHOLDS["total_summary_tokens_warn"]:
        alerts.append(f"🟡 全局摘要总量 {total_summary_tokens:,} tokens 超过阈值 {THRESHOLDS['total_summary_tokens_warn']:,}")
        max_level = max(max_level, 1)

    # 按会话检查
    cur.execute("""
        SELECT c.conversation_id, c.session_id, c.updated_at,
               COUNT(DISTINCT s.summary_id) as summary_count,
               COALESCE(SUM(s.token_count), 0) as summary_tokens,
               (SELECT COUNT(*) FROM messages m WHERE m.conversation_id = c.conversation_id) as msg_count,
               (SELECT COALESCE(SUM(m.token_count), 0) FROM messages m WHERE m.conversation_id = c.conversation_id) as msg_tokens
        FROM conversations c
        LEFT JOIN summaries s ON s.conversation_id = c.conversation_id
        GROUP BY c.conversation_id
        ORDER BY summary_tokens DESC
    """)

    rows = cur.fetchall()
    top_consumers = []

    for row in rows:
        sid = row["session_id"] or f"conv-{row['conversation_id']}"
        st = row["summary_tokens"]
        mt = row["msg_tokens"]
        sc = row["summary_count"]
        mc = row["msg_count"]

        if st > THRESHOLDS["summary_tokens_danger"] or mt > THRESHOLDS["msg_tokens_danger"]:
            alerts.append(f"🔴 会话 {sid[:12]}… 摘要{sc}条({st:,}t) 消息{mc}条({mt:,}t)")
            max_level = 2
        elif st > THRESHOLDS["summary_tokens_warn"] or mt > THRESHOLDS["msg_tokens_warn"]:
            alerts.append(f"🟡 会话 {sid[:12]}… 摘要{sc}条({st:,}t) 消息{mc}条({mt:,}t)")
            max_level = max(max_level, 1)

        if st > 10_000 or mt > 100_000:
            top_consumers.append({
                "session": sid[:20],
                "summaries": sc,
                "summary_tokens": st,
                "messages": mc,
                "msg_tokens": mt,
            })

    conn.close()

    # 输出报告
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if max_level == 0:
        print(f"✅ LCM 健康 | {now} | DB {db_size_mb:.1f}MB | {len(rows)}会话 | 全局摘要 {total_summary_tokens:,}t")
    elif max_level == 1:
        print(f"⚠️ LCM 警告 | {now}")
        for a in alerts:
            print(f"  {a}")
    else:
        print(f"🔴 LCM 危险 | {now}")
        for a in alerts:
            print(f"  {a}")

    # Top 5 消费者
    if top_consumers:
        top_consumers.sort(key=lambda x: x["summary_tokens"] + x["msg_tokens"] // 10, reverse=True)
        print(f"\n  Top {min(5, len(top_consumers))} 会话:")
        for i, tc in enumerate(top_consumers[:5], 1):
            print(f"  {i}. {tc['session']} | 摘要{tc['summaries']}条({tc['summary_tokens']:,}t) | 消息{tc['messages']}条({tc['msg_tokens']:,}t)")

    # 输出 JSON 供 cron 使用
    report = {
        "level": max_level,
        "db_size_mb": round(db_size_mb, 1),
        "total_conversations": len(rows),
        "total_summary_tokens": total_summary_tokens,
        "alerts": alerts,
        "top_consumers": top_consumers[:5],
        "checked_at": now,
    }
    report_path = os.path.expanduser("~/.qclaw/workspace/data/lcm_health.json")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return max_level

if __name__ == "__main__":
    sys.exit(check_lcm())
