#!/bin/bash
# 启动 Web 界面（中国版）

echo "🚀 启动 AI Agent Web 界面（支持阿里通义千问等国内服务）"
echo "=============================================="
echo ""

# 进入项目根目录
cd "$(dirname "$0")/../.."

# 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
else
    echo "❌ 未找到虚拟环境，请先运行: python3 -m venv venv"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
if ! python -c "import streamlit" 2>/dev/null; then
    echo "⚠️  未安装 streamlit，正在安装..."
    pip install streamlit -q
fi

echo ""
echo "🌐 正在启动 Web 服务器..."
echo "💡 浏览器会自动打开，如果没有，请访问: http://localhost:8501"
echo ""
echo "⚠️  使用 Ctrl+C 停止服务"
echo "=============================================="
echo ""

# 启动 Streamlit
streamlit run web_ui/web_ui_china.py

