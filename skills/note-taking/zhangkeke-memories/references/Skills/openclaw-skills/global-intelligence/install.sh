#!/bin/bash
# global-intelligence / install.sh
# 安装脚本

echo "🌍 安装 Global Intelligence 全球局势分析系统..."

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

# 检查Python版本
python3 --version > /dev/null 2>&1 || {
    echo "❌ 错误: 需要 Python 3.8+"
    exit 1
}

# 创建数据目录
echo "📁 创建数据目录..."
mkdir -p "$SKILL_DIR/data/reports"
mkdir -p "$SKILL_DIR/data/history"
mkdir -p "$SKILL_DIR/data/vector-db"

# 设置权限
echo "🔐 设置执行权限..."
chmod +x "$SKILL_DIR/main.py"
chmod +x "$SKILL_DIR/scripts/"*.py

# 创建快捷命令
echo "🔗 创建快捷命令..."
INSTALL_DIR="${HOME}/.local/bin"
mkdir -p "$INSTALL_DIR"

cat > "$INSTALL_DIR/global-intel" << 'EOF'
#!/bin/bash
SKILL_DIR="${HOME}/.hermes/skills/note-taking/zhangkeke-memories/references/Skills/openclaw-skills/global-intelligence"
python3 "$SKILL_DIR/main.py" "$@"
EOF

chmod +x "$INSTALL_DIR/global-intel"

echo ""
echo "✅ 安装完成!"
echo ""
echo "使用方法:"
echo "  global-intel '中美AI竞争'        # 完整分析"
echo "  global-intel '俄乌局势' -q       # 快速扫描"
echo "  global-intel '台海局势' -p 高    # 高优先级报告"
echo ""
echo "报告保存位置:"
echo "  ~/.hermes/skills/note-taking/zhangkeke-memories/references/Skills/openclaw-skills/global-intelligence/data/reports/"
echo ""
