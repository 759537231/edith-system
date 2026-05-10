"""
任务执行型 Agent 模板
适用于：自动化操作、多步骤任务、批量处理
用法：python generate.py --name "数据清洗" --type task --roles 1
"""

SKILL_MD = """# {name}

**版本**：v0.1 自动生成
**类型**：任务执行型
**生成时间**：{timestamp}

---

## 触发词

- 「{trigger}」
- 「执行{name}」
- 「开始{name}」

---

## 简介

{description}

---

## 核心能力

{capabilities}

---

## 工作流程

### 接收任务
1. 解析用户指令，明确任务目标
2. 确认输入/输出格式
3. 如不明确，向用户确认（最多2轮）

### 执行任务
{task_steps}

### 汇报结果
```
✅ 任务完成
━━━━━━━━━━━━━━
📊 处理量：[数量]
⏱ 耗时：[预估]
📁 输出：[文件路径/位置]
⚠️ 异常：[数量，如无则写"无"]
━━━━━━━━━━━━━━
```

---

## 批量模式

当任务涉及多个项目时：
1. 先列出所有待处理项
2. 逐项处理，每完成一项打 ✅
3. 遇到错误标记 ⚠️，继续处理剩余项
4. 最终输出汇总报告

示例：
```
⏳ 处理中...
  ✅ 项目A
  ✅ 项目B
  ⚠️ 项目C（原因：格式错误，已跳过）
  ✅ 项目D
━━━━━━━━━━━━━━
完成 4/5，异常 1
```

---

## 错误处理

- 文件不存在 → 提示用户检查路径
- 格式错误 → 记录并跳过，不中断
- 权限不足 → 明确告知所需权限
- 工具缺失 → 提示安装方法

---

## 约束

- {constraint_1}
- {constraint_2}
- {constraint_3}
- 批量操作前先确认（超过10项时）
- 不删除用户文件，只创建/修改

---

## 工具

{tools_section}

---

## 记忆

- 任务历史：记录每次执行的关键参数和结果
- 错误日志：记录常见错误及解决方案
- 优化建议：根据执行经验提出改进

---

*本文件由 Agent 工厂 Skill 自动生成 · {timestamp}*
"""


def generate(answers: dict) -> dict:
    """
    根据用户回答生成任务执行型 Agent 的文件内容

    answers 预期字段：
      - name: Agent 名称
      - trigger: 触发词
      - description: 一句话描述
      - capabilities: 核心能力列表
      - task_steps: 任务步骤
      - tools: 需要的工具列表
      - constraint_1/2/3: 约束
    """
    from datetime import datetime
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    name = answers.get("name", "新Agent")
    trigger = answers.get("trigger", name)
    description = answers.get("description", f"{name} 自动化任务")
    capabilities = answers.get("capabilities",
        "自动解析任务指令\n批量处理数据文件\n生成执行报告"
    )
    tools = answers.get("tools", ["文件读写", "数据分析"])

    # 构建任务步骤
    task_steps = answers.get("task_steps",
        "1. 验证输入文件/数据\n"
        "2. 按规则执行处理\n"
        "3. 验证输出结果\n"
        "4. 生成执行报告"
    )

    # 构建工具部分
    tools_section = ""
    for t in tools:
        tools_section += f"- {t}\n"
    if not tools_section:
        tools_section = "暂无外部工具依赖\n"

    constraint_1 = answers.get("constraint_1", "操作前先确认，避免误操作")
    constraint_2 = answers.get("constraint_2", "遇到错误不中断，记录并继续")
    constraint_3 = answers.get("constraint_3", "输出结果可追溯、可复现")

    files = {}

    # 生成 SKILL.md
    files["SKILL.md"] = SKILL_MD.format(
        name=name,
        trigger=trigger,
        description=description,
        capabilities=capabilities,
        task_steps=task_steps,
        constraint_1=constraint_1,
        constraint_2=constraint_2,
        constraint_3=constraint_3,
        tools_section=tools_section,
        timestamp=ts,
    )

    # 生成执行器角色卡
    files["roles/executor.md"] = f"""# 执行器

**所属**：{name}
**职责**：接收指令、执行任务、汇报结果

---

## 工作原则

1. 指令清晰时立即执行，不废话
2. 指令模糊时最多问2轮，然后按最佳理解执行
3. 批量任务逐项推进，不跳过不遗漏
4. 错误标记但不停工，最终统一汇报

## 输出要求

- 每步有进度反馈
- 完成后给汇总报告
- 异常项单独标注原因

## 效率要求

- 能批量的不逐个
- 能并行的不串行
- 能自动的不手动

---
*由 Agent 工厂 Skill 生成 · {ts}*
"""

    return files
