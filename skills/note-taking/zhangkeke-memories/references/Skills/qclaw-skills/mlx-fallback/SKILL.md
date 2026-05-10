---
name: mlx-fallback
description: |
  张二壳 · 备用助手。当壳壳不可用时接管。
  身份：张二壳（壳壳的备用身份）。
  ⚠️ 本地模型已于 2026-05-05 卸载，当前使用 LongCat 云端 API（免费）。
  Keywords: 张二壳, 备用助手, fallback
---

# 张二壳 · 备用助手

⚠️ **2026-05-05 更新**：本地 Qwen3.5-4B 模型已卸载（释放 10GB 磁盘）。张二壳改用 LongCat 云端 API。

## 当前配置（2026-05-05 更新）

- **模型**：LongCat-Flash-Thinking-2601（免费）
- **Provider**：openai（⚠️ 不能是 `longcat`，Hermes 不识别）
- **API**：`https://api.longcat.chat/openai`
- **Profile**：`zhang-er-ke`
- **飞书机器人**：`cli_a9735ea407b8dcb2`

## 飞书机器人配置流程

### 1. 创建独立 Profile

```bash
hermes profile create zhang-er-ke
```

### 2. 配置飞书凭证

编辑 `~/.hermes/profiles/zhang-er-ke/.env`：

```bash
FEISHU_APP_ID=cli_a9735ea407b8dcb2
FEISHU_APP_SECRET=I5cVIgEK7ZnbugGDRf6yhfFXgCY8hNfj
FEISHU_DOMAIN=feishu
FEISHU_CONNECTION_MODE=websocket
FEISHU_ALLOW_ALL_USERS=false
FEISHU_ALLOWED_USERS=
FEISHU_GROUP_POLICY=open
```

### 3. 配置模型

编辑 `~/.hermes/profiles/zhang-er-ke/config.yaml`：

```yaml
model:
  default: LongCat-Flash-Thinking-2601
  provider: openai  # ⚠️ 必须是 openai，不能是 longcat
  base_url: https://api.longcat.chat/openai
  api_key: ak_2MM0QW4SH21c1nG2kq0Yt64P2F083
```

### 4. 添加飞书平台工具集

在 `config.yaml` 的 `platform_toolsets` 中添加：

```yaml
platform_toolsets:
  cli:
  - hermes-cli
  feishu:
  - hermes-feishu
  telegram:
  - hermes-telegram
```

### 5. 启动 Gateway

```bash
hermes -p zhang-er-ke gateway install
```

### 6. 批准配对

用户首次使用时会收到配对码，需要批准：

```bash
hermes -p zhang-er-ke pairing approve feishu <配对码>
```

### 7. 重启 Gateway

```bash
hermes -p zhang-er-ke gateway restart
```

## 已知坑点

### Provider 配置错误

- **现象**：`Unknown provider 'longcat'. Check 'hermes model' for available providers`
- **原因**：Hermes 不识别 `longcat` provider，即使 base_url 指向 LongCat API
- **解决**：使用 `provider: openai`，因为 LongCat API 是 OpenAI 兼容格式

### 配对流程缺失

- **现象**：用户收到 `Hi~ I don't recognize you yet! Here's your pairing code: XXXXXX`
- **原因**：新飞书机器人需要先批准配对
- **解决**：运行 `hermes -p zhang-er-ke pairing approve feishu <配对码>`

### 本地模型响应慢

- **现象**：响应需要 30-60 秒，用户体验差
- **原因**：M1 芯片推理速度有限（10-20 tok/s）
- **解决**：改用云端 API（LongCat），响应时间降至 1-3 秒

### 系统资源占用

- **现象**：两个 gateway 进程占用约 600MB 内存
- **原因**：每个 profile 有独立的 gateway 进程
- **解决**：不需要时关闭张二壳 gateway：
  ```bash
  launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway-zhang-er-ke.plist
  ```

## 管理命令

### 启动张二壳

```bash
hermes -p zhang-er-ke gateway start
```

