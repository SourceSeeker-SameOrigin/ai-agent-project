#!/bin/bash

# 俄罗斯方块游戏启动脚本

echo "🎮 启动俄罗斯方块游戏..."
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查Pygame是否安装
if ! python3 -c "import pygame" &> /dev/null; then
    echo "⚠️  Pygame未安装，正在安装..."
    pip3 install pygame
    if [ $? -ne 0 ]; then
        echo "❌ Pygame安装失败，请手动安装: pip install pygame"
        exit 1
    fi
    echo "✅ Pygame安装成功"
fi

# 运行游戏
echo "🚀 启动游戏..."
echo "控制说明:"
echo "  ← → : 左右移动"
echo "  ↑   : 旋转"
echo "  ↓   : 加速下落"
echo "  空格 : 硬降落"
echo "  P   : 暂停/继续"
echo "  R   : 重新开始"
echo "  ESC : 退出游戏"
echo ""
echo "游戏即将启动..."

python3 main.py