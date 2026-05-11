# 伊迪丝可视化面板 — 架构说明

## 组件

```
~/.hermes/edith-dashboard/
├── server.py           # Flask + SSE 服务器
├── templates/
│   └── index.html      # 前端界面（中国风宣纸风格）
├── venv/               # Python虚拟环境
└── edith_api.py        # API调用工具（已复制到skill scripts/）
```

## 启动

```bash
cd ~/.hermes/edith-dashboard
source venv/bin/activate
python server.py
# 访问 http://localhost:8080
```

## API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/state` | GET | 获取当前状态 |
| `/api/phase` | POST | 设置阶段 `{"phase":"understand"}` |
| `/api/department` | POST | 更新部门 `{"department":"工部","status":"working","task":"..."}` |
| `/api/discussion` | POST | 添加商讨 `{"round":1,"speaker":"小米","content":"..."}` |
| `/api/milestone` | POST | 更新里程碑 `{"name":"理解需求","status":"done"}` |
| `/api/reset` | POST | 重置面板 |
| `/stream` | GET | SSE事件流 |
| `/api/department/<name>` | GET | 部门详情（含知识库） |

## 前端功能

- 📊 8阶段流程图（理解→第一轮→第二轮→对话讨论→第三轮→确认→执行→交付）
- 🏢 10部门状态卡片（idle/working/done），可点击打开侧边栏
- 💬 商讨记录实时滚动，发言者标签化（深绿色圆角色块）
- 🎯 里程碑进度追踪（active状态弹跳动画）
- ▶ 演练按钮（实色填充，点击后disabled+loading状态）
- 三栏色彩体系：左=柳绿、中=天青、右=金色
- 当前步骤：实色填充+脉冲光晕+scale(1.1)
- 流程连接线：步骤间箭头+渐变色底线

## UI设计规范（2026-05-10）

CSS变量：`--paper`(暖白) `--ink`(深灰) `--green`(青瓷绿) `--green-dark`(深青瓷) `--willow`(柳绿) `--sky`(天青) `--gold`(金) `--red`(朱砂红)

字体：Noto Serif SC（Google Fonts），衬线体，中国风

布局：三栏grid（左280px部门 + 中自适应流程 + 右360px商讨），毛玻璃卡片(backdrop-filter:blur)

## 部门评估工作流（2026-05-10 验证）

评估类任务（"看看XX做得怎么样"）的标准流程：
1. 截图当前状态（browser_vision）
2. 读取源代码（read_file）
3. 并行派发评估部门（美术设计+市场运营部）
4. 每个部门独立评分+给出CSS级改进方案
5. 综合评判，按P0/P1/P2优先级排列
6. 派工部执行P0改进
7. 截图验证效果

**注意**：vision_analyze无法区分细微色差，验证CSS颜色必须用getComputedStyle。

## Pitfalls

- 端口8080常被占用，服务器自动查找可用端口
- Flask用`render_template()`查找`templates/`目录，不是`static/`
- 多文件用`execute_code`一次性创建，不要拆成多个write_file
- SKILL.md阶段变更时必须同步更新index.html的PHASES数组和PHASE_NAMES对象
- 面板进程需手动启动，edith_api.py调用前先curl确认面板在运行
- Flask多进程占端口：重启前必须`lsof -i :8080`确认释放
- CSS验证必须用getComputedStyle，vision_analyze看不清细微色差
