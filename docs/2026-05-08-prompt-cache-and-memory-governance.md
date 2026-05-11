# 商讨记录：Prompt Cache优化 + MEMORY生命周期管理

> 日期：2026-05-08
> 伊迪丝版本：v5.2
> 模式：四轮商讨（含对话讨论）

---

## 任务一：Prompt Cache命中优化

### 第一轮：需求理解

**真实意图**：降低LLM API调用的token消耗，通过提升prompt cache命中率和减少重复传输的token量实现成本优化

**验收标准**：
- 系统提示前缀在同一次会话中保持一致
- 针对DeepSeek的自动前缀匹配机制优化
- 改动量小（<50行代码），不影响现有功能

**约束**：
- MiMo不支持prompt caching，只能做应用层优化
- 6月1日MiMo到期，优化主要为切DeepSeek做准备

**风险**：时间戳删除可能影响调试信息 → 本地文件名已记录时间，不影响

### 第二轮：独立方案

**小米方案**（4步）：定位→删除→精简MEMORY→验证
**LongCat方案**（6步）：备份→定位→扫描全部动态注入→精简（保守）→端到端测试→文档记录

### 对话讨论（5轮）

**共识**：
- 备份用git diff替代cp
- 扫描所有动态注入点（不只时间戳）
- MEMORY精简列清单+删除理由+archive备份
- SOUL.md只给建议不动
- diff验证前缀一致性

**分歧**：无

### 第三轮：综合评判

**最终方案**（6步）：
1. grep定位时间戳注入代码，确认无依赖
2. 扫描系统提示构建流程，找出所有动态注入点
3. 删除时间戳注入代码
4. 精简MEMORY.md（列清单+archive）
5. diff验证前缀一致性
6. 记录优化结果到memory

### 执行结果

| 步骤 | 结果 | 详情 |
|------|------|------|
| 1. grep定位 | ✅ | `run_agent.py:5259`，无其他代码依赖 |
| 2. 动态注入扫描 | ✅ | 唯一动态项：时间戳（每次请求变）；Session ID/Model/Provider会话内不变 |
| 3. 删除时间戳 | ✅ | 改用meta_parts保留Session ID/Model/Provider，语法检查通过 |
| 4. MEMORY精简 | ✅ | 28KB→4KB（-86%），17条移入archive.md |
| 5. diff验证 | ✅ | 时间戳无残留，元数据代码正确 |
| 6. 记录结果 | ✅ | memory已更新 |

**关键代码变更**：
```python
# 删除前
from hermes_time import now as _hermes_now
now = _hermes_now()
timestamp_line = f"Conversation started: {now.strftime('%A, %B %d, %Y %I:%M %p')}"
# ... append to prompt_parts

# 删除后
meta_parts = []
if self.pass_session_id and self.session_id:
    meta_parts.append(f"Session ID: {self.session_id}")
if self.model:
    meta_parts.append(f"Model: {self.model}")
if self.provider:
    meta_parts.append(f"Provider: {self.provider}")
if meta_parts:
    prompt_parts.append("\n".join(meta_parts))
```

**预期收益**：切DeepSeek后，系统提示前缀稳定，缓存命中价98%折扣。

---

## 任务二：MEMORY.md生命周期管理

### 第一轮：需求理解

**真实意图**：建立低成本/零成本的MEMORY.md生命周期管理机制，防止膨胀导致每次请求浪费token

**约束**：
- 不能用heartbeat（消耗token）
- 不能增加用户操作负担
- MiMo额度有限，不能浪费在维护任务上

### 第二轮：独立方案

**小米方案**：写入时治理（行为习惯+日期标签）
**LongCat方案**：分层存储+shell脚本检测+cron提醒

### 对话讨论（5轮）

**共识**：
- 200行/10KB上限
- 写入前`wc -l`检测（不消耗token）
- 伊迪丝铁律：超限则商讨前先归档
- 壳壳模式：超限被动提醒
- 每条记忆末尾标创建日期
- MEMORY.md只存一行摘要，详情在archive
- 不搞cron/heartbeat，零额外消耗
- 归档SOP标准化

**分歧**：无

### 第三轮：综合评判

**最终方案**（4步）：
1. MEMORY.md顶部加大小上限注释
2. 伊迪丝SKILL.md加铁律+壳壳提醒
3. 建立归档SOP写入SKILL.md
4. MEMORY.md现有条目统一加创建日期

### 执行结果

| 步骤 | 结果 | 详情 |
|------|------|------|
| 1. 大小上限注释 | ✅ | MEMORY.md顶部加200行/10KB上限+格式规范 |
| 2. 伊迪丝铁律 | ✅ | 硬规则第6条+references/memory-governance.md |
| 3. 归档SOP | ✅ | 三层架构：MEMORY.md→archive.md→删除 |
| 4. 创建日期 | ✅ | 所有条目统一加(创建:YYYY-MM-DD) |

**伊迪丝铁律**：
> 写入memory前必须先检查MEMORY.md行数（`wc -l`），超过200行先归档再写入。

---

## 仓库整理

| 操作 | 详情 |
|------|------|
| 同步edith-skill | 新增memory-governance.md参考文件 |
| 删除重复departments/ | 保留skills/departments/ |
| 删除重复dashboard/ | 保留edith-dashboard/ |
| 删除重复edith-skill.md | 保留skills/edith-skill/目录 |
| 删除pptx schemas | 954KB XSD文件，不需要 |

---

## 总结

两个任务共10个步骤，全部完成。零额外token消耗，结构性治理机制已建立。

**关键成果**：
1. Prompt cache优化：时间戳删除+MEMORY精简86%，切DeepSeek后自动受益
2. MEMORY生命周期：200行上限+写入前检测+伊迪丝铁律+归档SOP
3. 仓库整理：去重+清理，结构更清晰
