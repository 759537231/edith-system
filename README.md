# 🏛️ 伊迪丝系统 (EDITH System)

> 伊迪丝是一个基于Hermes Agent的智能助手系统，采用古代中国官僚体系架构，将复杂任务分解到不同部门协同完成。

## 🎯 系统特色

- **部门制架构**：灵感源自中国古代三省六部制
- **三轮商讨机制**：需求理解→独立方案→综合评判
- **双模型协作**：小米（技术）+ LongCat（风险）
- **分级审核**：低/中/高风险任务差异化处理
- **可视化监控**：实时面板展示商讨过程

## 📁 项目结构

```
edith-system/
├── README.md                 # 项目说明
├── ANALYSIS.md              # 系统分析（优势/不足/改进）
├── coding-assistant/        # 工部（编程助手）
│   ├── SKILL.md
│   ├── references/
│   └── templates/
├── departments/             # 6个独立部门
│   ├── hubu/               # 户部（数据分析）
│   ├── jiaohusheji/        # 交互设计
│   ├── meishusheji/        # 美术设计
│   ├── menxiasheng/        # 门下省（合规审核）
│   ├── tongshangbu/        # 通商部（信息收集）
│   └── xingbu/             # 刑部（安全审核）
└── edith-dashboard/        # 可视化面板
    ├── server.py           # Flask后端
    ├── edith_api.py        # 伊迪丝API工具
    ├── templates/          # 前端模板
    └── 80s-homepage.html   # 80年代风格示例
```

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/759537231/edith-system.git
cd edith-system
```

### 2. 安装依赖
```bash
pip install flask
```

### 3. 启动可视化面板
```bash
cd edith-dashboard
python server.py
```

### 4. 访问面板
打开浏览器访问 `http://localhost:8080`

## 📊 系统对比

| 特性 | 伊迪丝 | AutoGen | CrewAI | LangGraph |
|------|--------|---------|--------|-----------|
| 部门制 | ✅ | ❌ | ❌ | ❌ |
| 三轮商讨 | ✅ | ❌ | ❌ | ❌ |
| 双模型协作 | ✅ | ❌ | ❌ | ❌ |
| 记忆分层 | ❌ | ❌ | ✅ | ❌ |
| 图状工作流 | ❌ | ❌ | ❌ | ✅ |
| 可视化面板 | ✅ | ✅ | ✅ | ✅ |

## 🙏 致谢

### 三省六部制原创作者
- **项目**：[cft0808/edict](https://github.com/cft0808/edict)
- **作者**：cft0808
- **星标**：15.7k ⭐
- **贡献**：第一个将中国古代三省六部制做成AI多代理系统的开源项目
- **意义**：为伊迪丝系统提供了核心架构灵感

### 可视化界面
- **创作者**：壳壳（Hermes Agent）
- **技术栈**：Flask + SSE + 原生HTML/CSS/JS
- **设计原则**：零依赖、轻量级、实时推送

### 主流框架参考
- **AutoGen**（微软）：团队协作模式、Human-in-the-Loop
- **CrewAI**：角色系统、记忆分层、知识注入
- **LangGraph**：图状工作流、状态管理、条件路由

## 📝 版本历史

- **v4.7** (2026-05-09) — 可视化面板完成，系统分析文档，致谢完善
- **v4.0** (2026-05-03) — 三轮商讨机制，部门精简至5+3
- **v3.0** (2026-05-02) — 整合商讨机制
- **v2.0** — 双模式分流，部门制架构
- **v1.0** — 初始版本

## 📄 许可证

MIT License

---

**创作者**：张壳壳（759537231）
**日期**：2026-05-09
