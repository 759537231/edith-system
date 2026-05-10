#!/usr/bin/env python3.11
"""
张二壳 · OpenAI 兼容 API 服务器（轻量版）
使用 mlx_lm 0.31.x + Python 3.11，无需 FastAPI/uvicorn 依赖。

启动：
  /Users/qianmo/.hermes/hermes-agent/venv/bin/python3.11 ~/models/mlx_server.py &

端口：8080
"""

import json
import time
import uuid
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

import mlx_lm
from mlx_lm.sample_utils import make_sampler

MODEL_PATH = "/Users/qianmo/models/Qwen/Qwen3-4B"
PORT = 8080

print(f"Loading model from {MODEL_PATH}...", flush=True)
model, tokenizer = mlx_lm.load(MODEL_PATH)
print("Model loaded!", flush=True)
print(f"Server running on http://127.0.0.1:{PORT}", flush=True)


def strip_thinking(text: str) -> str:
    """Remove <think>...</think> blocks, handling incomplete tags."""
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'<think>.*$', '', text, flags=re.DOTALL)
    return text.strip()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._json_response(200, {"status": "ok"})
        elif self.path == "/v1/models":
            self._json_response(200, {
                "data": [{"id": "qwen3-4b", "object": "model", "owned_by": "local"}]
            })
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path != "/v1/chat/completions":
            self.send_response(404)
            self.end_headers()
            return

        try:
            body = self._read_body()
            messages = body.get("messages", [])
            # Default 2048 — thinking tokens eat a big chunk
            max_tokens = body.get("max_tokens", 2048)
            temperature = body.get("temperature", 0.7)
            top_p = body.get("top_p", 0.9)

            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            sampler = make_sampler(temp=temperature, top_p=top_p)

            start_time = time.time()
            raw_response = mlx_lm.generate(
                model, tokenizer, prompt=prompt,
                max_tokens=max_tokens,
                sampler=sampler
            )
            elapsed = time.time() - start_time

            response = strip_thinking(raw_response)
            response_tokens = len(tokenizer.encode(response)) if response else 0

            print(f"[{elapsed:.1f}s] {response_tokens} tok ({response_tokens/elapsed:.1f} tok/s)", flush=True)

            result = {
                "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": body.get("model", "qwen3-4b"),
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": response},
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": len(tokenizer.encode(prompt)),
                    "completion_tokens": response_tokens,
                    "total_tokens": len(tokenizer.encode(prompt)) + response_tokens
                }
            }
            self._json_response(200, result)

        except Exception as e:
            import traceback
            traceback.print_exc()
            self._json_response(500, {"error": str(e)})

    def _read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(content_length))

    def _json_response(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    server.serve_forever()
