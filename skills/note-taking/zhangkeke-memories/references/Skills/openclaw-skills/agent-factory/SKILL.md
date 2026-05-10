# Agent 工厂 Skill

**版本**：v0.1 最小可行版
**目的**：通过对话 + 问卷，快速生成并安装新的 OpenClaw Skill Agent

---

## 触发词

用户说以下任一关键词时激活本 Skill：
- 「做一个新 Agent」
- 「帮我开发 Agent」
- 「新建一个 Agent」
- 「开发 Agent」

---

## 工作流程

### 阶段一：需求收集（对话式问卷）

收到触发词后，元 Agent 开始问卷流程：

**问题 1（必答）**
> 这个 Agent 是做什么的？请用一句话描述。

**问题 2（必答）**
> 这个 Agent 主要面向谁？（自己用 / 给他人用 / 公开发布）

**问题 3（选答）**
> 需要几个角色/分工？（单Agent / 多Agent协作）

**问题 4（选答）**
> 需要调用什么工具？（联网搜索 / 文件操作 / 数据库 / 其他）

收集完毕后，进入生成阶段。

---

### 阶段二：生成

调用对应模板生成文件：

```bash
python3 ~/.openclaw/workspace/skills/agent-factory/scripts/generate.py \
  --name "<Agent名称>" \
  --type "<类型: conversation | consultation | task>" \
  --roles "<角色数: 1 | 2+>" \
  --tools "<工具列表，用逗号分隔>"
```

生成结果：
- `~/.openclaw/workspace/skills/<Agent名称>/SKILL.md`
- `~/.openclaw/workspace/skills/<Agent名称>/roles/` （角色卡）
- `~/.openclaw/workspace/skills/<Agent名称>/protocols/` （协议文件）

---

### 阶段三：自动安装

```bash
python3 ~/.openclaw/workspace/skills/agent-factory/scripts/install.py \
  --skill "<Agent名称>"
```

安装完成后告知用户：「✅ 新 Agent 已就绪！直接说『[触发词]』即可使用」

---

## 模板说明

| 模板 | 适用场景 |
|------|---------|
| `conversation` | 通用对话型（个人助手、聊天机器人） |
| `consultation` | 垂直咨询型（即问即答，有专家角色） |
| `task` | 任务执行型（自动化操作、多步骤执行） |

---

## 输出格式

**问卷阶段**：直接对话提问，每次一个问题
**生成阶段**：展示生成进度
**安装完成**：确认信息 + 使用说明

---

## 约束

- Agent 名称只允许：中文、英文、数字、连字符
- 每个 Skill 生成后包含完整结构，不生成空壳
- 生成前先读模板文件，再写入，不要硬编码
- 安装后不自动重启 Gateway（QClaw 会自动检测新 Skill）