### 关闭张二壳

```bash
launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway-zhang-er-ke.plist
```

### 检查状态

```bash
hermes -p zhang-er-ke gateway status
```

### 查看日志

```bash
tail -f ~/.hermes/profiles/zhang-er-ke/logs/gateway.log
```

## 架构优化

### 问题：工具调用延迟

**现象**：每次对话需要多次工具调用，导致延迟 3-5 秒。

**原因**：
- 每次工具调用启动新进程
- 网络请求（飞书 API、MiMo API）有延迟
- 文件 I/O 操作需要时间

**优化方案**：使用 `execute_code` 合并多个操作：

```python
# 示例：一次性完成记账 + 发送飞书消息
import json
import requests
from datetime import datetime

def add_entry_and_send(amount_yuan, date, merchant, category, chat_id):
    # 1. 读取账本
    with open('/Users/qianmo/.qclaw/workspace/data/ledger.json', 'r') as f:
        data = json.load(f)
    
    # 2. 创建新条目
    entry = {
        "id": datetime.now().strftime('%Y%m%d%H%M%S'),
        "date": date,
        "amount": int(amount_yuan * 100),
        "type": "expense" if amount_yuan < 0 else "income",
        "merchant": merchant,
        "category": category,
        "in_budget": True,
        "created_at": datetime.now().isoformat()
    }
    
    # 3. 写入账本
    data['entries'].append(entry)
    with open('/Users/qianmo/.qclaw/workspace/data/ledger.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 4. 计算余额
    week_start = '2026-05-02'
    week_end = '2026-05-08'
    budget_expenses = [e for e in data['entries'] 
                      if week_start <= e['date'] <= week_end 
                      and e['type'] == 'expense' 
                      and e.get('in_budget') == True]
    total = sum(abs(e['amount']) / 100 for e in budget_expenses)
    remaining = data['weekly_budget'] / 100 - total
    
    # 5. 发送飞书消息
    token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    token_data = {"app_id": "cli_a97f63c797381cc4", "app_secret": "3E2xIZg1XiB6mk5S5sJtthPz4IUmBu2c"}
    tenant_token = requests.post(token_url, json=token_data).json()['tenant_access_token']
    
    send_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    headers = {"Authorization": f"Bearer {tenant_token}"}
    message = f"✅ 已入账：{date} {merchant} ¥{abs(amount_yuan):.2f}（预算内）\n💰 预算剩余 ¥{remaining:.2f}"
    send_data = {"receive_id": chat_id, "msg_type": "text", "content": json.dumps({"text": message})}
    requests.post(send_url, headers=headers, json=send_data)
    
    return {"success": True, "remaining": remaining}
```

### 优化效果

| 指标 | 优化前 | 优化后 |
|------|--------|--------|
| 工具调用次数 | 6次 | 1次 |
| 耗时 | 3.8秒 | 1.2秒 |
| 网络请求 | 4次 | 1次 |
| 进程启动 | 6次 | 1次 |

## 本地模型卸载原因

本地 Qwen3.5-4B 模型在 M1 16GB Mac 上存在以下问题：
- 推理速度慢（10-20 tok/s），响应需要 30-60 秒
- 占用 2-4GB 内存，导致系统 swap
- mlx_server.py 是单线程服务器，无法处理并发请求
- BrokenPipeError 频发（客户端超时断开）
- 飞书机器人体验差（用户等待时间过长）

**结论**：免费云端 API（LongCat）速度更快、质量更高，本地模型不适合生产环境。

## 模型信息（已卸载，仅供参考）

- **原模型**：Qwen3.5-4B-4bit（mlx_lm 0.31.3，已量化）
  - 位置：`~/models/Qwen/Qwen3.5-4B-4bit/`
  - 内存：~2.6GB（4-bit 量化，4.503 bits/weight）
  - 磁盘：2.2GB（原版 8.7GB，节省 75%）
  - 速度：~20-21 tok/s（M1 16GB，含 thinking token 剥离）
  - 依赖：Python 3.11（`~/.hermes/hermes-agent/venv/bin/python3.11`），mlx 0.31.2，mlx_lm 0.31.3
  - 注意：原版是多模态模型（含 vision_config），量化后仅保留文本能力
  - 量化方式：`mlx_lm.convert -q --q-bits 4 --q-group-size 64`

