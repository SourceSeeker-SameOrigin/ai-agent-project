#!/bin/bash

# 游戏开发Agent启动脚本 - V2版本
# 兼容 LangChain 0.3.x

echo "🎮 游戏开发Agent - V2版本 (LangChain 0.3.x 兼容)"
echo "================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装 Python 3"
    exit 1
fi

# 获取脚本所在目录并进入项目根目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/../.."

# 检查虚拟环境
if [ -d "venv" ]; then
    echo "✅ 找到虚拟环境"
    source venv/bin/activate
else
    echo "⚠️  未找到虚拟环境，使用系统Python"
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 文件"
    echo "创建 .env 文件并添加您的 API Key："
    echo "DEEPSEEK_API_KEY=your_key_here"
    echo ""
fi

# 检查依赖
echo "📦 检查依赖..."
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "❌ 缺少 streamlit，正在安装..."
    pip install streamlit
fi

if ! python3 -c "import langchain" 2>/dev/null; then
    echo "❌ 缺少 langchain，正在安装..."
    pip install -r requirements.txt
fi

echo "🔄 完全重启游戏开发Agent"
echo "================================"

# 停止所有streamlit进程
echo "停止所有Streamlit进程..."
pkill -9 -f "streamlit run web_ui/web_ui_game_dev.py" 2>/dev/null || true
sleep 1

# 清除Python缓存
echo "清除Python缓存..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
echo "   ✅ 缓存已清除"

# 清除Streamlit缓存
echo "清除Streamlit缓存..."
rm -rf ~/.streamlit/cache 2>/dev/null || true
echo "   ✅ Streamlit缓存已清除"

# 重新启动
echo "重新启动应用..."
echo ""

# 启动 Web UI
echo ""
echo "🚀 启动 Web UI (V2版本 - LangChain 0.3.x兼容)..."
echo "================================"
echo ""
echo "📝 提示:"
echo "  1. 浏览器会自动打开"
echo "  2. 在侧边栏输入 API 密钥"
echo "  3. V2版本使用 stream_mode='updates' 实现流式输出"
echo "  4. 完全兼容 LangChain 0.3.x"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

streamlit run web_ui/web_ui_game.py

