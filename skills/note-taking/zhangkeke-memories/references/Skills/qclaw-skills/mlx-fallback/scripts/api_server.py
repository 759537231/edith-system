#!/usr/bin/env python3
"""
张二壳 · API 服务
OpenAI 兼容接口，QClaw 模型路由可接入
启动后监听 http://localhost:18792
"""

import os
import sys

# 始终使用 HuggingFace 镜像
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import argparse
import base64
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn

# 加载张二壳 system prompt
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from system_prompt import SYSTEM_PROMPT
    print("✅ 张二壳 system prompt 加载成功")
except Exception as e:
    SYSTEM_PROMPT = "你是张二壳，本地智能助手。"
    print(f"⚠️ system prompt 加载失败: {e}")

# ── MLX 模型 ──────────────────────────────────────────────

model_cache = None
processor_cache = None
MODEL_ID = "RepublicOfKorokke/Qwen3.5-4B-mlx-vlm-mxfp4"


def load_mlx_model():
    """加载 MLX 模型（仅调用一次，后续复用）"""
    global model_cache, processor_cache
    if model_cache is not None:
        return model_cache, processor_cache

    print(f"📡 加载 MLX 模型: {MODEL_ID} ...")
    from mlx_vlm import load
    model_cache, processor_cache = load(MODEL_ID)
    print("✅ MLX 模型加载完成，已缓存")
    return model_cache, processor_cache


def mlx_generate(prompt: str, image_base64: Optional[str] = None) -> str:
    """调用 MLX 模型生成文本"""
    from mlx_vlm import generate

    model, processor = load_mlx_model()

    if image_base64:
        from PIL import Image
        import io
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        result = generate(model, processor, prompt=prompt, image=image)
    else:
        result = generate(model, processor, prompt=prompt)

    result_text = result.text
    # 去掉思考过程，只留最终答案
    for tag in ["<think>", "</think>"]:
        result_text = result_text.replace(tag, "")
    result_text = result_text.strip()
    return result_text


# ── 记忆读取 ───────────────────────────────────────────────

MEMORY_FILE = "/Users/labixiaoxin/.qclaw/workspace/MEMORY.md"
MEMORY_DIR = "/Users/labixiaoxin/.qclaw/workspace/memory"


def get_local_memory() -> str:
    """读取本地记忆文件，供张二壳了解用户背景"""
    parts = []
    
    # 1. 读取核心记忆 MEMORY.md
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                parts.append(f"## 用户核心信息\n{content}")
        except Exception as e:
            print(f"⚠️ 读取 MEMORY.md 失败: {e}")
    
    # 2. 读取今日记忆
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    today_mem = f"{MEMORY_DIR}/{today}.md"
    if os.path.exists(today_mem):
        try:
            with open(today_mem, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                parts.append(f"## 今日事项\n{content}")
        except Exception as e:
            print(f"⚠️ 读取今日记忆失败: {e}")
    
    if parts:
        return "\n\n".join(parts) + "\n\n"
    return ""


# ── FastAPI 应用 ────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """启动时预加载模型"""
    print("🚀 张二壳 API 服务启动中...")
    try:
        load_mlx_model()
        print("✅ 张二壳已就绪")
    except Exception as e:
        print(f"⚠️ 模型预加载失败: {e}")
        print("   服务已启动，首次请求时将再次尝试加载")
    yield
    print("👋 张二壳 API 服务关闭")


app = FastAPI(
    title="张二壳 API",
    description="本地 MLX 模型 API 服务，OpenAI 兼容接口",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── 请求 / 响应模型 ─────────────────────────────────────────

class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2048
    stream: Optional[bool] = False
    image: Optional[str] = None  # base64 编码图片（可选）


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatMessage(BaseModel):
    role: str
    content: str


class Choice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[Choice]
    usage: Usage


# ── API 路由 ────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "name": "张二壳 API",
        "version": "1.0.0",
        "model": MODEL_ID,
        "status": "running",
        "endpoints": {
            "chat": "POST /v1/chat/completions",
            "health": "GET /health",
        }
    }


@app.get("/health")
async def health():
    return {"status": "ok", "model": "loaded" if model_cache else "not_loaded"}


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(req: ChatCompletionRequest):
    """OpenAI 兼容的 chat completions 接口"""
    import time

    # 1. 提取对话内容（只取最后一条 user message，history 暂不注入以避免 4B 模型循环）
    user_messages = [m.content for m in req.messages if m.role == "user"]
    if not user_messages:
        raise HTTPException(status_code=400, detail="No user message found")

    last_user_message = user_messages[-1]

    # 2. 读取本地记忆
    local_memory = get_local_memory()
    
    # 3. 构建 prompt（system + 记忆 + 当前问题）
    full_prompt = SYSTEM_PROMPT
    if local_memory:
        full_prompt += f"\n\n{local_memory}"
    full_prompt += "\n\n## 用户问题\n" + last_user_message

    # 3. 调用 MLX 模型
    print(f"🤖 张二壳处理中: {last_user_message[:50]}...")
    start = time.time()

    try:
        answer = mlx_generate(full_prompt, image_base64=req.image)
    except Exception as e:
        print(f"❌ MLX 生成失败: {e}")
        raise HTTPException(status_code=500, detail=f"MLX generation failed: {e}")

    elapsed = time.time() - start
    print(f"✅ 生成完成，耗时 {elapsed:.1f}s")

    # 4. 返回 OpenAI 兼容格式
    prompt_tokens = len(full_prompt) // 4
    completion_tokens = len(answer) // 4

    return ChatCompletionResponse(
        id=f"chatcmpl-{int(time.time()*1000)}",
        created=int(time.time()),
        model=req.model,
        choices=[Choice(
            index=0,
            message=ChatMessage(role="assistant", content=answer),
            finish_reason="stop",
        )],
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        ),
    )


# ── 启动 ───────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="张二壳 API 服务")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=18793, help="监听端口")
    args = parser.parse_args()

    print(f"""
╔══════════════════════════════════════╗
║       张二壳 · 本地智能助手 API       ║
║   端口: http://{args.host}:{args.port}        ║
║   文档: http://{args.host}:{args.port}/docs   ║
╚══════════════════════════════════════╝
    """)

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="info",
    )
