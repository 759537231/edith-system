#!/usr/bin/env python3
"""
有声书主播AI协作系统 - 启动脚本
Audiobook Narrator AI Collaboration System

用法:
  python3 run.py [port]     # 启动服务 (默认 8765)
  python3 run.py --help     # 显示帮助
"""

import sys
import os
import argparse

# 添加项目根目录到 Python 路径
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

def main():
    parser = argparse.ArgumentParser(
        description="有声书主播AI协作系统",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "port", nargs="?", type=int, default=8765,
        help="服务端口 (默认: 8765)"
    )
    parser.add_argument(
        "--host", default="0.0.0.0",
        help="监听地址 (默认: 0.0.0.0)"
    )
    parser.add_argument(
        "--reload", action="store_true",
        help="开启热重载 (开发模式)"
    )
    parser.add_argument(
        "--demo", action="store_true",
        help="启动演示模式 (使用模拟数据)"
    )
    args = parser.parse_args()

    try:
        from fastapi import FastAPI
        import uvicorn
    except ImportError:
        print("❌ 缺少依赖，请先安装:")
        print("   pip3 install fastapi uvicorn pydub edge-tts")
        sys.exit(1)

    app = FastAPI(
        title="有声书主播AI协作系统",
        version="0.1.0",
        description="主播与AI协作制作有声书"
    )

    # 导入并注册路由
    try:
        from api.routes import router as api_router
        app.include_router(api_router, prefix="/api")
        print("✓ API 路由注册成功")
    except Exception as e:
        print(f"⚠ API 路由加载失败: {e}")

    @app.get("/")
    def index():
        return {
            "name": "有声书主播AI协作系统",
            "version": "0.1.0",
            "status": "running",
            "endpoints": {
                "docs": "/docs",
                "projects": "/api/projects",
                "tasks": "/api/tasks"
            }
        }

    print(f"\n🚀 启动服务: http://{args.host}:{args.port}")
    print(f"   文档: http://localhost:{args.port}/docs")
    print(f"   热重载: {'开启' if args.reload else '关闭'}\n")

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    main()