#!/bin/bash
# 音频计费系统 - 简单启动脚本

export PATH="$HOME/.local/bin:$PATH"

# 获取脚本目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 使用 Python 运行
python3 "$SCRIPT_DIR/audio_billing.py" "$@"
