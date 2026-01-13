#!/bin/bash

echo "启动飞机射击游戏..."
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.6+"
    exit 1
fi

# 检查Pygame是否安装
if ! python3 -c "import pygame" &> /dev/null; then
    echo "Pygame未安装，正在安装..."
    pip3 install pygame
    if [ $? -ne 0 ]; then
        echo "安装Pygame失败，请手动安装: pip3 install pygame"
        exit 1
    fi
fi

# 运行游戏
echo "正在启动游戏..."
python3 main.py