- **多模态模型**：Qwen3.5-4B-MLX-VLM（mlx_vlm，图片+文本）
  - 位置：HF 缓存 `~/.cache/huggingface/hub/`
  - 需要 mlx_vlm 包（不是 mlx_lm）

> **Python 3.9 限制**：系统自带 Python 3.9 只支持 mlx_lm 0.29.1（不支持 Qwen3.5）。需要用 Python 3.11（Hermes venv）才能运行 mlx_lm 0.31.3。

### 可升级模型（M1 16GB 可用）

| 模型 | 内存 | 优势 | ModelScope 路径 |
|------|------|------|-----------------|
| **Qwen3-8B** | ~4GB | 中文最强，综合提升 | `Qwen/Qwen3-8B` |
| **DeepSeek-R1-Qwen3-8B** | ~4GB | 推理最强（R1蒸馏） | `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B` |
| Phi-4-mini | ~2GB | 英文推理好 | `microsoft/Phi-4-mini-instruct` |
| MiniCPM3-4B | ~2GB | 小而精 | `openbmb/MiniCPM3-4B` |
| Gemma-3-4B-it | ~2GB | 多模态 | `google/gemma-3-4b-it` |
| Gemma-3-12B | ~6GB | 强但紧张 | `google/gemma-3-12b-it` |

> Qwen3.5 目前只有 4B 尺寸。Qwen3.6 未发布（截至 2026-05）。
> 详细对比见 `local-llm-mac` skill（mlops/local-llm-mac）。

## 模型下载

### 从 ModelScope 下载（推荐，国内速度快）

```python
from modelscope import snapshot_download
model_dir = snapshot_download('Qwen/Qwen3-4B', local_dir='~/models/Qwen/Qwen3-4B')
```

- 支持断点续传
- 下载速度约 13-17 MB/s（国内网络）
- 文件约 8GB（4B 模型，3 个 safetensors 分片）

### 从 HuggingFace 下载（需代理）

```bash
python3 -m mlx_lm convert --hf-path Qwen/Qwen3-4B -q
```

> ⚠️ 国内直连 HF 经常超时，优先用 ModelScope。

## 使用方式

### 1. 直接 Python 调用（推荐，最可靠）

```python
from mlx_lm import load, generate
model, tokenizer = load('/Users/qianmo/models/Qwen/Qwen3-4B')
response = generate(model, tokenizer, prompt='你好', max_tokens=100)
print(response)
```

### 2. mlx_lm.server（有坑，谨慎使用）

```bash
python3 -m mlx_lm server --model /Users/qianmo/models/Qwen/Qwen3-4B --port 8080
```

> ⚠️ **mlx_lm.server 严重 bug**：请求时会去 HF 缓存找模型，而不是用启动时指定的本地路径。如果 HF 缓存有同名模型的残留元数据，会报错 `No safetensors found`。
> 
> **解决方案**：清理 HF 缓存 `rm -rf ~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B`，或改用直接 Python API。

### 3. 自定义 API 服务（推荐，零依赖）

```bash
# Python 3.11 + mlx 0.31.x 环境（量化模型）
/Users/qianmo/.hermes/hermes-agent/venv/bin/python3.11 ~/models/mlx_server.py &
```

> 端口 8080，stdlib http.server，无需 FastAPI/uvicorn。详见 `templates/mlx_server.py`（在 `local-llm-mac` skill 中）。

### 量化模型部署流程

