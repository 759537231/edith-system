## 任务背景
通商部受命查询 Hermes Agent 独立版的官方信息，涵盖安装方式、端口配置、macOS 支持及与 OpenClaw 的集成关系。

## 执行过程
1. 识别 web_search 不可用，改用 online-search skill 执行搜索
2. 搜索 Hermes Agent GitHub 仓库、安装脚本、官方文档
3. 补充搜索端口配置和 macOS 相关内容
4. 整合信息后以通商部口吻输出，生成 artifact 文件

## 关键结果
- 官方一键安装：`curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`
- Web UI 默认端口 localhost:7860，配置在 `~/.hermes/config.yaml`
- macOS 原生支持，含 BlueBubbles iMessage 桥接
- 与 OpenClaw 通过 `hermes claw migrate` 迁移命令衔接
- 生成文件：`task-summary_2026-05-02_hermes-agent-intel.md`

## 结论建议
情报收集完毕，已归档。建议下一步评估 Hermes 与现有 OpenClaw 环境的共存策略及迁移优先级。