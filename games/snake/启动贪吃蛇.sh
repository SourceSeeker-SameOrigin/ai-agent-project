#!/bin/bash

echo "====================================="
echo "🐍 启动贪吃蛇游戏"
echo "====================================="

# 获取脚本所在目录的父目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "📁 项目目录: $PROJECT_ROOT"

# 激活虚拟环境
if [ -d "$PROJECT_ROOT/venv" ]; then
    echo "✅ 激活虚拟环境..."
    source "$PROJECT_ROOT/venv/bin/activate"
else
    echo "⚠️  未找到虚拟环境，使用系统 Python"
fi

# 检查 pygame
echo "🔍 检查 pygame..."
python -c "import pygame" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ pygame 未安装"
    echo "📦 安装 pygame..."
    pip install pygame
fi

# 进入项目根目录
cd "$PROJECT_ROOT"

# 启动游戏
echo "====================================="
echo "🚀 启动游戏..."
echo "====================================="
python run_snake_game.py

echo ""
echo "====================================="
echo "👋 游戏已退出"
echo "====================================="

