@echo off
echo 启动飞机射击游戏...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.6+
    pause
    exit /b 1
)

REM 检查Pygame是否安装
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo Pygame未安装，正在安装...
    pip install pygame
    if errorlevel 1 (
        echo 安装Pygame失败，请手动安装: pip install pygame
        pause
        exit /b 1
    )
)

REM 运行游戏
echo 正在启动游戏...
python main.py

pause