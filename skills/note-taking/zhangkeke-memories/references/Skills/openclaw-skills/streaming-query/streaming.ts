/**
 * QClaw 流式查询引擎
 * 参考 Claude Code v2.1.88 源码 query.ts / QueryEngine.ts
 */

import { Readable } from 'stream'

/**
 * 流式消息类型
 */
export type StreamMessage =
  | { type: 'text'; delta: string }
  | { type: 'thinking'; delta: string }
  | { type: 'tool_call'; tool: string; input?: any }
  | { type: 'tool_result'; result: any }
  | { type: 'error'; error: string }
  | { type: 'done' }

/**
 * 查询选项
 */
export interface QueryOptions {
  systemPrompt?: string
  temperature?: number
  maxTokens?: number
  signal?: AbortSignal
}

/**
 * API 响应块
 */
interface APIChunk {
  choices?: Array<{
    delta?: {
      content?: string
      reasoning_content?: string
      tool_calls?: Array<{
        function?: {
          name?: string
          arguments?: string
        }
      }>
    }
    finish_reason?: string
  }>
}

/**
 * 流式查询
 */
export async function* queryStream(
  prompt: string,
  callAPI: (request: any) => Promise<Readable>,
  options?: QueryOptions
): AsyncGenerator<StreamMessage> {
  
  // 构建请求
  const request = {
    model: 'modelroute',
    messages: [
      ...(options?.systemPrompt ? [{ role: 'system', content: options.systemPrompt }] : []),
      { role: 'user', content: prompt }
    ],
    stream: true,
    temperature: options?.temperature ?? 0.7,
    max_tokens: options?.maxTokens ?? 4096
  }
  
  try {
    // 调用 API
    const stream = await callAPI(request)
    
    // 解析流
    let buffer = ''
    
    for await (const chunk of stream) {
      // 检查是否被中断
      if (options?.signal?.aborted) {
        yield { type: 'error', error: 'Request aborted' }
        return
      }
      
      buffer += chunk.toString()
      
      // 按行解析 SSE
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          
          // 结束标记
          if (data === '[DONE]') {
            yield { type: 'done' }
            return
          }
          
          try {
            const json: APIChunk = JSON.parse(data)
            const message = parseChunk(json)
            
            if (message) {
              yield message
            }
          } catch {
            // 忽略解析错误
          }
        }
      }
    }
    
    yield { type: 'done' }
    
  } catch (error) {
    yield {
      type: 'error',
      error: error instanceof Error ? error.message : 'Unknown error'
    }
  }
}

/**
 * 解析 API 响应块
 */
function parseChunk(chunk: APIChunk): StreamMessage | null {
  const choice = chunk.choices?.[0]
  
  if (!choice) return null
  
  // 完成
  if (choice.finish_reason) {
    return { type: 'done' }
  }
  
  const delta = choice.delta
  
  if (!delta) return null
  
  // 思考过程
  if (delta.reasoning_content) {
    return {
      type: 'thinking',
      delta: delta.reasoning_content
    }
  }
  
  // 文本内容
  if (delta.content) {
    return {
      type: 'text',
      delta: delta.content
    }
  }
  
  // 工具调用
  if (delta.tool_calls && delta.tool_calls.length > 0) {
    const toolCall = delta.tool_calls[0]
    return {
      type: 'tool_call',
      tool: toolCall.function?.name || 'unknown',
      input: toolCall.function?.arguments
        ? JSON.parse(toolCall.function.arguments)
        : undefined
    }
  }
  
  return null
}

/**
 * 流式渲染器
 */
export class StreamRenderer {
  private textBuffer: string = ''
  private thinkingBuffer: string = ''
  private onText?: (text: string) => void
  private onThinking?: (thinking: string) => void
  private onToolCall?: (tool: string, input?: any) => void
  private onToolResult?: (result: any) => void
  private onError?: (error: string) => void
  private onDone?: () => void
  
  /**
   * 设置回调
   */
  setCallbacks(callbacks: {
    onText?: (text: string) => void
    onThinking?: (thinking: string) => void
    onToolCall?: (tool: string, input?: any) => void
    onToolResult?: (result: any) => void
    onError?: (error: string) => void
    onDone?: () => void
  }): void {
    this.onText = callbacks.onText
    this.onThinking = callbacks.onThinking
    this.onToolCall = callbacks.onToolCall
    this.onToolResult = callbacks.onToolResult
    this.onError = callbacks.onError
    this.onDone = callbacks.onDone
  }
  
  /**
   * 处理消息
   */
  handleMessage(msg: StreamMessage): void {
    switch (msg.type) {
      case 'text':
        this.textBuffer += msg.delta
        this.onText?.(this.textBuffer)
        break
        
      case 'thinking':
        this.thinkingBuffer += msg.delta
        this.onThinking?.(this.thinkingBuffer)
        break
        
      case 'tool_call':
        this.onToolCall?.(msg.tool, msg.input)
        break
        
      case 'tool_result':
        this.onToolResult?.(msg.result)
        break
        
      case 'error':
        this.onError?.(msg.error)
        break
        
      case 'done':
        this.onDone?.()
        break
    }
  }
  
  /**
   * 获取完整文本
   */
  getFullText(): string {
    return this.textBuffer
  }
  
  /**
   * 获取完整思考过程
   */
  getFullThinking(): string {
    return this.thinkingBuffer
  }
  
  /**
   * 重置
   */
  reset(): void {
    this.textBuffer = ''
    this.thinkingBuffer = ''
  }
}

/**
 * 同步查询（兼容旧代码）
 */
export async function query(
  prompt: string,
  callAPI: (request: any) => Promise<Readable>,
  options?: QueryOptions
): Promise<string> {
  const messages: StreamMessage[] = []
  
  for await (const msg of queryStream(prompt, callAPI, options)) {
    messages.push(msg)
  }
  
  // 合并所有文本
  return messages
    .filter(m => m.type === 'text')
    .map(m => m.delta)
    .join('')
}
