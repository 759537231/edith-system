# 伊迪丝系统 (EDITH System)

> **"像一个饱读诗书的人那样思考"**

伊迪丝是一个基于Hermes Agent的智能助手系统，采用古代中国官僚体系架构，将复杂任务分解到不同部门协同完成。

## 🏛️ 系统架构

伊迪丝采用 **部门制** 架构，每个部门专注于特定领域：

### 核心部门

| 部门 | 职责 | 触发词 |
|------|------|--------|
| **枢密院** | 战略规划、任务调度 | 规划、策略、架构 |
| **工部** (coding-assistant) | 代码实现、调试、测试 | 编程、代码、开发、bug |
| **通商部** | 联网搜索、API调用、信息收集 | 搜索、查询、获取 |
| **户部** | 数据核算、报表、统计 | 数据、统计、分析 |
| **刑部** | 安全审核、权限校验 | 安全、权限、审核 |
| **门下省** | 合规审核、对外输出审核 | 合规、审核、输出 |
| **美术设计** | 视觉设计、UI设计 | 设计、美术、视觉 |
| **交互设计** | 交互逻辑、用户体验 | 交互、体验、流程 |

## 🔄 工作流程

```
用户请求 → 伊迪丝(调度) → 部门执行 → 质量把控 → 交付
```

1. **任务接收**：理解用户意图
2. **任务拆分**：分解为可执行的子任务
3. **部门调度**：分配给对应部门
4. **执行监控**：跟踪任务进度
5. **质量把控**：伊迪丝保留最终决定权
6. **经验同步**：查漏补缺，持续优化

## 📁 项目结构

```
edith-system/
├── departments/          # 部门skills
│   ├── meishusheji/     # 美术设计
│   ├── menxiasheng/     # 门下省
│   ├── jiaohusheji/     # 交互设计
│   ├── hubu/            # 户部
│   ├── tongshangbu/     # 通商部
│   └── xingbu/          # 刑部
├── coding-assistant/    # 工部 - 编程助手
│   ├── SKILL.md        # 技能定义
│   ├── references/     # 参考文档
│   └── templates/      # 模板文件
└── README.md           # 本文件
```

## 🚀 快速开始

### 前置要求

- [Hermes Agent](https://github.com/nickspaargaren/hermes-agent) 已安装
- macOS / Linux / Windows (WSL)

### 安装

```bash
# 克隆仓库
git clone https://github.com/759537231/edith-system.git

# 将skills复制到Hermes目录
cp -R edith-system/departments ~/.hermes/skills/
cp -R edith-system/coding-assistant ~/.hermes/skills/software-development/
```

### 使用

在Hermes中触发伊迪丝：

```
唤醒伊迪丝
```

或直接请求特定部门服务：

```
帮我写一个Python脚本  # → 工部
搜索最新的AI论文      # → 通商部
分析这份销售数据      # → 户部
```

## 🎯 设计原则

1. **专业分工**：每个部门只做自己擅长的事
2. **质量把控**：伊迪丝保留最终决定权
3. **经验沉淀**：查漏补缺，不重复记录
4. **简洁高效**：能用一句说清的，不用三句

## 📚 文档

- [伊迪丝核心SKILL.md](departments/README.md) - 部门详细说明
- [工部使用指南](coding-assistant/SKILL.md) - 编程助手文档
- [Hermes Agent文档](https://github.com/nickspaargaren/hermes-agent)

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [Hermes Agent](https://github.com/nickspaargaren/hermes-agent) - 底层框架
- 古代中国官僚体系 - 架构灵感来源

---

> **"为而不争，功成不居"** — 伊迪丝系统的核心理念
