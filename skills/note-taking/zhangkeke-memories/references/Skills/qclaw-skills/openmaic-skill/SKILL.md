---
name: openmaic-skill
description: |
  将PDF或主题文本一键生成交互式课程。基于清华OpenMAIC项目核心逻辑封装。
  当用户说"生成课程"、"帮我把这个PDF变成课程"、"教我XXX"时触发。
metadata:
  openclaw:
    emoji: '📚'
---

# OpenMAIC Skill - 课程生成器

基于清华OpenMAIC项目的课程生成能力，封装为OpenClaw Skill。

## 功能

| 输入 | 输出 |
|------|------|
| PDF文档 | 课程大纲 + 幻灯片 |
| 主题文本 | 课程大纲 + 幻灯片 |
| 用户画像 | 个性化课程内容 |

## 使用方式

### 方式一：直接生成

```
用户: 帮我生成一个关于量子物理的课程
壳壳: 收到，正在分析需求并生成课程大纲...

[输出大纲JSON]
[输出幻灯片内容]
```

### 方式二：上传PDF

```
用户: [上传PDF] 把这个变成课程
壳壳: 正在解析PDF，已提取X个核心知识点...
      建议生成X个场景，预计时长X分钟
      目标受众是？[初学者/中级/高级]

用户: 初学者
壳壳: [生成大纲]
      确认大纲后我继续生成幻灯片，还是现在就调整？

用户: 继续
壳壳: [生成PPTX] [生成测验]
      课程已生成，下载链接：xxx.pptx
```

## 核心流程

```
┌─────────────┐
│ 用户需求/PDF │
└──────┬──────┘
       ▼
┌─────────────┐
│ 提取知识点  │
└──────┬──────┘
       ▼
┌─────────────┐
│ 生成场景大纲│ ← AI模型处理Prompt
└──────┬──────┘
       ▼
┌─────────────┐
│ 填充内容    │ ← AI模型处理Prompt
└──────┬──────┘
       ▼
┌─────────────┐
│ 导出PPTX    │ ← 复用pptx skill
└─────────────┘
```

## 文件结构

```
~/.qclaw/workspace/skills/openmaic-skill/
├── SKILL.md                    # 本文档
├── scripts/
│   └── course_generator.py     # 核心生成逻辑
└── prompts/
    ├── outline_system.md       # 大纲生成系统提示
    ├── outline_user.md         # 大纲生成用户模板
    └── slide_system.md         # 幻灯片内容系统提示
```

## Prompt模板来源

基于清华OpenMAIC项目原始Prompt模板，从GitHub获取并本地化：

| 原始文件 | 本地文件 | 用途 |
|----------|----------|------|
| `requirements-to-outlines/system.md` | `prompts/outline_system.md` | 大纲生成 |
| `requirements-to-outlines/user.md` | `prompts/outline_user.md` | 用户输入 |
| `slide-content/system.md` | `prompts/slide_system.md` | 幻灯片内容 |

## API调用方式

AI在执行此Skill时：

1. **读取Prompt模板**：调用 `course_generator.py` 的 `format_*_prompt()` 函数
2. **调用AI模型**：使用当前会话的模型路由
3. **解析响应**：`parse_outline_response()` 提取JSON
4. **对接pptx skill**：生成最终幻灯片文件

## 配置

无需额外API密钥，使用现有模型路由。

---

## ⚠️ 完整性说明（2026-05-04 审查）

**本 skill 只包含 Prompt 模板，不是完整平台。**

与原版 OpenMAIC 的差距：

| 能力 | 原版 OpenMAIC | 本 skill |
|------|--------------|---------|
| 课程大纲生成 | ✅ | ✅（Prompt模板） |
| 幻灯片内容生成 | ✅ | ✅（Prompt模板） |
| 交互式HTML场景 | ✅ | ❌ |
| PBL项目式学习 | ✅ | ❌ |
| AI图片/视频生成 | ✅ | ❌ |
| PPTX渲染导出 | ✅ | ❌（需对接pptx skill） |
| 课程播放器 | ✅ | ❌ |

**结论**：适合生成大纲+幻灯片内容的JSON结构，不适合生成完整交互式课程。

**替代方案**：原版 OpenMAIC 平台已免费开放（2026-05-04 确认），可直接使用。

## ⚠️ 与原版 OpenMAIC 的差距（2026-05-04 确认）

本 skill 只提取了 Prompt 模板，**不等于**原版 OpenMAIC 平台。

| 能力 | 本 skill | 原版 OpenMAIC |
|------|---------|--------------|
| 课程大纲生成 | ✅ JSON 结构 | ✅ |
| 幻灯片内容 | ✅ JSON 结构 | ✅ |
| PPTX 渲染导出 | ❌ 需配合 powerpoint skill | ✅ 内置 |
| 交互式 HTML 场景 | ❌ | ✅ |
| PBL 项目式学习 | ❌ | ✅ |
| AI 图片/视频生成 | ❌ | ✅ |
| 课程播放器 | ❌ | ✅ |

**原版平台**（2026-05 起免费开放）：可直接使用，不需要自己的 API。

**本 skill 适用场景**：
- 需要自定义课程生成流程
- 需要批量生成课程大纲
- 需要与其他系统集成

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v0.1.0 | 2026-04-08 | 初始版本，完成Prompt提取和Python核心逻辑 |