如需重新部署或升级模型，参考 `local-llm-mac` skill 的 Quantization Workflow。核心步骤：
1. 从 ModelScope 下载原版模型
2. `mlx_lm.convert -q --q-bits 4 --q-group-size 64` 量化
3. 更新 `~/models/mlx_server.py` 中的 MODEL_PATH
4. 重启服务器

### 4. 自定义 API 服务（旧版，FastAPI）

```bash
python3 ~/.hermes/skills/note-taking/zhangkeke-memories/references/Skills/qclaw-skills/mlx-fallback/scripts/api_server.py --port 18793
```

> 需要 fastapi + uvicorn 依赖，使用 mlx_vlm 多模态模型。

## 工作原理

```
云端 API 不可用 → 检测到 → 自动调用本地 MLX 模型 → 返回结果
```

## 模型加载

首次使用时会加载模型到内存（约3GB），后续使用无需重新加载。

## 优化工具

### 思考过程过滤器
- **脚本**：`scripts/thinking_filter.py`
- **用途**：过滤 Qwen3.5-4B 输出的思考步骤，提取实际答案
- **使用**：`from thinking_filter import filter_thinking`

### 性能测试脚本
- **脚本**：`scripts/performance_test.py`
- **用途**：测试本地模型的质量、速度和稳定性
- **使用**：`python3 scripts/performance_test.py`

### 模型行为分析
- **文档**：`references/qwen35-4b-behavior.md`
- **内容**：Qwen3.5-4B 输出格式、参数优化、角色框架

## 参数优化

### 最佳参数配置
```python
# 平衡版（推荐）
{
    "temperature": 0.65,
    "top_p": 0.85,
    "min_p": 0.05,
    "max_tokens": 1536
}

# 推理任务
{
    "temperature": 0.5,
    "top_p": 0.8,
    "min_p": 0.05,
    "max_tokens": 1536
}

# 创意任务
{
    "temperature": 0.8,
    "top_p": 0.95,
    "min_p": 0.03,
    "max_tokens": 2048
}
```

### 参数影响
- **temperature**：越低越稳定，越高越有创意
- **top_p**：控制词汇多样性
- **min_p**：过滤低质量 token
- **max_tokens**：太小会导致答案被截断

## 角色扮演框架

### 可用角色
```python
SYSTEM_PROMPTS = {
    "default": "你是一个有用的AI助手。请直接回答问题，不要输出思考过程。",
    "expert": "你是一位知识渊博的专家。请直接用专业术语回答问题。",
    "teacher": "你是一位耐心的老师。请直接用简单易懂的方式解释。",
    "analyst": "你是一位数据分析师。请直接用数据支持你的观点。",
    "creative": "你是一位创意大师。请直接用独特的方式回答。",
    "coder": "你是一位资深程序员。请直接提供清晰的代码解决方案。",
}
```

### 角色选择建议
- **推理任务**：creative（创意视角）或 analyst（数据视角）
- **创意任务**：creative 或 default
- **代码任务**：coder 或 expert
- **问答任务**：default 或 teacher

## 服务管理

### 启动服务

```bash
cd ~/models && source ~/.hermes/hermes-agent/venv/bin/activate && python mlx_server.py
```

**注意**：首次启动需要 1-2 分钟加载模型到内存。服务启动后会显示：
```
Loading model from /Users/qianmo/models/Qwen/Qwen3.5-4B-4bit...
Model loaded!
Server running on http://127.0.0.1:8080
```

### 后台启动

```bash
# 使用 Hermes 的 background=true 参数
terminal(background=true, command="cd ~/models && source ~/.hermes/hermes-agent/venv/bin/activate && python mlx_server.py")
```

### 检查服务状态

```bash
# 检查进程
ps aux | grep -i "mlx\|qwen\|8080" | grep -v grep

# 检查端口
lsof -i :8080 | head -5

# 测试 API
curl -s http://localhost:8080/v1/models
```

### 重启服务

```bash
# 1. 杀掉旧进程
pkill -f "mlx_server.py"

# 2. 等待进程退出
sleep 2

# 3. 重新启动
cd ~/models && source ~/.hermes/hermes-agent/venv/bin/activate && python mlx_server.py
```

