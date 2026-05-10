# Streaming Query Skill

> 参考 Claude Code v2.1.88 源码 query.ts / QueryEngine.ts  
> 目标：实现流式输出，实时显示模型思考过程

## 功能说明

本 Skill 提供流式查询引擎，支持：
- AsyncGenerator 流式输出
- 实时文本和思考过程显示
- 工具调用和结果处理
- 中断和错误处理

## 使用方法

### 1. 流式查询

```typescript
import { queryStream, StreamMessage } from './streaming'

// 创建流式查询
const stream = queryStream(prompt, callAPI, options)

// 逐条处理消息
for await (const msg of stream) {
  switch (msg.type) {
    case 'text':
      console.log('文本:', msg.delta)
      break
    case 'thinking':
      console.log('思考:', msg.delta)
      break
    case 'tool_call':
      console.log('工具:', msg.tool)
      break
    case 'done':
      console.log('完成')
      break
  }
}
```

### 2. 使用 StreamRenderer

```typescript
import { StreamRenderer, queryStream } from './streaming'

const renderer = new StreamRenderer()

// 设置回调
renderer.setCallbacks({
  onText: (text) => console.log('文本更新:', text),
  onThinking: (thinking) => console.log('思考:', thinking),
  onToolCall: (tool, input) => console.log('工具调用:', tool),
  onDone: () => console.log('完成')
})

// 处理流
for await (const msg of queryStream(prompt, callAPI)) {
  renderer.handleMessage(msg)
}

// 获取完整文本
const fullText = renderer.getFullText()
```

### 3. 同步查询（兼容旧代码）

```typescript
import { query } from './streaming'

const response = await query(prompt, callAPI, options)
console.log(response)
```

### 4. 中断支持

```typescript
const controller = new AbortController()

// 启动查询
const stream = queryStream(prompt, callAPI, {
  signal: controller.signal
})

// 用户中断
controller.abort()
```

## 消息类型

| 类型 | 说明 | 字段 |
|------|------|------|
| `text` | 文本片段 | `delta` |
| `thinking` | 思考片段 | `delta` |
| `tool_call` | 工具调用开始 | `tool`, `input` |
| `tool_result` | 工具调用结果 | `result` |
| `error` | 错误 | `error` |
| `done` | 完成 | - |

## 预期收益

| 维度 | 收益 |
|------|------|
| **用户体验** | ⭐⭐⭐ 高 - 实时反馈 |
| **响应速度** | ⭐⭐⭐ 高 - 首字节时间大幅缩短 |
| **可控性** | ⭐⭐ 中 - 支持中断 |

## 注意事项

1. 需要底层 API 支持流式输出
2. 前端需要支持增量渲染
3. 中断后无法恢复（需要重新查询）

---

*创建时间：2026-04-08*
*作者：伊迪丝 · 工部*
