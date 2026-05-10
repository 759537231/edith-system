/**
 * QClaw 权限系统
 * 参考 Claude Code v2.1.88 源码 Tool.ts / commands.ts
 */

/**
 * 权限模式
 */
export type PermissionMode = 'default' | 'plan' | 'auto'

/**
 * 工具权限级别
 */
export type ToolPermissionLevel = 'read' | 'write' | 'execute' | 'admin'

/**
 * 权限检查结果
 */
export type PermissionResult = 'allow' | 'deny' | 'confirm'

/**
 * 自动批准规则
 */
export interface AlwaysAllowRules {
  commands: string[]  // 自动批准的命令模式（支持通配符）
  files: string[]     // 自动批准的文件路径模式
}

/**
 * 工具权限上下文
 */
export interface ToolPermissionContext {
  mode: PermissionMode
  allowedTools: Set<string>
  deniedTools: Set<string>
  alwaysAllowRules: AlwaysAllowRules
  toolLevels: Map<string, ToolPermissionLevel>
}

/**
 * 默认权限上下文
 */
export function createDefaultPermissionContext(): ToolPermissionContext {
  return {
    mode: 'default',
    allowedTools: new Set(),
    deniedTools: new Set([
      'exec:rm -rf',
      'exec:format',
      'exec:mkfs',
      'exec:dd if='
    ]),
    alwaysAllowRules: {
      commands: [
        'git status',
        'git log',
        'git diff',
        'git branch',
        'ls',
        'cat',
        'echo',
        'pwd',
        'which',
        'node --version',
        'python --version'
      ],
      files: [
        '~/.qclaw/*',
        '~/.openclaw/*',
        '~/Desktop/*',
        '~/Documents/*'
      ]
    },
    toolLevels: new Map([
      ['read', 'read'],
      ['web_fetch', 'read'],
      ['web_search', 'read'],
      ['memory_search', 'read'],
      ['write', 'write'],
      ['edit', 'write'],
      ['exec', 'execute'],
      ['browser', 'execute'],
      ['process', 'admin'],
      ['subagents', 'admin']
    ])
  }
}

/**
 * 检查工具权限
 */
export function checkToolPermission(
  toolName: string,
  toolInput: Record<string, any>,
  context: ToolPermissionContext
): PermissionResult {
  // 1. 检查黑名单
  if (isInDenyList(toolName, toolInput, context)) {
    return 'deny'
  }
  
  // 2. 检查白名单
  if (context.allowedTools.has(toolName)) {
    return 'allow'
  }
  
  // 3. 检查自动批准规则
  if (matchesAlwaysAllowRules(toolName, toolInput, context)) {
    return 'allow'
  }
  
  // 4. 根据模式判断
  return checkByMode(toolName, context)
}

/**
 * 检查是否在黑名单中
 */
function isInDenyList(
  toolName: string,
  toolInput: Record<string, any>,
  context: ToolPermissionContext
): boolean {
  for (const denied of context.deniedTools) {
    // 格式: toolName:pattern
    if (denied.includes(':')) {
      const [name, pattern] = denied.split(':')
      if (name === toolName) {
        const input = toolInput.command || toolInput.path || ''
        if (input.includes(pattern)) {
          return true
        }
      }
    } else {
      if (denied === toolName) {
        return true
      }
    }
  }
  return false
}

/**
 * 检查是否匹配自动批准规则
 */
function matchesAlwaysAllowRules(
  toolName: string,
  toolInput: Record<string, any>,
  context: ToolPermissionContext
): boolean {
  const rules = context.alwaysAllowRules
  
  // 检查命令规则
  if (toolName === 'exec' && toolInput.command) {
    for (const pattern of rules.commands) {
      if (matchPattern(toolInput.command, pattern)) {
        return true
      }
    }
  }
  
  // 检查文件规则
  if (['read', 'write', 'edit'].includes(toolName)) {
    const filePath = toolInput.path || toolInput.file_path || ''
    for (const pattern of rules.files) {
      if (matchPattern(filePath, pattern)) {
        return true
      }
    }
  }
  
  return false
}

/**
 * 根据模式检查权限
 */
function checkByMode(toolName: string, context: ToolPermissionContext): PermissionResult {
  const level = context.toolLevels.get(toolName) || 'execute'
  
  switch (context.mode) {
    case 'plan':
      // 规划模式：只允许只读操作
      return level === 'read' ? 'allow' : 'deny'
      
    case 'auto':
      // 自动模式：只读和写入自动批准，执行和管理需确认
      return level === 'read' || level === 'write' ? 'allow' : 'confirm'
      
    case 'default':
    default:
      // 默认模式：只读自动批准，其他需确认
      return level === 'read' ? 'allow' : 'confirm'
  }
}

/**
 * 简单模式匹配（支持 * 通配符）
 */
function matchPattern(text: string, pattern: string): boolean {
  // 精确匹配
  if (pattern === text) return true
  
  // 前缀匹配
  if (pattern.endsWith('*')) {
    const prefix = pattern.slice(0, -1)
    return text.startsWith(prefix)
  }
  
  // 后缀匹配
  if (pattern.startsWith('*')) {
    const suffix = pattern.slice(1)
    return text.endsWith(suffix)
  }
  
  // 包含匹配
  if (pattern.includes('*')) {
    const parts = pattern.split('*')
    let index = 0
    for (const part of parts) {
      index = text.indexOf(part, index)
      if (index === -1) return false
      index += part.length
    }
    return true
  }
  
  return false
}

/**
 * 切换权限模式
 */
export function setPermissionMode(
  context: ToolPermissionContext,
  mode: PermissionMode
): void {
  context.mode = mode
}

/**
 * 获取当前权限模式
 */
export function getPermissionMode(context: ToolPermissionContext): PermissionMode {
  return context.mode
}

/**
 * 添加工具到白名单
 */
export function allowTool(context: ToolPermissionContext, toolName: string): void {
  context.allowedTools.add(toolName)
  context.deniedTools.delete(toolName)
}

/**
 * 添加工具到黑名单
 */
export function denyTool(context: ToolPermissionContext, toolName: string): void {
  context.deniedTools.add(toolName)
  context.allowedTools.delete(toolName)
}