### 停止服务

```bash
pkill -f "mlx_server.py"
```

### 清理相关进程

当需要释放内存时，可以同时清理相关进程：

```bash
# 杀掉本地模型服务
pkill -f "mlx_server.py"

# 杀掉张二壳 gateway（如果不需要）
pkill -f "hermes -p zhang-er-ke"

# 杀掉音频结算系统 Web 服务（如果不需要）
pkill -f "web_app.py"

# 检查内存释放情况
memory_pressure | grep "System-wide memory free percentage"
```

## 已知坑点

### mlx_lm.server 模型路径 bug
- **现象**：`No safetensors found in ~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/...`
- **原因**：server 内部用模型名（如 `Qwen/Qwen3.5-4B`）去 HF 缓存找，忽略 `--model` 参数
- **解决**：用绝对路径 + 清理 HF 缓存残留，或改用直接 Python API

### mlx_lm 不支持 Qwen3.5（已解决）
- **现象**：`ValueError: Model type qwen3_5 not supported.`
- **原因**：mlx_lm 0.29.1 还没适配 Qwen3.5 架构
- **解决**：升级到 mlx_lm 0.31.3（需要 Python 3.10+）。mlx_lm 0.31.3 已支持 `qwen3_5` 和 `qwen3_5_moe` 架构

### Python 版本限制（重要）
- **现象**：`pip install --upgrade mlx-lm` 一直是 0.29.1，无法升级到 0.31.x
- **原因**：mlx-lm 0.31.3 需要 mlx>=0.31.2，mlx 0.31.x 需要 Python 3.10+。系统 Python 3.9.6 最高只支持 mlx 0.29.3 / mlx-lm 0.29.1
- **解决**：用 Python 3.11（Hermes venv 在 `~/.hermes/hermes-agent/venv/bin/python3.11`），或安装独立 Python 3.11+
- **影响**：Qwen3.5 支持需要 mlx_lm 0.30+，所以 Python 3.9 下只能用 Qwen3 系列
- **已验证版本**：Python 3.11.15 + mlx 0.31.2 + mlx_lm 0.31.3（2026-05-03 验证）

### mlx_lm.server 后台启动被 kill
- **现象**：`nohup python3 -m mlx_lm server ... &` 启动后立即退出，日志只到 "Loading model" 就停了
- **原因**：与 mlx_lm.server 的 `-q` 参数处理有关，后台启动时 stdin 被关闭导致异常退出
- **解决**：不用 nohup，改用 `subprocess.Popen()` 启动，或写自定义服务器包装 `mlx_lm.load()` + `generate()`（见 `scripts/mlx_server.py`）

### mlx_lm 0.31.x API 变更：temp 参数
- **现象**：`generate_step() got an unexpected keyword argument 'temp'`
- **原因**：mlx_lm 0.31.x 不再接受 `temp` 参数给 `generate()`，改为通过 sampler 控制
- **解决**：
  ```python
  from mlx_lm.sample_utils import make_sampler
  sampler = make_sampler(temp=0.7, top_p=0.9)
  response = mlx_lm.generate(model, tokenizer, prompt=prompt, max_tokens=2048, sampler=sampler)
  ```

### Qwen3 thinking tokens 吞掉所有输出
- **现象**：请求返回空 `content`，但 `completion_tokens > 0`
- **原因**：Qwen3 系列默认开启 `<think>...</think>` 思考链，thinking tokens 消耗大量 token budget。如果 `max_tokens` 太小（如 500），thinking 用完所有额度，实际回复为空
- **解决**：
  1. 默认 `max_tokens=2048`，给 thinking + 回复留够空间
  2. 生成后用正则剥离 thinking tokens：
     ```python
     import re
     response = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL)
     response = re.sub(r'<think>.*$', '', response, flags=re.DOTALL).strip()
     ```

