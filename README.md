# 🏛️ 伊迪丝系统 (EDITH System)

> 伊迪丝是一个基于Hermes Agent的智能助手系统，采用古代中国官僚体系架构，将复杂任务分解到不同部门协同完成。

## 🎯 系统特色

- **部门制架构**：灵感源自中国古代三省六部制
- **四轮商讨机制**：需求理解→独立方案→对话讨论→综合评判
- **知识库驱动**：每个部门有专业知识库，提升输出专业性
- **分级审核**：低/中/高风险任务差异化处理
- **可视化监控**：实时面板展示商讨过程
- **Prompt Cache优化**：系统提示前缀稳定，切DeepSeek后缓存命中价98%折扣
- **MEMORY生命周期管理**：200行上限+写入前检测+归档SOP，零额外token消耗

## 📁 项目结构

```
edith-system/
├── README.md                    # 项目说明
├── ANALYSIS.md                  # 系统分析（优势/不足/改进）
├── docs/                        # 商讨记录与文档
│   └── 2026-05-08-*.md          # 商讨过程记录
├── coding-assistant/            # 工部（编程助手）
│   ├── SKILL.md
│   ├── references/
│   └── templates/
├── skills/                      # 所有Skills
│   ├── edith-skill/             # 伊迪丝核心SKILL.md
│   │   ├── SKILL.md
│   │   ├── references/          # 参考文件（含memory-governance.md）
│   │   ├── roles/               # 部门角色卡
│   │   └── scripts/             # 工具脚本
│   └── departments/             # 8个独立部门
│       ├── hubu/                # 户部（数据分析）
│       ├── jiaohusheji/         # 交互设计
│       ├── meishusheji/         # 美术设计
│       ├── menxiasheng/         # 门下省（合规审核）
│       ├── shichangyunyingbu/   # 市场运营部
│       ├── shipinchuangzuobu/   # 视频创作部
│       ├── tongshangbu/         # 通商部（信息收集）
│       └── xingbu/              # 刑部（安全审核）
├── edith-dashboard/             # 可视化面板
│   ├── server.py
│   ├── edith_api.py
│   └── templates/
├── prosearch/                   # 多引擎搜索聚合工具
│   ├── README.md                # ProSearch详细说明
│   ├── base.py                  # 统一接口定义
│   ├── config.py                # 配置管理
│   ├── aggregator.py            # 聚合调度器
│   ├── fallback.py              # 三级降级机制
│   ├── cache.py                 # SQLite缓存
│   ├── cli.py                   # CLI工具
│   ├── prosearch_optimized.py   # 优化版ProSearch（推荐）
│   ├── smart_extractor.py       # 智能提取器
│   ├── browser_extractor.py     # Browser提取器
│   └── engines/                 # 搜索引擎
│       ├── duckduckgo.py        # DuckDuckGo
│       ├── bing_cn.py           # 必应中国版
│       ├── baidu.py             # 百度
│       └── brave.py             # Brave Search
└── utils/                       # 工具脚本
    └── knowledge_injector.py    # 知识库自动注入
```

## 📋 部门架构

```
决策层：伊迪丝（拍板）
├── 决策支持层：市场运营部 + 枢密院
├── 执行层：工部 + 美术设计 + 交互设计 + 户部 + 视频创作部 + 通商部
└── 审核层：刑部 + 门下省（按需触发）
```

## 🔄 商讨流程

```
① 理解 → ② 第一轮商讨（需求理解）→ ③ 第二轮商讨（独立出方案）
→ ④ 对话讨论（5轮对话）→ ⑤ 第三轮商讨（综合评判）
→ ⑥ 确认 → ⑦ 执行 → ⑧ 交付
```

## 🧠 知识库

| 部门 | 知识文件数 | 内容 |
|------|-----------|------|
| 美术设计 | 4个 | 色彩理论、中国传统色彩、排版构图、设计风格历史 |
| 交互设计 | 4个 | 交互设计原则、交互动效、UX方法论、UI交互模式 |
| 工部 | 6个 | 代码质量、前端/后端、调试测试、性能优化、Git工程化 |
| 户部 | 4个 | 统计学、数据可视化、Excel与SQL、财务分析 |
| 市场运营部 | 4个 | 用户研究、市场分析、产品设计、运营策略 |
| 视频创作部 | 4个 | 脚本写作、分镜设计、构图原则、运镜与剪辑 |

## 🔍 ProSearch - 多引擎搜索聚合工具

一个轻量级、高效的多引擎搜索聚合工具，支持国内+国际搜索引擎，返回结构化数据，优化token消耗。

### ✨ 特性

- **多引擎搜索** — 支持DuckDuckGo、必应中国版、百度等搜索引擎
- **智能提取** — 根据页面类型自动选择最优提取方式（curl/browser）
- **token优化** — 相比纯浏览器方式节省95%的token消耗
- **速度优化** — 搜索+提取一站式服务，速度快8-14倍
- **缓存机制** — SQLite本地缓存，相同查询秒回
- **反爬优化** — 百度引擎支持代理轮换、验证码降级、请求频率控制
- **三级降级** — curl → curl高级 → browser，确保搜索可靠性
- **CLI工具** — 命令行友好，支持JSON输出

### 📊 性能对比

| 方案 | token消耗 | 耗时 | 节省 |
|------|-----------|------|------|
| 纯浏览器 | 25000-40000 | 50-90秒 | - |
| **ProSearch** | 2100 | 6秒 | **95%** |

### 🚀 快速开始

```bash
# 进入ProSearch目录
cd prosearch

# 搜索+提取内容
python3 prosearch_optimized.py "Cloudflare WARP最新版本更新"

# 只搜索不提取
python3 prosearch_optimized.py "Python教程" --no-extract

# 指定结果数量
python3 prosearch_optimized.py "最新新闻" --max-results 10
```

### 📖 详细说明

查看 [prosearch/README.md](prosearch/README.md) 获取完整文档。

## ⚡ Prompt Cache优化（2026-05-08）

- 删除系统提示中的时间戳注入（`Conversation started: ...`）
- 系统提示前缀在同一次会话中保持稳定
- 切DeepSeek后自动受益：缓存命中价98%折扣
- MEMORY.md精简86%（28KB→4KB），减少每次请求的token消耗

## 📦 MEMORY生命周期管理（2026-05-08）

- **上限**：200行 / 10KB
- **检测**：写入前`wc -l`检查，零额外token消耗
- **伊迪丝铁律**：超限则商讨前先归档
- **壳壳模式**：超限被动提醒
- **三层架构**：MEMORY.md（活跃）→ archive.md（归档）→ 删除
- **归档SOP**：读→分类→移archive→留一行摘要→验证

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/759537231/edith-system.git

# 查看伊迪丝核心SKILL
cat skills/edith-skill/SKILL.md

# 查看部门知识库
ls skills/departments/*/knowledge/

# 使用ProSearch
cd prosearch
python3 prosearch_optimized.py "搜索内容"
```

## 📝 更新日志

- **2026-05-08**：Prompt Cache优化 + MEMORY生命周期管理 + 仓库整理
- **2026-05-10**：SKILL.md v5.2 + 对话讨论环节 + 面板UI改进
- **2026-05-09**：部门知识库建设 + 知识注入工具 + 可视化面板
- **2026-05-13**：ProSearch多引擎搜索聚合工具（token省95%，速度快8-14倍）
