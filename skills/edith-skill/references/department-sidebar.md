# 部门详情侧边栏实现模式

> 2026-05-10 实现，可复用于任何需要"卡片点击→详情展示"的面板。

## 架构

```
前端（index.html）          后端（server.py）
  部门卡片 onclick  →  fetch /api/department/<name>
                              ↓
                        读取 DEPT_ROLES 映射
                        读取知识库文件
                        返回 JSON
                              ↓
  侧边栏渲染  ←  JSON 数据
```

## 后端API模板

```python
@app.route("/api/department/<name>")
def get_department_detail(name):
    dept_info = DEPT_ROLES.get(name, {"role": "未知", "has_knowledge": False})
    dept_state = state.depts.get(name, {"status": "idle", "task": ""})
    
    # 读取知识库
    knowledge_content = []
    if dept_info.get("has_knowledge") and dept_info.get("dir"):
        knowledge_path = os.path.expanduser(f"~/.hermes/skills/{dept_info['dir']}/knowledge/")
        if os.path.exists(knowledge_path):
            for f in sorted(os.listdir(knowledge_path)):
                if f.endswith('.md'):
                    with open(os.path.join(knowledge_path, f), 'r', encoding='utf-8') as file:
                        content = file.read()
                        lines = content.split('\n')
                        title = lines[0].replace('#', '').strip() if lines else f
                        preview = content[:300] + "..." if len(content) > 300 else content
                        knowledge_content.append({"file": f, "title": title, "preview": preview})
    
    return jsonify({
        "name": name,
        "role": dept_info.get("role", "未知"),
        "status": dept_state.get("status", "idle"),
        "current_task": dept_state.get("task", ""),
        "knowledge": knowledge_content,
        "has_knowledge": dept_info.get("has_knowledge", False)
    })
```

## 前端侧边栏模板

### HTML结构
```html
<div id="deptSidebar" class="sidebar">
  <div class="sidebar-header">
    <h3 id="deptName">部门名称</h3>
    <button class="close-btn" onclick="closeSidebar()">×</button>
  </div>
  <div class="sidebar-content">
    <div class="dept-info"><h4>📋 职责</h4><p id="deptRole">-</p></div>
    <div class="dept-info"><h4>🔄 当前状态</h4><p id="deptStatus">-</p></div>
    <div class="dept-info"><h4>📝 当前任务</h4><p id="deptTask">-</p></div>
    <div class="dept-info"><h4>📚 知识库</h4><div id="deptKnowledge">暂无知识库</div></div>
  </div>
</div>
<div id="sidebarOverlay" class="overlay" onclick="closeSidebar()"></div>
```

### CSS关键样式
```css
.sidebar {
  position: fixed; top: 0; right: -450px; width: 450px; height: 100vh;
  background: var(--paper); box-shadow: -4px 0 20px rgba(0,0,0,0.15);
  transition: right 0.3s ease; z-index: 1000; overflow-y: auto;
}
.sidebar.open { right: 0; }
.overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); z-index: 999; }
.overlay.show { display: block; }
```

### JS交互
```javascript
function openSidebar(deptName) {
  fetch('/api/department/' + encodeURIComponent(deptName))
    .then(r => r.json())
    .then(data => {
      document.getElementById('deptName').textContent = data.name;
      document.getElementById('deptRole').textContent = data.role;
      document.getElementById('deptStatus').textContent = data.status;
      document.getElementById('deptTask').textContent = data.current_task || '无';
      var knowledgeDiv = document.getElementById('deptKnowledge');
      if (data.knowledge && data.knowledge.length > 0) {
        knowledgeDiv.innerHTML = data.knowledge.map(k => 
          '<div class="knowledge-item"><strong>' + k.title + '</strong><p>' + k.preview + '</p></div>'
        ).join('');
      } else {
        knowledgeDiv.textContent = '暂无知识库';
      }
      document.getElementById('deptSidebar').classList.add('open');
      document.getElementById('sidebarOverlay').classList.add('show');
    });
}
function closeSidebar() {
  document.getElementById('deptSidebar').classList.remove('open');
  document.getElementById('sidebarOverlay').classList.remove('show');
}
```

### 给卡片添加点击事件
```javascript
// 在init()中，给每个卡片添加onclick
document.getElementById("dept-list").innerHTML = DEPTS.map(d =>
  '<div class="dept" id="d-'+d+'" onclick="openSidebar(\''+d+'\')" style="cursor:pointer">...'
).join("");
```

## Pitfalls

1. **知识库路径不统一**：工部在`software-development/coding-assistant/`，其他在`departments/{拼音}/`。必须用映射表。
2. **中文URL编码**：fetch时必须用`encodeURIComponent(deptName)`。
3. **Flask热更新失败**：添加新路由后必须kill旧进程重启，否则404。
4. **侧边栏z-index**：必须高于主内容（1000），overlay用999。
