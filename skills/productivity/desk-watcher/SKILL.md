---
name: desk-watcher
description: |
  书桌监控系统。Cron定时检查~/.hermes/desk/目录，自动处理新文件和便签。
  异步协作空间的后端基础设施。
trigger_keywords:
  - "书桌监控"
  - "desk watcher"
  - "异步协作"
  - "自动处理文件"
---

# 📋 Desk Watcher — 书桌监控系统

## 概述

每5分钟由Cron调用，检查`~/.hermes/desk/`目录的新文件和便签，输出JSON供Agent处理。

## 目录结构

```
~/.hermes/desk/
├── inbox/        ← 用户放文件进来
├── outbox/       ← 处理结果放这里
├── notes/        ← 便签，Agent主动读取执行
├── processed/    ← 处理完的原文件移到这里
├── logs/         ← 处理日志
└── .desk.lock    ← 文件锁（防重复处理）
```

## 脚本

`~/.hermes/scripts/desk_watcher.py` — 主监控脚本

**功能**：
- 扫描inbox目录的新文件（支持 .txt/.csv/.xlsx/.md/.json）
- 扫描notes目录的便签（.txt格式）
- 文件锁防重复处理（fcntl）
- 输出JSON到stdout供Cron job读取
- 日志写入 ~/.hermes/desk/logs/{日期}.log

**便签格式**：
```
提醒：明天下午3点给媳妇转账
```
第一行是指令类型（提醒/任务/备忘），冒号后是内容。

## Cron Job

- Job ID: `36cfa831973a`
- 名称: 书桌监控
- 频率: every 5m, forever
- 脚本: desk_watcher.py
- 行为: 有新内容→处理+飞书通知，无内容→静默

## 使用方式

1. **放文件**: 把txt/csv/xlsx文件扔进 `~/.hermes/desk/inbox/`
2. **写便签**: 在 `~/.hermes/desk/notes/` 里新建txt
3. **看结果**: `~/.hermes/desk/outbox/`，飞书也会收到通知

## ⚠️ 坑：工作目录问题

如果working directory是已删除的目录（如qimen_app），terminal和search_files会报错。

**解决**: 用 `execute_code` + Python的 `os`/`subprocess` 代替terminal命令。

## 前端：书桌桌面应用

书桌系统有两个部分：
- **后端**：`desk_watcher.py` + Cron（自动监控+处理）
- **前端**：Electron桌面应用（用户交互界面）

**桌面应用位置**：`~/Desktop/desk-app/release/mac-arm64/书桌.app`

**技术栈**：Electron + React + Vite（详见 `electron-react-vite-app` skill）

**功能**：
- 📥 收件箱 / 📤 发件箱 / 📝 便签 — 侧栏导航
- 💬 对话 — 直接在应用内和Hermes Agent对话
- 🤖 规则引擎 — 三层架构自动处理（见下文）
- 📁 文件上传（Cmd+O）
- 📝 新建便签（Cmd+N）
- 📋 文件预览（文本内容）
- 🎨 深色主题、macOS原生标题栏

**对话功能**：通过 `hermes chat -q "消息" -Q` CLI调用，在Electron主进程中spawn子进程。

**启动方式**：
```bash
open ~/Desktop/desk-app/release/mac-arm64/书桌.app
# 或开发模式（有热更新）
cd ~/Desktop/desk-app && npm run electron:dev
```

## 规则引擎三层架构

**核心文件**：
- `src/main/rule-engine.js` — 规则引擎核心
- `src/main/history-manager.js` — 历史记录和习惯分析

**处理流程**：inbox文件 → chokidar检测 → 类型分类 → 意图识别 → AI分析 → 记录历史 → 结果写入outbox → 原文件移到processed

### 第一层：文件类型检测

自动识别：spreadsheet、image、document、code、data

### 第二层：意图识别 + AI分析

8种意图模式（财务💰、简历👤、合同📋、报告📊、代码审查🐛、数据分析📈、学习笔记📚、会议纪要🤝）

- 关键词计数匹配，confidence = min(matchCount/3, 1)
- ≥0.3触发AI分析（调用hermes CLI）
- 根据意图选择不同prompt

### 第三层：历史记录 + 习惯学习

**存储**：`~/.hermes/desk/history.json`

**分析维度**：
- 文件名高频词 → 识别命名习惯
- 意图分布 → 识别处理偏好
- 时间模式 → 识别时间段偏好

**输出**：统计信息（总处理数、意图分布）+ 习惯建议

## ⚠️ 常见问题

1. **chokidar不工作** → 检查`ignored`正则，用`/(^|[\/\\])\.[^\/\\]+$/`而非`/(^|[\/\\])\./`
2. **打包后代码不更新** → 必须`npm run build && npm run pack`
3. **console.log不可见** → 用`fs.appendFileSync`写日志文件
4. **工作目录报错** → 用`execute_code`代替`terminal`
