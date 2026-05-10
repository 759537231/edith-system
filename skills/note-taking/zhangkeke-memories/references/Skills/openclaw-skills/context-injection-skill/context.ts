/**
 * QClaw 上下文自动注入
 * 参考 Claude Code 的 getUserContext/getSystemContext 设计
 * 自动注入 Git 状态、当前日期等信息
 */

import { execSync } from 'child_process'
import { existsSync, readFileSync } from 'fs'
import { join } from 'path'

interface GitStatus {
  branch: string
  mainBranch: string
  status: string
  recentCommits: string
  userName: string
}

interface SystemContext {
  gitStatus?: GitStatus
  currentDate: string
  currentTime: string
  timezone: string
}

interface UserContext {
  memoryMd?: string
  projectRoot?: string
}

/**
 * 获取本地 ISO 日期
 */
function getLocalISODate(): string {
  const now = new Date()
  const offset = now.getTimezoneOffset()
  const local = new Date(now.getTime() - offset * 60 * 1000)
  return local.toISOString().split('T')[0]
}

/**
 * 获取本地时间
 */
function getLocalTime(): string {
  return new Date().toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}

/**
 * 获取时区
 */
function getTimezone(): string {
  try {
    return Intl.DateTimeFormat().resolvedOptions().timeZone
  } catch {
    return 'Asia/Shanghai'
  }
}

/**
 * 检查是否在 Git 仓库中
 */
function isGitRepo(cwd: string): boolean {
  try {
    execSync('git rev-parse --git-dir', { cwd, stdio: 'pipe' })
    return true
  } catch {
    return false
  }
}

/**
 * 获取 Git 状态
 */
function getGitStatus(cwd: string): GitStatus | null {
  if (!isGitRepo(cwd)) {
    return null
  }

  try {
    const branch = execSync('git rev-parse --abbrev-ref HEAD', { cwd, encoding: 'utf-8' }).trim()
    
    let mainBranch = 'main'
    try {
      mainBranch = execSync('git symbolic-ref refs/remotes/origin/HEAD', { cwd, encoding: 'utf-8' })
        .trim()
        .replace('refs/remotes/origin/', '')
    } catch {
      // 默认 main
    }

    const status = execSync('git status --short', { cwd, encoding: 'utf-8' }).trim()
    
    const recentCommits = execSync('git log --oneline -n 5', { cwd, encoding: 'utf-8' }).trim()
    
    let userName = ''
    try {
      userName = execSync('git config user.name', { cwd, encoding: 'utf-8' }).trim()
    } catch {
      // 忽略
    }

    return {
      branch,
      mainBranch,
      status: status || '(clean)',
      recentCommits,
      userName
    }
  } catch (error) {
    console.error('Failed to get git status:', error)
    return null
  }
}

/**
 * 格式化 Git 状态为可读文本
 */
function formatGitStatus(git: GitStatus): string {
  const lines = [
    `当前分支: ${git.branch}`,
    `主分支: ${git.mainBranch}`,
    git.userName ? `Git 用户: ${git.userName}` : null,
    `状态:\n${git.status}`,
    `最近提交:\n${git.recentCommits}`
  ].filter(Boolean)

  return lines.join('\n\n')
}

/**
 * 获取系统上下文（自动注入）
 */
export async function getSystemContext(cwd?: string): Promise<SystemContext> {
  const workDir = cwd || process.cwd()
  
  const gitStatus = getGitStatus(workDir)
  
  return {
    ...(gitStatus && { gitStatus }),
    currentDate: `今天是 ${getLocalISODate()}`,
    currentTime: `当前时间 ${getLocalTime()}`,
    timezone: `时区 ${getTimezone()}`
  }
}

/**
 * 获取用户上下文（自动注入）
 */
export async function getUserContext(workspaceRoot?: string): Promise<UserContext> {
  const root = workspaceRoot || process.cwd()
  
  // 查找 MEMORY.md
  const memoryPath = join(root, 'MEMORY.md')
  let memoryMd: string | undefined
  
  if (existsSync(memoryPath)) {
    try {
      memoryMd = readFileSync(memoryPath, 'utf-8')
    } catch {
      // 忽略
    }
  }
  
  return {
    ...(memoryMd && { memoryMd }),
    projectRoot: root
  }
}

/**
 * 构建完整的上下文注入文本
 */
export async function buildContextInjection(cwd?: string): Promise<string> {
  const systemCtx = await getSystemContext(cwd)
  const userCtx = await getUserContext(cwd)
  
  const parts: string[] = []
  
  // 系统上下文
  parts.push(`## 系统信息\n`)
  parts.push(systemCtx.currentDate)
  parts.push(`，${systemCtx.currentTime}`)
  parts.push(`，${systemCtx.timezone}`)
  
  if (systemCtx.gitStatus) {
    parts.push(`\n\n## Git 状态\n`)
    parts.push(formatGitStatus(systemCtx.gitStatus))
  }
  
  // 用户上下文
  if (userCtx.memoryMd) {
    parts.push(`\n\n## 项目记忆\n`)
    parts.push(`见 MEMORY.md 文件内容`)
  }
  
  return parts.join('')
}

/**
 * 获取当前日期（简化版，用于快速注入）
 */
export function getCurrentDateContext(): string {
  return `今天是 ${getLocalISODate()}，当前时间 ${getLocalTime()}，时区 ${getTimezone()}`
}

// 导出工具函数
export {
  getLocalISODate,
  getLocalTime,
  getTimezone,
  isGitRepo,
  getGitStatus,
  formatGitStatus
}
