#!/usr/bin/env python3
"""
加载 MLX 模型并测试对话
"""

import sys
import os

def load_model():
    """加载 MLX 模型"""
    print("正在加载模型...")
    
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    
    from mlx_vlm import load
    
    model_id = "RepublicOfKorokke/Qwen3.5-4B-mlx-vlm-mxfp4"
    print(f"模型ID: {model_id}")
    
    model, processor = load(model_id)
    print("✅ 模型加载成功！")
    
    return model, processor

def chat(model, processor, prompt):
    """处理对话请求（张二壳身份）"""
    from mlx_vlm import generate

    # 导入张二壳 system prompt
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from system_prompt import SYSTEM_PROMPT
        full_prompt = SYSTEM_PROMPT + "\n\n## 用户问题\n" + prompt
        print("✅ 张二壳 system prompt 已加载")
    except Exception:
        full_prompt = prompt
        print("⚠️ system prompt 加载失败，使用裸 prompt")

    result = generate(model, processor, prompt=full_prompt)
    return result.text

if __name__ == "__main__":
    # 加载模型
    model, processor = load_model()
    
    # 测试对话
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        print(f"\n用户: {prompt}")
        response = chat(model, processor, prompt)
        print(f"AI: {response}")
    else:
        print("\n用法: python3 chat.py <问题>")
