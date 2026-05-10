#!/usr/bin/env python3
"""伊迪丝可视化面板 — Flask + SSE + 任务控制"""
import json, socket, threading, time
from datetime import datetime
from flask import Flask, render_template, Response, request, jsonify
from queue import Queue

app = Flask(__name__)

DEPARTMENTS = ["枢密院","市场运营部","工部","通商部","户部","美术设计","交互设计","视频创作部","刑部","门下省"]

class Task:
    """单个任务的状态"""
    def __init__(self, task_id, dept, description):
        self.task_id = task_id
        self.dept = dept
        self.description = description
        self.status = "pending"  # pending/running/done/failed/paused/killed
        self.session_id = None
        self.start_time = None
        self.last_output_time = None
        self.timeout = 120  # 120秒无输出视为卡死
        self.paused = False
        self.killed = False

    def to_dict(self):
        elapsed = 0
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
        return {
            "task_id": self.task_id,
            "dept": self.dept,
            "description": self.description,
            "status": self.status,
            "elapsed": elapsed,
            "paused": self.paused
        }

class State:
    def __init__(self):
        self.phase = "idle"
        self.depts = {d: {"status":"idle","task":""} for d in DEPARTMENTS}
        self.discussions = []  # [{round,speaker,content,ts}]
        self.milestones = []   # [{name,status}]
        self.clients = []
        self.lock = threading.Lock()
        self.tasks = {}  # task_id -> Task
        self.current_task_id = None

    def broadcast(self, data):
        dead = []
        for q in self.clients:
            try: q.put_nowait(data)
            except: dead.append(q)
        for q in dead: self.clients.remove(q)

    def add_client(self):
        q = Queue()
        self.clients.append(q)
        return q

    def create_task(self, dept, description):
        """创建新任务"""
        task_id = f"task_{int(time.time())}"
        task = Task(task_id, dept, description)
        self.tasks[task_id] = task
        self.current_task_id = task_id
        self.broadcast({"t":"task_created","task":task.to_dict()})
        return task_id

    def start_task(self, task_id, session_id=None):
        """开始任务"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = "running"
            task.session_id = session_id
            task.start_time = time.time()
            task.last_output_time = time.time()
            self.broadcast({"t":"task_started","task":task.to_dict()})

    def update_task_output(self, task_id):
        """更新任务输出时间（用于卡死检测）"""
        if task_id in self.tasks:
            self.tasks[task_id].last_output_time = time.time()

    def complete_task(self, task_id, status="done"):
        """完成任务"""
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            self.broadcast({"t":"task_completed","task_id":task_id,"status":status})

    def pause_task(self, task_id):
        """暂停任务"""
        if task_id in self.tasks:
            self.tasks[task_id].paused = True
            self.tasks[task_id].status = "paused"
            self.broadcast({"t":"task_paused","task_id":task_id})

    def kill_task(self, task_id):
        """终止任务"""
        if task_id in self.tasks:
            self.tasks[task_id].killed = True
            self.tasks[task_id].status = "killed"
            self.broadcast({"t":"task_killed","task_id":task_id})

    def check_stuck_tasks(self):
        """检查卡死的任务"""
        stuck = []
        for task_id, task in self.tasks.items():
            if task.status == "running" and task.last_output_time:
                if time.time() - task.last_output_time > task.timeout:
                    stuck.append(task_id)
        return stuck

state = State()

# 后台线程：卡死检测
def stuck_checker():
    while True:
        time.sleep(30)  # 每30秒检查一次
        stuck = state.check_stuck_tasks()
        for task_id in stuck:
            state.broadcast({"t":"task_stuck","task_id":task_id,"message":"任务可能卡死，建议暂停或终止"})

checker_thread = threading.Thread(target=stuck_checker, daemon=True)
checker_thread.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/80s-v2")
def homepage_80s_v2():
    from flask import send_from_directory
    import os
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "80s-v2.html")

@app.route("/stream")
def stream():
    def gen():
        q = state.add_client()
        try:
            # 1. 立即发送连接确认 + 当前完整状态
            import time as _t
            tasks = [t.to_dict() for t in state.tasks.values()]
            init = {
                "t": "init",
                "phase": state.phase,
                "departments": state.depts,
                "discussions": state.discussions[-30:],
                "milestones": state.milestones,
                "tasks": tasks,
                "current_task_id": state.current_task_id
            }
            yield f"data: {json.dumps(init, ensure_ascii=False)}\n\n"
            # 2. 事件循环 + 心跳
            while True:
                try:
                    msg = q.get(timeout=15)
                    yield f"data: {json.dumps(msg, ensure_ascii=False)}\n\n"
                except Exception:
                    yield ": heartbeat\n\n"
        except GeneratorExit:
            if q in state.clients: state.clients.remove(q)
    return Response(gen(), mimetype="text/event-stream", headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})

@app.route("/api/state")
def get_state():
    tasks = [t.to_dict() for t in state.tasks.values()]
    return jsonify({
        "phase": state.phase,
        "departments": state.depts,
        "discussions": state.discussions[-30:],
        "milestones": state.milestones,
        "tasks": tasks,
        "current_task_id": state.current_task_id
    })

@app.route("/api/phase", methods=["POST"])
def set_phase():
    state.phase = request.json.get("phase","idle")
    state.broadcast({"t":"phase","v":state.phase})
    return jsonify(ok=True)

@app.route("/api/department", methods=["POST"])
def set_dept():
    d = request.json
    name = d.get("department","")
    if name in state.depts:
        state.depts[name].update(status=d.get("status","idle"), task=d.get("task",""))
        state.broadcast({"t":"dept","name":name,**state.depts[name]})
    return jsonify(ok=True)

@app.route("/api/discussion", methods=["POST"])
def add_disc():
    d = request.json
    entry = {"round":d.get("round",1),"speaker":d.get("speaker",""),"content":d.get("content",""),"ts":datetime.now().strftime("%H:%M:%S")}
    state.discussions.append(entry)
    state.broadcast({"t":"disc",**entry})
    return jsonify(ok=True)

@app.route("/api/milestone", methods=["POST"])
def set_mile():
    d = request.json
    name = d.get("name","")
    status = d.get("status","pending")
    found = [m for m in state.milestones if m["name"]==name]
    if found:
        found[0]["status"] = status
    else:
        state.milestones.append({"name":name,"status":status})
    state.broadcast({"t":"mile","name":name,"status":status})
    return jsonify(ok=True)

@app.route("/api/reset", methods=["POST"])
def reset():
    state.phase = "idle"
    for d in state.depts: state.depts[d].update(status="idle",task="")
    state.discussions.clear()
    state.milestones.clear()
    state.tasks.clear()
    state.current_task_id = None
    state.broadcast({"t":"reset"})
    return jsonify(ok=True)

# === 新增：任务控制 API ===

@app.route("/api/task/create", methods=["POST"])
def create_task():
    d = request.json
    task_id = state.create_task(d.get("dept",""), d.get("description",""))
    return jsonify(ok=True, task_id=task_id)

@app.route("/api/task/start", methods=["POST"])
def start_task():
    d = request.json
    state.start_task(d.get("task_id",""), d.get("session_id"))
    return jsonify(ok=True)

@app.route("/api/task/complete", methods=["POST"])
def complete_task():
    d = request.json
    state.complete_task(d.get("task_id",""), d.get("status","done"))
    return jsonify(ok=True)

@app.route("/api/task/pause", methods=["POST"])
def pause_task():
    d = request.json
    task_id = d.get("task_id","")
    state.pause_task(task_id)
    # 通知伊迪丝暂停
    state.broadcast({"t":"action","action":"pause","task_id":task_id})
    return jsonify(ok=True)

@app.route("/api/task/kill", methods=["POST"])
def kill_task():
    d = request.json
    task_id = d.get("task_id","")
    state.kill_task(task_id)
    # 通知伊迪丝终止
    state.broadcast({"t":"action","action":"kill","task_id":task_id})
    return jsonify(ok=True)

@app.route("/api/task/output", methods=["POST"])
def task_output():
    """更新任务输出时间（防止卡死检测误报）"""
    d = request.json
    state.update_task_output(d.get("task_id",""))
    return jsonify(ok=True)

def free_port(start=8080):
    for p in range(start, start+50):
        try:
            with socket.socket() as s: s.bind(("",p)); return p
        except: pass
    return start

# === 新增：部门详情 API ===
import os

DEPT_ROLES = {
    "枢密院": {"role": "战略判断、任务拆解顺序", "has_knowledge": False, "dir": None},
    "市场运营部": {"role": "需求分析、市场分析、运营策略", "has_knowledge": True, "dir": "departments/shichangyunyingbu"},
    "工部": {"role": "代码实现、工具开发、自动化脚本", "has_knowledge": True, "dir": "software-development/coding-assistant"},
    "通商部": {"role": "联网搜索、API调用、信息收集", "has_knowledge": False, "dir": "departments/tongshangbu"},
    "户部": {"role": "数据核算、报表、统计", "has_knowledge": True, "dir": "departments/hubu"},
    "美术设计": {"role": "视觉设计、UI设计、美术风格", "has_knowledge": True, "dir": "departments/meishusheji"},
    "交互设计": {"role": "交互逻辑、用户体验、流程设计", "has_knowledge": True, "dir": "departments/jiaohusheji"},
    "视频创作部": {"role": "脚本、分镜、构图、运镜、剪辑", "has_knowledge": True, "dir": "departments/shipinchuangzuobu"},
    "刑部": {"role": "动作安全、权限校验", "has_knowledge": False, "dir": "departments/xingbu"},
    "门下省": {"role": "对外输出合规审核", "has_knowledge": False, "dir": "departments/menxiasheng"}
}

@app.route("/api/department/<name>")
def get_department_detail(name):
    if name not in DEPARTMENTS:
        return jsonify({"error": "部门不存在"}), 404
    
    dept_info = DEPT_ROLES.get(name, {"role": "未知", "has_knowledge": False})
    dept_state = state.depts.get(name, {"status": "idle", "task": ""})
    
    # 读取知识库
    knowledge_content = []
    if dept_info.get("has_knowledge") and dept_info.get("dir"):
        knowledge_path = os.path.expanduser(f"~/.hermes/skills/{dept_info['dir']}/knowledge/")
        if os.path.exists(knowledge_path):
            for f in sorted(os.listdir(knowledge_path)):
                if f.endswith('.md'):
                    try:
                        with open(os.path.join(knowledge_path, f), 'r', encoding='utf-8') as file:
                            content = file.read()
                            # 提取标题和前300字符
                            lines = content.split('\n')
                            title = lines[0].replace('#', '').strip() if lines else f
                            preview = content[:300] + "..." if len(content) > 300 else content
                            knowledge_content.append({"file": f, "title": title, "preview": preview})
                    except:
                        knowledge_content.append({"file": f, "title": f, "preview": "读取失败"})
    
    return jsonify({
        "name": name,
        "role": dept_info.get("role", "未知"),
        "status": dept_state.get("status", "idle"),
        "current_task": dept_state.get("task", ""),
        "knowledge": knowledge_content,
        "has_knowledge": dept_info.get("has_knowledge", False)
    })

@app.route("/80s")
def homepage_80s():
    return render_template("80s-homepage.html")

if __name__ == "__main__":
    port = free_port()
    print(f"🏛️  伊迪丝可视化面板: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, threaded=True)
