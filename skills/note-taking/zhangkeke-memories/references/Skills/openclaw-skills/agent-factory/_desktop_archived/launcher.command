#!/bin/zsh
# Agent 工厂 桌面版启动器（双击此文件即可）
# 放在 ~/Desktop/Agent工厂.command 双击使用

LOGDIR="$HOME/Library/Logs/AgentFactory"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/launcher_$(date +%Y%m%d).log"

log() {
    echo "[$(date '+%H:%M:%S')] $1" >> "$LOGFILE"
}

APPDIR="$(dirname "$0")"

log "═══ Agent 工厂启动 ═══"

# 1. 检查 MLX API 服务（18793）
MLX_RUNNING=false
if curl -s --max-time 2 http://127.0.0.1:18793/v1/models &>/dev/null; then
    MLX_RUNNING=true
    log "✅ MLX API 服务已在运行（18793）"
fi

# 2. 如果 MLX 未运行，尝试启动
if [ "$MLX_RUNNING" = false ]; then
    log "⚙️ MLX 服务未运行，检查是否已加载..."
    # 可能是张二壳在其他端口
    if curl -s --max-time 2 http://127.0.0.1:18792/v1/models &>/dev/null; then
        log "✅ 发现张二壳 API（18792），桌面版使用 18792"
        sed -i '' 's|18793|18792|g' "$APPDIR/app.py"
        log "已切换 app.py 到 18792"
    else
        log "⚠️ 未检测到本地模型服务"
        log "请先运行：python3 ~/.qclaw/workspace/skills/mlx-fallback/scripts/api_server.py"
        osascript -e 'display alert "Agent 工厂" message "未检测到本地模型服务（18793/18792）。请先在终端运行：\npython3 ~/.qclaw/workspace/skills/mlx-fallback/scripts/api_server.py\n\n然后重新双击 Agent 工厂。"' 2>/dev/null || true
        exit 1
    fi
fi

# 3. 检查 streamlit
if ! command -v streamlit &>/dev/null; then
    log "📦 安装 streamlit..."
    pip3 install streamlit --quiet 2>> "$LOGFILE"
fi

# 4. 启动 Agent 工厂 App
log "🚀 启动 Agent 工厂（端口 8501）..."
cd "$APPDIR" && nohup streamlit run app.py \
    --server.port 8501 \
    --server.headless true \
    --browser.gatherUsageStats false \
    --browser.serverAddress "localhost" \
    &>> "$LOGDIR/app_$(date +%Y%m%d).log" &

ST_PID=$!
log "Streamlit 已启动 pid=$ST_PID"

# 5. 等待服务就绪
for i in {1..10}; do
    sleep 1
    if curl -s --max-time 1 http://localhost:8501 &>/dev/null; then
        log "✅ Agent 工厂已就绪"
        break
    fi
    [ $i -eq 10 ] && log "⚠️ Agent 工厂启动超时"
done

# 6. 自动打开浏览器
open "http://localhost:8501"
log "🌐 浏览器已打开"

osascript -e 'display notification "Agent 工厂已就绪" with title "🏭 Agent 工厂"' 2>/dev/null || true