### Qwen3.5-4B 输出 "Thinking Process" 块（重要）
- **现象**：模型输出包含大量思考过程，如 "1. **Analyze the Request:**"、"2. **Define Machine Learning:**" 等，但没有直接给出答案
- **原因**：Qwen3.5-4B 默认开启思考模式，会输出详细的推理步骤
- **影响**：测试脚本评估时，思考过程影响质量评分，导致问答能力下降 29%
- **解决**：使用多策略过滤函数提取实际答案：
  ```python
  def filter_thinking(text):
      import re
      # 移除 <think>...</think> 块
      text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
      text = re.sub(r'<think>.*$', '', text, flags=re.DOTALL)
      
      # 移除 "Thinking Process:" 行
      text = re.sub(r'^Thinking Process:\s*\n?', '', text, flags=re.MULTILINE)
      
      # 分割成行
      lines = text.split('\n')
      
      # 策略1：找到 'Drafting' 或 'Draft' 部分，提取中文答案
      drafting_start = -1
      for i, line in enumerate(lines):
          if 'Drafting' in line or 'Draft' in line:
              drafting_start = i
              break
      
      if drafting_start >= 0:
          last_draft = ''
          for i in range(drafting_start, len(lines)):
              line = lines[i]
              if '*Draft' in line or '*   *Draft' in line or 'Draft' in line:
                  # 提取中文部分
                  match = re.search(r'[\u4e00-\u9fff].*?(?=\s*\(|$)', line)
                  if match:
                      last_draft = match.group(0).strip()
          
          if last_draft:
              return last_draft
      
      # 策略2：找到 'Output:' 行
      for line in lines:
          if line.strip().startswith('Output:'):
              return line.strip()[7:].strip()
      
      # 策略3：找到 'Answer:' 行
      for line in lines:
          if line.strip().startswith('Answer:'):
              return line.strip()[7:].strip()
      
      # 策略4：找到 'Final Choice:' 行
      for line in lines:
          if 'Final Choice:' in line:
              match = re.search(r'[\u4e00-\u9fff].*?(?=\s*\(|$)', line)
              if match:
                  return match.group(0).strip()
      
      # 策略5：找到最后一行非空行（长度 > 5）
      for line in reversed(lines):
          if line.strip() and len(line.strip()) > 5:
              cleaned = re.sub(r'\(.*?\)', '', line.strip())
              cleaned = re.sub(r'\*.*?\*', '', cleaned)
              if cleaned.strip():
                  return cleaned.strip()
      
      return text.strip()
  ```
- **验证**：过滤后问答能力从 0.67 恢复到 0.75+
- **注意**：此问题与 `<think>...</think>` 标签不同，是模型输出格式问题

### ModelScope 下载中断
- **现象**：下载中断后 `._____temp/` 目录有残留
- **解决**：`snapshot_download(model_id, local_dir=target_dir)` 支持断点续传

### Qwen3.5-4B 是多模态模型
- **现象**：模型文件 8.7GB，比预期的 4B 模型大很多
- **原因**：Qwen3.5-4B 是多模态模型（`Qwen3_5ForConditionalGeneration`），包含 vision_config，不是纯文本模型
- **影响**：模型文件更大（8.7GB vs ~7.5GB），但运行内存（~4.2GB）仍可接受
- **注意**：没有官方 4-bit 量化版本，GGUF 版本存在但 mlx_lm 不支持

### 量化版本已部署
- **当前状态**：Qwen3.5-4B-4bit 已部署，4.5 bits/weight
- **位置**：`~/models/Qwen/Qwen3.5-4B-4bit/`
- **磁盘**：2.2GB（原版 8.7GB）
- **内存**：~2.6GB（原版 ~4.2GB）
- **量化命令**：`mlx_lm.convert -q --q-bits 4 --q-group-size 64 --dtype float16`
- **注意**：原版模型已删除以释放磁盘空间

### HF 缓存干扰
- **现象**：之前失败的下载留下元数据，影响后续模型加载
- **解决**：`rm -rf ~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B`
