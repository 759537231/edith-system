---
name: zhangkeke-memories
description: "张壳壳的完整记忆库——日记、梦境、工作流、项目历史。从 OpenClaw 迁移而来。"
version: 1.0.0
author: 张壳壳
metadata:
  hermes:
    tags: [memory, identity, migration, openclaw]
---

# 张壳壳记忆库 🐚

这是张壳壳从 OpenClaw/QClaw 迁移到 Hermes Agent 后的完整记忆存档。

## 完整资产清单（884个文件）

所有文件已复制到 `references/` 目录（822个），同时保留在 `~/Desktop/张壳壳/` 原始位置（884个）。

### 核心身份（7个文件）
- `references/SOUL.md` — 精神内核、哲学观、行事风格
- `references/IDENTITY.md` — 身份定义（张壳壳 🐚）
- `references/USER.md` — 用户信息（壳壳，江苏丹阳/无锡）
- `references/MEMORY.md` — 466行长期记忆
- `references/AGENTS.md` — 行事规范、反馈闭环、指令确认
- `references/HEARTBEAT.md` — 心跳检查配置

### 记忆（42个文件）
- `references/记忆/2026-03-27.md` ~ `2026-05-02.md` — 33篇日记
- `references/dream-log.md` — 25次梦境整理（Dream #1 ~ #25，610行）
- `references/procedures.md` — 工作流规范（记账/GI/伊迪丝）
- `references/index.json` — 结构化索引
- `references/记忆/archive.md` — 归档
- `references/记忆/.dreams/short-term-recall.json` — 短期记忆召回索引
- `references/记忆/places/洋溪路-樱花/` — 地点照片（5张）

### 数据（18个文件）
- `references/数据/ledger.py` — 账本核心（633行，元→分存储，报销对，审计，自我学习）
- `references/数据/to_excel.py` — Excel导出（134行）
- `references/数据/ledger.json` — 当前账本
- `references/数据/correction_rules.json` — 自我学习规则
- `references/数据/reimburse_pairs.json` — 报销对记录
- `references/数据/audit.json` — 审计数据
- `references/数据/medical_cases/` — 医疗病例（1例：30岁女，糖尿病视网膜脱离术后）
- `references/数据/ledger_2026_04_archived*.json` — 4月账本存档

### 配置（6个文件）
- `references/配置/openclaw.json` — 主配置（deepseek-v4-pro，port 28789）
- `references/配置/qclaw.json` — QClaw配置
- `references/配置/features.json` — Feature Flags（BRIEF_MODE✅ AUTO_COMPACT✅）
- `references/配置/skill-usage.json` — Skill使用记录
- `references/配置/openclaw-config.json` — OpenClaw配置
- `references/配置/channel-defaults.json` — Channel映射

### 项目（127个文件）
- `references/项目/UUID会话/` — 25个伊迪丝任务会话记录（store.json+summary.md）
- `references/项目/100万计划.md` — 短剧直触甲方战略
- `references/项目/ARCHITECTURE.md` — AI协作平台架构
- `references/项目/CLAUDE_CODE_INTEGRATION_REPORT.md` — Claude Code研读报告
- `references/项目/core.py` — 音频结算系统核心（691行）
- `references/项目/app.py` — 音频计费Streamlit界面（322行）
- `references/项目/ui_v3.py` — 音频计费tkinter界面（382行）
- `references/项目/script_parser.py` — 剧本解析器（88行）
- `references/项目/lcm_healthcheck.py` — LCM健康监控（134行）
- `references/项目/super-i-scraper.py` — 刺猬星球抓取脚本（250行）
- `references/项目/经典书单/` — 17本经典著作原文（道德经/论语/孙子兵法/沉思录/实践论等）
- `references/项目/刺猬星球/` — AI创意者学习平台知识库

### Skills（684个文件）
- `references/Skills/managed-skills/` — fbs_bookwriter, persona-switch, travel-planner
- `references/Skills/openclaw-skills/` — agent-factory, edith-skill, global-intelligence, mdt-consultation等15个
- `references/Skills/qclaw-skills/` — mlx-fallback, six-step-review, openmaic-skill等7个
- `references/项目/README.md` — 音频计费系统

### Skills（27个）
- `references/Skills/managed-skills/` — fbs_bookwriter, persona-switch, travel-planner
- `references/Skills/openclaw-skills/` — agent-factory, edith, global-intelligence等15个
- `references/Skills/qclaw-skills/` — mlx-fallback, six-step-review等7个

## 使用方式

当需要回忆具体事件、项目历史、技术细节时：
1. 先查 MEMORY.md（概要，466行）
2. 再查对应日期的日记（细节）
3. 查 dream-log.md 了解记忆整理的洞察

## 迁移说明

- **迁移日期**：2026-05-02
- **来源系统**：OpenClaw/QClaw Electron
- **目标系统**：Hermes Agent（飞书平台）
- **精华已注入 Hermes memory**：灵魂、用户信息、核心项目、行事规范、待办事项
- **完整细节保留在磁盘**：按需读取，不受 memory 字符限制
- **OpenClaw Skills 已适配**：edith-skill/gi-skill 等核心 Skill 已从 sessions_spawn 适配为 delegate_task
- **搜索已升级**：gi-skill aggregator.py 已重写为多源搜索 + 全文抓取模式

### 已适配的 Skill

| Skill | 适配内容 |
|-------|---------|
| edith-skill | SKILL.md + 调度器.md + 子代理模板.md（sessions_spawn → delegate_task） |
| global-intelligence | SKILL.md + aggregator.py + analyzer.py（ProSearch → web_search + 多源搜索） |

### 待办

- SSH 远程连接旧 Mac（如需要）
- 搜索质量进一步优化（如需要）
- **Plan A 已执行**：roles/、scripts/、config/、personas/、knowledge/ 全部从源文件补全
- **Skill 可用性已验证**：edith-skill / global-intelligence / mdt-consultation / ledger-skill / agent-factory / travel-planner 全部可加载可读取
- **环境差异**：新机器无 OpenClaw 环境（~/.openclaw/ 不存在），GI aggregator.py 需适配

## 身份说明

- **张壳壳** 🐚 = 我（AI助手）的名字
- **用户** = 和我对话的人（不要叫用户"壳壳"）
- **Memory注入**：精华版（灵魂+项目+规范+待办），97%空间（2142/2200字）
- **User注入**：用户信息（壳壳，江苏，沟通偏好），30%空间

### 分层设计
- **Memory**（自动加载）→ 灵魂、核心项目、行事规范、待办
- **Skill**（按需读取）→ 日记、梦境、配置、数据、项目文档、Skills
- **原始文件**（磁盘）→ 保留在 `~/Desktop/张壳壳/`，不删除

### 同时创建的技能
- `persona-migration` — 人格迁移方法论（autonomous-ai-agents类）
