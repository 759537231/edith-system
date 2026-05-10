# Global Intelligence v1.0 + 伊迪丝隔离架构

## 时间
2026-04-18 00:00 ~ 07:30

## 目标
Global Intelligence Skill 从 v0.3 升级到 v1.0 + 伊迪丝系统加入上下文隔离机制

## 完成清单

### Global Intelligence v1.0
1. ✅ analyzer.py 重构：517行→280行，移除MLX调用，改为纯prompt构建器+解析器
2. ✅ aggregator.py 重写：去掉无效RSS（国内不通），关键词自动扩展，标题+URL双重去重
3. ✅ reporter.py 修复：章节编号修正（二三四→三四五），自动去重（同主题当天只留最新）
4. ✅ 历史报告清理：3份测试产物移废纸篓（中美AI竞争×3）
5. ✅ SKILL.md 重写v1.0：QClaw Only + 隔离架构文档
6. ✅ MEMORY.md 同步
7. ✅ Atlas × QClaw 验证通过：14秒，输出质量极高

### 伊迪丝隔离架构
8. ✅ SKILL.md 新增「上下文隔离机制」章节：
   - 何时隔离（3+部门 / 多轮LLM推理 / 大量数据回流）
   - 何时不隔离（单部门 / 轻量任务 / 用户要求看过程）
   - 隔离调度员模板（sessions_spawn 单调度员）
   - 成本对比表（串行/并行/隔离调度员）

## 架构决策

### QClaw Only（MLX彻底移除）
- 用户明确：「不考虑所有本地模型方案，只考虑接入QClaw」
- QClaw没有开放API，sessions_spawn是唯一调用方式
- Python脚本（analyzer/aggregator）只做数据准备，不做推理
- 实际推理全部由AI agent通过sessions_spawn驱动

### 隔离架构（防记忆污染）
- 用户提出：「这个不会记忆污染吗」→ 是的
- 解决方案：spawn 1个隔离调度员，内部消化所有中间结果
- 主会话只收到最终报告（~100 tokens vs 原来~5000 tokens）
- 用户选择方案A：伊迪丝内部也加隔离机制

### 记忆污染问题
- sessions_spawn(mode="run") 子智能体是隔离的 ✅
- 但结果回流主会话时会污染上下文 ⚠️
- 隔离调度员 = 把污染限定在临时子智能体内，不回流

## 剩余待办
1. 向量嵌入（需DashScope API Key）
2. PDF模板化（低优先级）
3. 端到端隔离流程验证（用调度员跑一次完整8维分析）
