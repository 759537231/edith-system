#!/usr/bin/env python3
"""
测试图片理解功能
"""

import sys
import os

def load_model():
    """加载 MLX 模型"""
    print("正在加载模型...")
    
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    
    from mlx_vlm import load
    
    model_id = "RepublicOfKorokke/Qwen3.5-4B-mlx-vlm-mxfp4"
    model, processor = load(model_id)
    print("✅ 模型加载成功！")
    
    return model, processor

def understand_image(model, processor, image_path, prompt):
    """理解图片"""
    from mlx_vlm import generate
    from PIL import Image
    
    image = Image.open(image_path)
    result = generate(model, processor, prompt=prompt, image=image)
    return result.text

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 test_image.py <图片路径> <问题>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    prompt = sys.argv[2]
    
    if not os.path.exists(image_path):
        print(f"❌ 图片不存在: {image_path}")
        sys.exit(1)
    
    # 加载模型
    model, processor = load_model()
    
    # 理解图片
    print(f"\n图片: {image_path}")
    print(f"问题: {prompt}")
    print("分析中...")
    
    response = understand_image(model, processor, image_path, prompt)
    print(f"\n结果: {response}")
