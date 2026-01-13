@echo off
REM 俄罗斯方块游戏启动脚本（Windows）

echo 🎮 启动俄罗斯方块游戏...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查Pygame是否安装
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Pygame未安装，正在安装...
    pip install pygame
    if errorlevel 1 (
        echo ❌ Pygame安装失败，请手动安装: pip install pygame
        pause
        exit /b 1
    )
    echo ✅ Pygame安装成功
)

REM 运行游戏
echo 🚀 启动游戏...
echo 控制说明:
echo   ← → : 左右移动
echo   ↑   : 旋转
echo   ↓   : 加速下落
echo   空格 : 硬降落
echo   P   : 暂停/继续
echo   R   : 重新开始
echo   ESC : 退出游戏
echo.
echo 游戏即将启动...
echo.

python main.py

pause