# 本地模型选型参考（2026-05 更新）

> 基于 Mac Mini M1 16GB 的实测调研

## mlx_lm 兼容性说明（重要）

| 模型 | model_type | mlx_lm 0.29.1 支持？ | 备注 |
|------|-----------|---------------------|------|
| Qwen3-4B | `qwen3` | ✅ 支持 | **当前主力** |
| Qwen3.5-4B | `qwen3_5` | ❌ 不支持 | 需等 mlx_lm 更新 |
| Qwen3.5-35B-A3B | `qwen3_5` | ❌ 不支持 | 同上 |

## Qwen 3.x 全系列

### Qwen 3（mlx_lm 已支持）

| 模型 | 参数量 | 类型 | 16GB M1 可跑？ | 内存(Q4) | 速度(M1) | 备注 |
|------|--------|------|---------------|----------|----------|------|
| Qwen3-1.8B | 1.8B | Dense | ✅ 轻松 | ~1.5GB | 70-90 tok/s | 极速 |
| **Qwen3-4B** | 4B | Dense | ✅ 舒服 | ~3GB | 45-65 tok/s | **首选** |
| Qwen3-8B | 8B | Dense | ⚠️ 勉强 | ~5GB | 25-40 tok/s | 剩余空间紧张 |

### Qwen 3.5（mlx_lm 暂不支持）

| 模型 | 参数量 | 类型 | 16GB M1 可跑？ | 内存(Q4) | 速度(M1) | 备注 |
|------|--------|------|---------------|----------|----------|------|
| Qwen3.5-0.8B | 0.8B | Dense | ✅ 轻松 | ~1GB | 80-100 tok/s | 超轻量 |
| Qwen3.5-2B | 2B | Dense | ✅ 轻松 | ~2GB | 60-80 tok/s | 速度快 |
| Qwen3.5-4B | 4B | Dense | ✅ 舒服 | ~3GB | 45-65 tok/s | 等 mlx_lm 更新 |
| Qwen3.5-9B | 9B | Dense | ⚠️ 勉强 | ~6GB | 25-40 tok/s | 剩余空间紧张 |
| Qwen3.5-35B-A3B | 35B(活跃3B) | MoE | ❌ 跑不动 | ~17.5GB | — | 内存按总参数算，不按活跃参数 |

### Qwen 3.6

| 模型 | 参数量 | 类型 | 16GB M1 可跑？ | 备注 |
|------|--------|------|---------------|------|
| Qwen3.6-27B | 27B | Dense | ❌ | 需32GB+ |
| Qwen3.6-35B-A3B | 35B(活跃3B) | MoE | ❌ 跑不动 | 内存按总参数算，~17.5GB |
| Qwen3.6-max | 云端 | — | — | 仅云端 |
| Qwen3.6-plus | 云端 | — | — | 仅云端 |

## 其他模型

| 模型 | 厂商 | 大小 | 16GB M1 可跑？ | 强项 |
|------|------|------|---------------|------|
| Phi-3-mini 3.8B | Microsoft | 3.8B | ✅ | 推理强、速度快 |
| Phi-4 | Microsoft | 14B | ⚠️ 勉强 | 推理能力突出 |
| DeepSeek Coder V2 Lite | DeepSeek | 16B(活跃2.4B) | ✅ MoE | 代码专用 |
| Ministral 8B | Mistral | 8B | ⚠️ 勉强 | 边缘优化 |
| Llama 3.2 3B | Meta | 3B | ✅ | 英文强 |
| Gemma 4 31B | Google | 31B | ❌ | 多模态 |

## MoE 模型：16GB 的突破口

Qwen3.5-35B-A3B 和 Qwen3.6-35B-A3B 是 MoE（混合专家）架构：
- 总参数 35B = 能力接近大模型
- 活跃参数只有 3B = 推理时内存占用小
- 已有人在 Apple Silicon 上跑通（4-bit 量化，6.6 tok/s）

**局限**：
- 速度慢（6.6 tok/s vs 7B 的 25-40 tok/s）
- 需要 llama.cpp 或专门的 MoE 推理引擎
- MLX 对 MoE 支持可能不成熟

## 推荐策略

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 日常对话 | **Qwen3-4B** | mlx_lm 已支持，速度质量平衡 |
| 代码生成 | DeepSeek Coder V2 Lite | 代码专业 |
| 极速响应 | Qwen3-1.8B | 批量简单任务 |
| 最大能力 | Qwen3.5-35B-A3B | MoE 突破内存限制（需等 mlx_lm 支持） |
| 英文任务 | Llama 3.2 3B | 英文优化 |

> ⚠️ 当前（2026-05）mlx_lm 只支持 Qwen3，不支持 Qwen3.5。首选 Qwen3-4B。

## 量化选择

| 量化 | 质量 | 速度 | 内存 | 建议 |
|------|------|------|------|------|
| Q8_0 | 很好 | 中 | 中 | 重要任务 |
| **Q4_K_M** | 好 | 快 | 小 | **日常首选** |
| Q2_K | 差 | 最快 | 最小 | 不推荐 |

## 参考项目

- flash-moe-35b: Qwen3.5-35B-A3B-4bit 在 Apple Silicon 上 6.6 tok/s
- mlx-fallback: Qwen3.5-4B-MLX-VLM 本地部署
- localai: Qwen3.5-4B + RAG 完整本地方案

## 实战踩坑记录（2026-05-03）

### mlx_lm.server 模型路径 bug
- **现象**：启动时指定 `--model /path/to/Qwen3-4B`，但请求时报错 `No safetensors found in ~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/...`
- **根因**：server 内部用模型名（从 config.json 读取）去 HF 缓存找，忽略 `--model` 参数
- **复现**：HF 缓存有同名模型残留 → 必现
- **解决**：清理 HF 缓存 + 用绝对路径，或改用直接 Python API（最可靠）

### ModelScope 断点续传
- **场景**：HuggingFace 连接超时，改用 ModelScope 下载
- **方法**：`python3 -c "from modelscope import snapshot_download; snapshot_download('Qwen/Qwen3-4B', local_dir='~/models/Qwen/Qwen3-4B')"`
- **特性**：自动检测 `._____temp/` 目录中的未完成文件，断点续传
- **速度**：国内源约 13-17 MB/s

### HF 缓存干扰
- **现象**：之前 HF 下载失败留下元数据，影响后续 mlx_lm 加载
- **解决**：`rm -rf ~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B`
- **预防**：下载新模型前先清理同名缓存

### Python 版本与 mlx 版本对应关系
| Python | 最高 mlx | 最高 mlx-lm | 说明 |
|--------|---------|-------------|------|
| 3.9.6（系统） | 0.29.3 | 0.29.1 | 当前环境，无法升级 |
| 3.10+ | 0.31.x | 0.31.3 | 支持 Qwen3.5 |
| 3.11（Hermes venv） | 最新 | 最新 | 路径：`~/.hermes/hermes-agent/venv/bin/python3.11` |

**结论**：要支持 Qwen3.5，必须用 Python 3.10+ 环境安装 mlx-lm。

### mlx_lm.server 后台启动被 kill
- **现象**：`nohup python3 -m mlx_lm server ... &` 启动后立即退出
- **原因**：server 的 `-q` 参数处理有 bug，后台启动时 stdin 关闭导致异常
- **解决**：用 `subprocess.Popen()` 启动（保持 stdin 打开），或写自定义 Flask 服务器包装 `load()` + `generate()`
