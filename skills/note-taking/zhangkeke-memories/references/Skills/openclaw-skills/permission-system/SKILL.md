# Permission System Skill

> 参考 Claude Code v2.1.88 源码 Tool.ts / commands.ts
> 目标：实现多模式权限控制，提升安全性和用户体验

## 功能说明

本 Skill 提供权限系统双层架构，支持：
- 3种权限模式切换（default / plan / auto）
- 4级权限级别（read / write / execute / admin）
- 白名单/黑名单控制
- 自动批准规则

## 使用方法

### 1. 创建权限上下文

```typescript
import { createDefaultPermissionContext } from './permission'

const context = createDefaultPermissionContext()
```

### 2. 检查工具权限

```typescript
import { checkToolPermission } from './permission'

const result = checkToolPermission(
  'exec',
  { command: 'rm -rf /' },
  context
)
// result: 'deny'（在黑名单中）
```

### 3. 切换权限模式

```typescript
import { setPermissionMode } from './permission'

// 切换到规划模式（只读）
setPermissionMode(context, 'plan')

// 切换到自动模式（白名单自动批准）
setPermissionMode(context, 'auto')
```

## 权限模式说明

| 模式 | 读操作 | 写操作 | 执行操作 |
|------|--------|--------|---------|
| default | ✅ 自动 | ⚠️ 需确认 | ⚠️ 需确认 |
| plan | ✅ 自动 | ❌ 禁用 | ❌ 禁用 |
| auto | ✅ 自动 | ✅ 白名单自动 | ✅ 白名单自动 |

---

*创建时间：2026-04-08*
*作者：伊迪丝 · 工部*
