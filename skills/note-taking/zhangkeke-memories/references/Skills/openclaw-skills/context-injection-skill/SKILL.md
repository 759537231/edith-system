# Context Injection Skill

> 参考 Claude Code 的 `getUserContext`/`getSystemContext` 设计
> 自动注入 Git 状态、当前日期等信息

## 功能说明

本 Skill 提供上下文自动注入功能，包括：
- 当前日期和时间
- Git 仓库状态
- 时区信息
- MEMORY.md 文件引用

## 使用方法

### 1. 快速日期注入（推荐）

```typescript
import { getCurrentDateContext } from './utils/context'

const dateText = getCurrentDateContext()
// "今天是 2026-04-08，当前时间 10:45，时区 Asia/Shanghai"
```

### 2. 完整上下文注入

```typescript
import { buildContextInjection } from './utils/context'

const contextText = await buildContextInjection()
// 包含：日期、时间、Git状态、MEMORY.md引用
```

### 3. 分别获取

```typescript
import { getSystemContext, getUserContext } from './utils/context'

// 系统上下文
const systemCtx = await getSystemContext()
console.log(systemCtx.currentDate) // "今天是 2026-04-08"
console.log(systemCtx.gitStatus)   // { branch: 'main', status: '(clean)', ... }

// 用户上下文
const userCtx = await getUserContext()
console.log(userCtx.memoryMd)      // MEMORY.md 文件内容
```

## 注入内容示例

```
## 系统信息

今天是 2026-04-08，当前时间 10:45，时区 Asia/Shanghai

## Git 状态

当前分支: main
主分支: main
Git 用户: 张三
状态:
M src/utils/context.ts
?? docs/CONTEXT_INJECTION.md

最近提交:
abc123 feat: 添加上下文自动注入
def456 fix: 修复日期格式

## 项目记忆

见 MEMORY.md 文件内容
```

## 触发方式

- **自动触发**：对话开始时 AI 主动调用
- **手动触发**：用户说"注入上下文"或"当前环境信息"

## 注意事项

1. 非 Git 目录会跳过 Git 状态
2. MEMORY.md 不存在时会跳过
3. 远程环境（CI/CD）可通过环境变量 `QCLAW_SKIP_GIT=true` 跳过 Git 状态

## 参考来源

- Claude Code v2.1.88 源码 `context.ts`
- 设计理念：自动注入，减少用户手动维护负担

---

*创建时间：2026-04-08*
*作者：伊迪丝 · 工部*
