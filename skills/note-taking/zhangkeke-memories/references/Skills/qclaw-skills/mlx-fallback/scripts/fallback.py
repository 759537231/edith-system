#!/usr/bin/env python3
"""
MLX Fallback 脚本
云API失败时自动切换到本地 Qwen3.5-4B MLX 模型
"""

import sys
import os
import traceback

# 设置镜像源
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

def try_cloud_api(prompt, image_path=None):
    """
    尝试调用云API
    返回: (成功=True, 结果或错误信息)
    """
    try:
        # 这里放云API调用逻辑
        # 目前用占位符，等QClaw支持时替换
        raise Exception("云API不可用，触发fallback")
    except Exception as e:
        return False, str(e)

def call_local_mlx(prompt, image_path=None):
    """
    调用本地 MLX 模型
    """
    print("📡 切换到本地模型...")

    from mlx_vlm import load, generate
    from PIL import Image

    # 导入张二壳 system prompt
    try:
        from system_prompt import SYSTEM_PROMPT
        full_prompt = SYSTEM_PROMPT + "\n\n## 用户问题\n" + prompt
        print("✅ 张二壳 system prompt 已加载")
    except Exception:
        full_prompt = prompt
        print("⚠️ system prompt 加载失败，使用裸 prompt")

    model_id = "RepublicOfKorokke/Qwen3.5-4B-mlx-vlm-mxfp4"

    # 检查模型是否已加载（全局变量）
    global model_cache
    if model_cache is None:
        print("🔄 加载本地模型...")
        model_cache, processor_cache = load(model_id)
        print("✅ 本地模型加载完成")

    model, processor = model_cache, processor_cache

    if image_path:
        # 图片理解模式
        print(f"🖼️ 分析图片: {image_path}")
        image = Image.open(image_path)
        result = generate(model, processor, prompt=full_prompt, image=image)
    else:
        # 纯文本模式
        result = generate(model, processor, prompt=full_prompt)

    return True, result.text

# 全局缓存
model_cache = None
processor_cache = None

def chat_with_fallback(prompt, image_path=None):
    """
    带自动fallback的对话
    """
    # 第一步：尝试云API
    print("🌐 尝试云API...")
    success, result = try_cloud_api(prompt, image_path)
    
    if success:
        print("✅ 云API成功")
        return result
    else:
        print(f"⚠️ 云API失败: {result}")
    
    # 第二步：fallback到本地模型
    success, result = call_local_mlx(prompt, image_path)
    
    if success:
        print("✅ 本地模型成功")
        return result
    else:
        print(f"❌ 本地模型也失败: {result}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 fallback.py <问题>")
        print("  python3 fallback.py <问题> <图片路径>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    image_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"💬 问题: {prompt}")
    if image_path:
        print(f"🖼️ 图片: {image_path}")
    print()
    
    result = chat_with_fallback(prompt, image_path)
    
    if result:
        print(f"\n📝 回答:\n{result}")
    else:
        print("\n❌ 全部失败")
