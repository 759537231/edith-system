/**
 * QClaw Feature Flags 系统
 * 参考 Claude Code 的 feature() 设计，控制实验性功能的启用/禁用
 */

import { readFileSync, existsSync } from 'fs'
import { join } from 'path'

interface FeatureConfig {
  enabled: boolean
  description: string
}

interface FeaturesFile {
  $schema?: string
  version: string
  description?: string
  features: Record<string, FeatureConfig>
}

// 缓存已加载的配置
let cachedFeatures: Map<string, boolean> | null = null

/**
 * 获取 features.json 的路径
 */
function getFeaturesPath(): string {
  // 优先级：环境变量 > 默认路径
  if (process.env.QCLAW_FEATURES_PATH) {
    return process.env.QCLAW_FEATURES_PATH
  }
  
  // macOS/Linux
  const homeDir = process.env.HOME || process.env.USERPROFILE
  return join(homeDir || '~', '.qclaw', 'features.json')
}

/**
 * 加载 features.json
 */
function loadFeatures(): Map<string, boolean> {
  if (cachedFeatures) {
    return cachedFeatures
  }

  const featuresPath = getFeaturesPath()
  
  if (!existsSync(featuresPath)) {
    // 文件不存在时返回空 Map
    cachedFeatures = new Map()
    return cachedFeatures
  }

  try {
    const content = readFileSync(featuresPath, 'utf-8')
    const config: FeaturesFile = JSON.parse(content)
    
    cachedFeatures = new Map()
    for (const [name, feature] of Object.entries(config.features || {})) {
      cachedFeatures.set(name, feature.enabled)
    }
    
    return cachedFeatures
  } catch (error) {
    console.error('Failed to load features.json:', error)
    cachedFeatures = new Map()
    return cachedFeatures
  }
}

/**
 * 检查某个功能是否启用
 * @param name 功能名称
 * @returns 是否启用
 */
export function isFeatureEnabled(name: string): boolean {
  const features = loadFeatures()
  return features.get(name) ?? false
}

/**
 * 获取所有已启用的功能
 * @returns 已启用的功能名称列表
 */
export function getEnabledFeatures(): string[] {
  const features = loadFeatures()
  return Array.from(features.entries())
    .filter(([, enabled]) => enabled)
    .map(([name]) => name)
}

/**
 * 获取所有功能及其状态
 * @returns 功能状态映射
 */
export function getAllFeatures(): Record<string, { enabled: boolean; description: string }> {
  const featuresPath = getFeaturesPath()
  
  if (!existsSync(featuresPath)) {
    return {}
  }

  try {
    const content = readFileSync(featuresPath, 'utf-8')
    const config: FeaturesFile = JSON.parse(content)
    
    const result: Record<string, { enabled: boolean; description: string }> = {}
    for (const [name, feature] of Object.entries(config.features || {})) {
      result[name] = {
        enabled: feature.enabled,
        description: feature.description
      }
    }
    
    return result
  } catch {
    return {}
  }
}

/**
 * 清除缓存（用于重新加载配置）
 */
export function clearFeaturesCache(): void {
  cachedFeatures = null
}

// 兼容 Claude Code 的命名
export const feature = isFeatureEnabled
