# 伊迪丝可视化面板部署指南

## 部署位置

`~/.hermes/edith-dashboard/`

## 文件结构

```
edith-dashboard/
├── server.py              # Flask后端 + SSE实时推送
├── edith_api.py           # 伊迪丝调用工具（命令行）
├── templates/
│   └── index.html         # 前端界面（深色主题）
├── 80s-homepage.html      # 80年代风格示例页面
└── venv/                  # Python虚拟环境（已装Flask）
```

## 启动命令

```bash
cd ~/.hermes/edith-dashboard && source venv/bin/activate && python server.py
```

端口：8080（自动探测可用端口）

## edith_api.py 用法

```bash
API=~/.hermes/edith-dashboard/edith_api.py

# 设置阶段
python3 $API phase understand    # 理解
python3 $API phase round1        # 第一轮商讨
python3 $API phase round2        # 第二轮商讨
python3 $API phase dialogue      # 对话讨论（v5.1新增）
python3 $API phase round3        # 第三轮商讨
python3 $API phase confirm       # 确认
python3 $API phase execute       # 执行
python3 $API phase deliver       # 交付
python3 $API phase idle          # 待命

# 更新部门状态
python3 $API dept 工部 working "正在实现XXX"
python3 $API dept 工部 done

# 添加商讨记录
python3 $API disc 1 小米 "需求分析：用户需要..."
python3 $API disc 1 LongCat "风险点：..."
python3 $API disc 2 伊迪丝 "最终方案：..."

# 更新里程碑
python3 $API mile "需求理解" active
python3 $API mile "需求理解" done

# 重置面板
python3 $API reset
```

## API端点

| 端点 | 方法 | 功能 |
|------|------|------|
| `/` | GET | 前端页面 |
| `/stream` | GET | SSE事件流 |
| `/api/state` | GET | 获取当前状态 |
| `/api/phase` | POST | 更新阶段 |
| `/api/department` | POST | 更新部门状态 |
| `/api/department/<name>` | GET | 获取部门详情（职责/知识库/状态） |
| `/api/discussion` | POST | 添加商讨记录 |
| `/api/milestone` | POST | 更新里程碑 |
| `/api/reset` | POST | 重置面板 |

### 部门详情API（2026-05-10 新增）

`GET /api/department/<name>` 返回：
```json
{
  "name": "工部",
  "role": "代码实现、工具开发、自动化脚本",
  "status": "idle",
  "current_task": "",
  "knowledge": [
    {"file": "01-代码质量原则.md", "title": "代码质量与设计模式", "preview": "...前300字..."}
  ],
  "has_knowledge": true
}
```

**知识库路径映射**：部门名→目录路径在`server.py`的`DEPT_ROLES`字典中定义，注意工部路径是`software-development/coding-assistant`而非`departments/工部`。

## Pitfalls

1. **端口冲突**：8080常被占用，server.py已实现自动探测可用端口
2. **路径不匹配**：server.py用`render_template()`查找`templates/`目录，不是`static/`
3. **Flask未安装**：需在venv中运行，或`pip install flask`
4. **面板未启动**：伊迪丝执行任务前需确认面板在运行，否则API调用会Connection refused
5. **批量操作**：多个API调用应合并到一个terminal命令中，避免被中断
6. **SSE连接失败（2026-05-10）**：浏览器SSE readyState=0，前端收不到后端推送。原因：SSE端点`/stream`路径正确但连接未建立，需排查EventSource初始化和后端SSE实现
7. **demo()函数API调用未序列化（2026-05-10）**：前3个API调用同时发送，服务器状态混乱。应改为Promise链式调用
8. **SSE无重连机制（2026-05-10）**：`es.onerror`只记录日志，没有自动重连。应添加setTimeout重连逻辑
9. **API端点名称（2026-05-10）**：GET端点是`/api/state`不是`/api/status`，前端调用404会导致JSON解析错误
10. **CSS变量浏览器白屏（2026-05-10）**：CSS中使用`var(--xxx)`，curl确认HTML正确但浏览器显示白屏。可能原因：CSS语法错误阻塞渲染、Google Fonts加载失败。解法：变量名用英文不用中文、`@import url(...)`加`media="print" onload="this.media='all'"`避免阻塞、本地字体替代Google Fonts
11. **部门详情侧边栏（2026-05-10）**：前端`openSidebar(name)`调用`/api/department/<name>`，右侧滑出450px面板。部门卡片需`onclick="openSidebar('部门名')"` + `cursor:pointer`
12. **工部知识库路径（2026-05-10）**：工部知识库在`~/.hermes/skills/software-development/coding-assistant/knowledge/`，不在`departments/`下。`DEPT_ROLES`的`dir`字段需包含完整子路径（如`software-development/coding-assistant`）
13. **面板阶段必须与SKILL.md同步（2026-05-10 血的教训）**：当伊迪丝SKILL.md中的总调度流程变更（如新增"对话讨论"环节），必须同步更新`index.html`中的`PHASES`数组和`PHASE_NAMES`对象。否则面板显示的流程步骤与实际流程不一致。自检方法：`grep "const PHASES=" templates/index.html`，对比SKILL.md中的流程步骤数
14. **Flask重启必须杀旧进程（2026-05-10 强化）**：`pkill -f "python server.py"`可能杀不干净，用`lsof -i :8080 | grep LISTEN`找到实际PID再`kill -9`。重启后必须验证`curl -s http://localhost:8080/api/state`返回正确JSON

## SSE交互问题清单（2026-05-10 发现）

| # | 问题 | 位置 | 修复方案 |
|---|------|------|---------|
| 1 | SSE连接未建立 | index.html 第543行 | 检查EventSource初始化，确认后端/gen()生成器正常 |
| 2 | demo()API未序列化 | 第631-693行 | 改为Promise链式调用 |
| 3 | SSE无重连 | 第544-545行 | 添加setTimeout重连 |
| 4 | API无错误处理 | 第614-620行 | 添加response.ok检查和catch |
| 5 | UI更新无错误边界 | setPhase/setDept | 添加try-catch保护 |

## 版本

- v1.3 (2026-05-10) — 新增dialogue阶段（对话讨论）、面板阶段同步pitfall、Flask重启pitfall
- v1.2 (2026-05-10) — 新增部门详情API（/api/department/<name>）、侧边栏实现、CSS变量白屏pitfall、工部知识库路径pitfall
- v1.1 (2026-05-10) — 补充SSE交互问题清单、面板启动验证流程、API端点名称陷阱
- v1.0 (2026-05-09) — 初始版本，Flask + SSE + 原生前端
