# Feature Flags Skill

> 参考 Claude Code 的 `feature()` 设计，控制实验性功能的启用/禁用

## 功能说明

本 Skill 提供 Feature Flags 功能开关系统，支持：
- 运行时配置读取
- 功能启用状态检查
- 与 Claude Code 类似的 API 风格

## 配置文件位置

```
~/.qclaw/features.json
```

## 使用方法

### 1. 检查功能是否启用

```typescript
// AI 在对话中可以这样检查
import { isFeatureEnabled } from './utils/features'

if (isFeatureEnabled('PROACTIVE')) {
  // 执行主动模式逻辑
}
```

### 2. 获取所有已启用的功能

```typescript
import { getEnabledFeatures } from './utils/features'

const enabledFeatures = getEnabledFeatures()
// ['BRIEF_MODE', 'AUTO_COMPACT']
```

## 当前支持的功能

| 功能名 | 默认状态 | 说明 |
|--------|---------|------|
| `PROACTIVE` | ❌ 关闭 | 主动模式 |
| `VOICE_MODE` | ❌ 关闭 | 语音模式 |
| `COORDINATOR_MODE` | ❌ 关闭 | 多Agent协调模式 |
| `BRIEF_MODE` | ✅ 启用 | 简报模式 |
| `AUTO_COMPACT` | ✅ 启用 | 自动压缩 |
| `EXPERIMENTAL_SKILL_SEARCH` | ❌ 关闭 | 实验性Skill搜索 |
| `CONTEXT_COLLAPSE` | ❌ 关闭 | 上下文折叠 |
| `WORKFLOW_SCRIPTS` | ❌ 关闭 | 工作流脚本 |

## 触发方式

- **自动触发**：无（需要 AI 主动调用）
- **手动触发**：用户说"检查功能开关"或"哪些功能已启用"

## 注意事项

1. 配置文件不存在时，所有功能默认关闭
2. 修改配置后无需重启，下次调用自动生效
3. 环境变量 `QCLAW_FEATURES_PATH` 可覆盖配置文件路径

## 参考来源

- Claude Code v2.1.88 源码 `tools.ts` 中的 `feature()` 函数
- 设计理念：编译时裁剪 vs 运行时配置

---

*创建时间：2026-04-08*
*作者：伊迪丝 · 工部*
