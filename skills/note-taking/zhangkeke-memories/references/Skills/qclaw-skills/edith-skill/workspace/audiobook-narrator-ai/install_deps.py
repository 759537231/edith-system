#!/usr/bin/env python3
"""
有声书主播AI协作系统
依赖安装脚本

用法: python3 install_deps.py
"""

import sys
import subprocess
import os

def run_cmd(cmd, desc=""):
    """执行命令，失败则退出"""
    print(f"\n📦 {desc or cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ 安装失败: {desc}")
        sys.exit(1)
    print(f"✓ 完成")

def main():
    print("=" * 50)
    print("有声书主播AI协作系统 - 依赖安装")
    print("=" * 50)

    # 核心依赖
    run_cmd(
        "pip3 install fastapi uvicorn pydub edge-tts requests",
        "安装核心依赖"
    )

    # 检查 ffmpeg
    ffmpeg_check = subprocess.run(
        "which ffmpeg",
        shell=True,
        capture_output=True
    )
    if ffmpeg_check.returncode != 0:
        print("\n⚠️  ffmpeg 未安装，将无法处理音频文件")
        print("   macOS: brew install ffmpeg")
        print("   Ubuntu: sudo apt install ffmpeg")
        print("   Windows: https://ffmpeg.org/download.html")
    else:
        print("✓ ffmpeg 已安装")

    # 验证导入
    print("\n🧪 验证模块...")
    try:
        import fastapi
        import uvicorn
        import pydub
        print("✓ 所有核心模块可用")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        sys.exit(1)

    print("\n✅ 依赖安装完成！")
    print("\n启动方式:")
    print("  python3 run.py              # 默认端口 8765")
    print("  python3 run.py 8080         # 指定端口")
    print("  python3 run.py --reload     # 开发模式")

if __name__ == "__main__":
    main()