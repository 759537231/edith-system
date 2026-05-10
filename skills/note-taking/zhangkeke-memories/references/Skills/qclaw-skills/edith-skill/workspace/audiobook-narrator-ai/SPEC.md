"""
有声书主播AI协作系统 - 技术方案
Audiobook Narrator AI Collaboration System

版本: v0.1.0
日期: 2026-04-22
作者: 伊迪丝·工部

架构概述:
  REST API + 异步任务队列 + 可插拔TTS引擎 + 音频拼接

技术栈:
  - 后端: Python 3.11+ / FastAPI / Uvicorn
  - TTS: Edge-TTS (主) / Azure TTS (备) / CosyVoice (离线)
  - 音频: pydub / ffmpeg
  - 前端: Bootstrap5 + htmx (零构建)
  - 数据: JSON文件存储 (SQLite可选)

核心原则:
  ① 先跑通再优化
  ② 先找现成方案，再考虑自己写
  ③ 写完必测试
  ④ 防御性编程（编码/路径空格/网络中断）
"""

from .project_manager import ProjectManager
from .content_pipeline import ContentPipeline
from .tts_orchestrator import TTSOrchestrator
from .audio_assembler import AudioAssembler

__version__ = "0.1.0"
__all__ = [
    "ProjectManager",
    "ContentPipeline",
    "TTSOrchestrator",
    "AudioAssembler",
]