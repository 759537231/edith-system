#!/usr/bin/env python3
"""
检查 MLX 模型状态
"""

import os
import sys

MODEL_PATH = "~/.cache/huggingface/hub/models--RepublicOfKorokke--Qwen3.5-4B-mlx-vlm-mxfp4"

def check_model():
    expanded_path = os.path.expanduser(MODEL_PATH)
    
    if os.path.exists(expanded_path):
        size = get_dir_size(expanded_path)
        print(f"✅ 模型已下载: {MODEL_PATH}")
        print(f"   大小: {size:.1f} GB")
        return True
    else:
        print(f"❌ 模型未找到: {MODEL_PATH}")
        print("   请先运行 python3 scripts/load_model.py")
        return False

def get_dir_size(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total / (1024**3)

if __name__ == "__main__":
    check_model()
