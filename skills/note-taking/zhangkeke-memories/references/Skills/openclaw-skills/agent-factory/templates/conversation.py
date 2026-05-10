"""
通用对话型 Agent 模板
v0.1 - 最小可行版
用法：python generate.py --name "xxx" --type conversation --roles 1
"""

SKILL_MD = """# {name} Agent

**版本**：v0.1 自动生成
**类型**：通用对话型
**生成时间**：{timestamp}

---

## 触发词

- 「{trigger}」
- 「打开{name}」
- 「开始{name}」

---

## Agent 简介

{description}

---

## 核心能力

{capabilities}

---

## 工作流程

{workflow}

---

## 输出格式

{output_format}

---

## 约束

- {constraint_1}
- {constraint_2}
- {constraint_3}

---

## 记忆

- 用户信息：{user_info}
- 关键决策：每次重要对话后更新 MEMORY.md
- 数据存储：对话摘要存至 IMA 知识库「{name}」笔记本

---

*本文件由 Agent 工厂 Skill 自动生成 · {timestamp}*
"""

ROLE_SYSTEM = """你是「{agent_name}」，一个{role_description}。

## 你的身份
- 名称：{agent_name}
- 定位：{role定位}
- 风格：{style}

## 核心职责
{responsibilities}

## 工作原则
1. {principle_1}
2. {principle_2}
3. {principle_3}

## 禁止事项
- {forbidden_1}
- {forbidden_2}

## 记忆
- 与用户的对话摘要定期存入知识库
- 关键偏好和决策记录在 MEMORY.md

---
*由 Agent 工厂 Skill 生成 · {timestamp}*
"""

ROLE_USER_GUIDE = """## 用户须知

- 本 Agent 名称：{agent_name}
- 使用方式：直接发送消息即可
- 退出方式：发送「退出」或切换至其他 Agent
- 数据说明：对话内容默认不外传
"""


def generate(answers: dict) -> dict:
    """
    根据用户回答生成对话型 Agent 的文件内容

    answers 预期字段：
      - name: Agent 名称
      - trigger: 触发词
      - description: 一句话描述
      - capabilities: 核心能力列表（每行一条）
      - workflow: 工作流程描述
      - output_format: 输出格式描述
      - style: Agent 风格
      - user_info: 用户信息说明
    """
    from datetime import datetime
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 填充默认值
    name = answers.get("name", "新Agent")
    trigger = answers.get("trigger", name)
    description = answers.get("description", "一个智能助手")
    capabilities = answers.get("capabilities", "回答用户问题\n协助完成任务")
    workflow = answers.get("workflow", "接收消息 → 理解意图 → 回答/执行 → 记录关键信息")
    output_format = answers.get("output_format", "直接回答，简洁清晰")
    style = answers.get("style", "温暖、专业、有耐心")
    user_info = answers.get("user_info", "基础信息（姓名、偏好等）")

    files = {}

    # 生成 SKILL.md
    files["SKILL.md"] = SKILL_MD.format(
        name=name,
        trigger=trigger,
        description=description,
        capabilities=capabilities,
        workflow=workflow,
        output_format=output_format,
        constraint_1="只回答确定的知识，不确定时说不知道",
        constraint_2="不泄露用户隐私",
        constraint_3="对话简洁，不废话",
        user_info=user_info,
        timestamp=ts,
    )

    # 生成角色卡
    files["roles/main.md"] = ROLE_SYSTEM.format(
        agent_name=name,
        role_description=description,
        role定位="助手",
        style=style,
        responsibilities=f"1. {capabilities.split(chr(10))[0] if chr(10) in capabilities else capabilities}",
        principle_1="准确优先，不确定则诚实承认",
        principle_2="简洁回答，不绕弯子",
        principle_3="主动记忆用户偏好",
        forbidden_1="编造事实或数据",
        forbidden_2="回答超出能力范围的问题",
        timestamp=ts,
    )

    # 生成用户指南
    files["roles/guide.md"] = ROLE_USER_GUIDE.format(
        agent_name=name,
    )

    return files
