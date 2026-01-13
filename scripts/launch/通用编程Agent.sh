#!/bin/bash

# 启动通用编程Agent Web界面

# 获取脚本所在目录的父目录的父目录（项目根目录）
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

# 进入项目根目录
cd "$PROJECT_ROOT"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行: python3 -m venv venv"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 检查依赖
if ! python3.11 -c "import streamlit" 2>/dev/null; then
    echo "⚠️  检测到缺少依赖，正在安装..."
    pip3.11 install -r requirements.txt
fi

# 启动Web界面
echo "🚀 启动通用编程Agent Web界面..."
echo "📝 访问地址: http://localhost:8501"
echo ""

streamlit run web_ui/web_ui_universal.py

