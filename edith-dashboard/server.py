#!/usr/bin/env python3
"""伊迪丝可视化面板 — Flask + SSE"""
import json, socket, threading
from datetime import datetime
from flask import Flask, render_template, Response, request, jsonify
from queue import Queue

app = Flask(__name__)

DEPARTMENTS = ["枢密院","市场运营部","工部","通商部","户部","美术设计","交互设计","刑部","门下省"]

class State:
    def __init__(self):
        self.phase = "idle"
        self.depts = {d: {"status":"idle","task":""} for d in DEPARTMENTS}
        self.discussions = []  # [{round,speaker,content,ts}]
        self.milestones = []   # [{name,status}]
        self.clients = []
        self.lock = threading.Lock()

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

state = State()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stream")
def stream():
    def gen():
        q = state.add_client()
        try:
            while True:
                yield f"data: {json.dumps(q.get(), ensure_ascii=False)}\n\n"
        except GeneratorExit:
            if q in state.clients: state.clients.remove(q)
    return Response(gen(), mimetype="text/event-stream")

@app.route("/api/state")
def get_state():
    return jsonify({"phase": state.phase, "departments": state.depts,
                    "discussions": state.discussions[-30:], "milestones": state.milestones})

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
    state.broadcast({"t":"reset"})
    return jsonify(ok=True)

def free_port(start=8080):
    for p in range(start, start+50):
        try:
            with socket.socket() as s: s.bind(("",p)); return p
        except: pass
    return start

if __name__ == "__main__":
    port = free_port()
    print(f"🏛️  伊迪丝可视化面板: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, threaded=True)
