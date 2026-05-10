---
name: memory-tagging
description: |
  记忆来源标记系统。自动为记忆内容添加来源标记（壳壳/二壳）。
  触发词：保存记忆、记住这个、写入记忆
---

# 🏷️ 记忆来源标记系统

## 功能

自动为记忆内容添加来源标记，区分是"壳壳记忆"还是"二壳记忆"。

## 使用方法

### 保存记忆时

在调用memory工具时，自动读取环境变量`MEMORY_TAG`，并添加到content前：

```python
import os

def get_memory_tag():
    """获取记忆标记"""
    return os.environ.get('MEMORY_TAG', '[壳壳记忆]')

def add_tag_to_content(content: str) -> str:
    """为内容添加记忆标记"""
    tag = get_memory_tag()
    
    # 检查是否已经有标记
    if content.startswith('[壳壳记忆]') or content.startswith('[二壳记忆]'):
        return content
    
    # 添加标记
    return f"{tag} {content}"
```

### 示例

**用户说**：记住我喜欢简洁回复

**AI应该**：
```python
import os

# 获取记忆标记
tag = os.environ.get('MEMORY_TAG', '[壳壳记忆]')

# 添加标记到内容
content = f"{tag} 用户偏好简洁回复"

# 保存记忆
memory(action="add", target="memory", content=content)
```

## 环境变量

- `MEMORY_TAG`: 记忆标记，值为`[壳壳记忆]`或`[二壳记忆]`
- `HERMES_PROFILE`: 当前profile名称

## 配置方法

### 张壳壳（云端）

```bash
export MEMORY_TAG="[壳壳记忆]"
hermes
```

### 张二壳（本地）

```bash
export MEMORY_TAG="[二壳记忆]"
hermes -p zhang-er-ke
```

或者使用wrapper脚本：

```bash
~/.local/bin/zhang-er-ke-wrapper
```

## 注意事项

1. 每次保存记忆都必须添加来源标记
2. 标记格式固定为`[壳壳记忆]`或`[二壳记忆]`
3. 标记放在内容最前面
4. 不要忘记添加标记

## Profile配置

### 创建张二壳Profile

```bash
# 创建profile（克隆默认配置）
hermes profile create zhang-er-ke --clone

# 配置本地模型
hermes -p zhang-er-ke config set model.default qwen3.5-4b
hermes -p zhang-er-ke config set model.base_url http://localhost:8080/v1
hermes -p zhang-er-ke config set model.api_key not-needed

# 配置共享skills目录
hermes -p zhang-er-ke config set skills.directory ~/.hermes/skills
```

### 创建Wrapper脚本

位置：`~/.local/bin/zhang-er-ke-wrapper`

```bash
#!/bin/bash
export HERMES_PROFILE="zhang-er-ke"
export MEMORY_TAG="[二壳记忆]"
hermes -p zhang-er-ke "$@"
```

### 启动命令

**张壳壳（云端）：**
```bash
hermes
```

**张二壳（本地）：**
```bash
~/.local/bin/zhang-er-ke-wrapper
```

## 相关文件

- 记忆存储：`~/.hermes/workspace/MEMORY.md`
- Profile配置：`~/.hermes/profiles/zhang-er-ke/`
- Wrapper脚本：`~/.local/bin/zhang-er-ke-wrapper`
