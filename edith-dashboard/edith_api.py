#!/usr/bin/env python3
"""伊迪丝面板API — 供伊迪丝调用，实时推送状态到可视化面板"""
import sys, json, urllib.request

BASE = "http://localhost:8080"

def post(path, data):
    """调用面板API"""
    try:
        req = urllib.request.Request(
            f"{BASE}/api/{path}",
            data=json.dumps(data, ensure_ascii=False).encode(),
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=2)
    except Exception as e:
        print(f"[面板API] {path} 失败: {e}", file=sys.stderr)

def phase(p):
    """设置阶段: understand/round1/round2/round3/confirm/execute/deliver"""
    post("phase", {"phase": p})

def dept(name, status, task=""):
    """更新部门状态: idle/working/done"""
    post("department", {"department": name, "status": status, "task": task})

def disc(round_num, speaker, content):
    """添加商讨记录"""
    post("discussion", {"round": round_num, "speaker": speaker, "content": content})

def mile(name, status="active"):
    """更新里程碑: pending/active/done"""
    post("milestone", {"name": name, "status": status})

def reset():
    """重置面板"""
    post("reset", {})

# 命令行调用: python edith_api.py phase understand
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python edith_api.py <命令> [参数...]")
        print("命令: phase | dept | disc | mile | reset")
        sys.exit(0)
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    if cmd == "phase" and args:
        phase(args[0])
    elif cmd == "dept" and len(args) >= 2:
        dept(args[0], args[1], args[2] if len(args) > 2 else "")
    elif cmd == "disc" and len(args) >= 3:
        disc(int(args[0]), args[1], " ".join(args[2:]))
    elif cmd == "mile" and args:
        mile(args[0], args[1] if len(args) > 1 else "active")
    elif cmd == "reset":
        reset()
    else:
        print(f"未知命令或参数不足: {cmd} {args}")
