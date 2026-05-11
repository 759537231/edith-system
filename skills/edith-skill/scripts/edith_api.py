#!/usr/bin/env python3
"""伊迪丝可视化面板 — API调用工具
用法：python3 edith_api.py <command> [args...]

命令：
  phase <phase>           设置阶段（idle/understand/round1/round2/dialogue/round3/confirm/execute/deliver）
  dept <name> <status> [task]  更新部门状态（idle/working/done）
  disc <round> <speaker> <content>  添加商讨记录
  mile <name> <status>    更新里程碑（pending/active/done）
  reset                   重置面板
  state                   获取当前状态
"""
import sys, json, urllib.request

BASE = "http://localhost:8080"

def api(path, data=None):
    req = urllib.request.Request(f"{BASE}{path}", 
        data=json.dumps(data).encode() if data else None,
        headers={"Content-Type": "application/json"},
        method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=3) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "phase" and len(sys.argv) >= 3:
        print(json.dumps(api("/api/phase", {"phase": sys.argv[2]})))
    elif cmd == "dept" and len(sys.argv) >= 4:
        data = {"department": sys.argv[2], "status": sys.argv[3]}
        if len(sys.argv) >= 5: data["task"] = sys.argv[4]
        print(json.dumps(api("/api/department", data)))
    elif cmd == "disc" and len(sys.argv) >= 5:
        print(json.dumps(api("/api/discussion", {
            "round": int(sys.argv[2]), "speaker": sys.argv[3], "content": sys.argv[4]
        })))
    elif cmd == "mile" and len(sys.argv) >= 4:
        print(json.dumps(api("/api/milestone", {"name": sys.argv[2], "status": sys.argv[3]})))
    elif cmd == "reset":
        print(json.dumps(api("/api/reset", {})))
    elif cmd == "state":
        print(json.dumps(api("/api/state"), indent=2, ensure_ascii=False))
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
