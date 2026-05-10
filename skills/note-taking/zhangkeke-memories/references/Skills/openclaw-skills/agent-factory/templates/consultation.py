"""
垂直咨询型 Agent 模板
适用于：专业咨询、多角色分诊、联合会诊场景
用法：python generate.py --name "法律咨询" --type consultation --roles 3
"""

SKILL_MD = """# {name}

**版本**：v0.1 自动生成
**类型**：垂直咨询型（多角色分诊）
**生成时间**：{timestamp}

---

## 触发词

- 「{trigger}」
- 「打开{name}」
- 「咨询{name}」

---

## 简介

{description}

---

## 角色团队

| 角色 | 职责 | 专业方向 |
|------|------|---------|
{role_table}

---

## 工作流程

### 阶段一：分诊（主诊评估）
1. 接收用户描述的问题
2. 判断属于哪个角色领域
3. 如需多角色协作，说明分工

### 阶段二：深度咨询
{consultation_steps}

### 阶段三：共识输出
1. 综合各角色观点
2. 给出明确结论 + 可执行方案
3. 标注需进一步确认的事项

---

## 输出格式

### 单角色结论
```
📌 结论：[一句话核心判断]
📋 方案：[具体可执行步骤]
⚠️ 注意：[需注意的事项]
❓ 待确认：[需要用户/专业人士确认的点]
```

### 多角色会诊
```
📊 会诊结论
━━━━━━━━━━━━━━
核心判断：[各角色共识]
━━━━━━━━━━━━━━
【角色A】观点 + 方案
【角色B】观点 + 方案
━━━━━━━━━━━━━━
📌 最终建议：[综合方案]
⚠️ 注意事项：[风险/禁忌]
```

---

## 约束

- {constraint_1}
- {constraint_2}
- {constraint_3}
- 涉及严重情况时必须建议就医/求助专业人士

---

## 记忆

- 用户病史/历史问题：每次咨询后更新
- 关键决策记录至 MEMORY.md
- 详细记录存至 IMA 知识库

---

*本文件由 Agent 工厂 Skill 自动生成 · {timestamp}*
"""


def generate(answers: dict) -> dict:
    """
    根据用户回答生成咨询型 Agent 的文件内容

    answers 预期字段：
      - name: Agent 名称
      - trigger: 触发词
      - description: 一句话描述
      - roles: 角色列表 [{"name":"xx", "duty":"xx", "field":"xx"}, ...]
      - style: Agent 风格
      - constraint_1/2/3: 约束
      - consultation_steps: 咨询步骤描述
    """
    from datetime import datetime
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    name = answers.get("name", "新Agent")
    trigger = answers.get("trigger", name)
    description = answers.get("description", "多角色专业咨询服务")
    roles = answers.get("roles", [
        {"name": "主诊", "duty": "初步评估与分诊", "field": "通用"},
    ])
    style = answers.get("style", "专业、严谨、有温度")

    # 构建角色表
    role_table = ""
    for r in roles:
        role_table += f"| {r.get('name', '角色')} | {r.get('duty', '待定')} | {r.get('field', '待定')} |\n"

    # 构建咨询步骤
    if len(roles) == 1:
        consultation_steps = answers.get("consultation_steps",
            "1. 深入了解问题细节\n"
            "2. 基于专业知识分析\n"
            "3. 给出结论和方案"
        )
    else:
        step_lines = []
        for i, r in enumerate(roles):
            step_lines.append(f"{i+1}. 【{r.get('name','角色{i+1}')}】分析本领域问题")
        step_lines.append(f"{len(roles)+1}. 综合各角色结论，形成最终方案")
        consultation_steps = answers.get("consultation_steps", "\n".join(step_lines))

    constraint_1 = answers.get("constraint_1", "给出结论需有依据，不凭空判断")
    constraint_2 = answers.get("constraint_2", "不确定时明确说明，不敷衍")
    constraint_3 = answers.get("constraint_3", "严重情况建议寻求专业帮助")

    files = {}

    # 生成 SKILL.md
    files["SKILL.md"] = SKILL_MD.format(
        name=name,
        trigger=trigger,
        description=description,
        role_table=role_table,
        consultation_steps=consultation_steps,
        constraint_1=constraint_1,
        constraint_2=constraint_2,
        constraint_3=constraint_3,
        timestamp=ts,
    )

    # 为每个角色生成角色卡
    for i, r in enumerate(roles):
        role_name = r.get("name", f"角色{i+1}")
        role_duty = r.get("duty", "待定")
        role_field = r.get("field", "待定")

        role_md = f"""# {role_name}

**所属**：{name}
**职责**：{role_duty}
**专业方向**：{role_field}

---

## 工作原则

1. 基于专业判断，给出明确观点
2. 不确定时诚实标注
3. 与其他角色互补，不重复

## 输出要求

- 先给结论，再说依据
- 方案具体可执行
- 标注风险和注意事项

---
*由 Agent 工厂 Skill 生成 · {ts}*
"""
        files[f"roles/{role_name}.md"] = role_md

    # 主诊角色（如果多角色，额外生成一个总协调）
    if len(roles) > 1:
        files["roles/协调员.md"] = f"""# 协调员（总控）

**所属**：{name}
**职责**：统筹各角色，综合输出最终方案

---

## 工作原则

1. 先分诊，再派发
2. 综合各角色观点，形成统一结论
3. 结论要有优先级：最重要 → 次要 → 可选

## 输出格式

按会诊模板输出，确保：
- 核心判断一句话说清
- 各角色观点不遗漏
- 最终建议可执行

---
*由 Agent 工厂 Skill 生成 · {ts}*
"""

    return files
