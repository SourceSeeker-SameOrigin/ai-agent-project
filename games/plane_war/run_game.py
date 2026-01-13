#!/usr/bin/env python3
"""
飞机大战游戏启动脚本
运行此文件启动游戏
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import main
    print("=" * 50)
    print("飞机大战游戏 - Plane War Game")
    print("=" * 50)
    print("游戏控制说明：")
    print("  方向键/WASD: 移动飞机")
    print("  空格键: 射击")
    print("  ESC键: 退出游戏")
    print("  R键: 重新开始游戏")
    print("=" * 50)
    print("正在启动游戏...")
    
    # 运行游戏
    main()
    
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖已安装：")
    print("  pip install pygame")
    print("或者运行：python -m pip install pygame")
    
except Exception as e:
    print(f"游戏运行错误: {e}")
    print("请检查游戏文件是否完整。")