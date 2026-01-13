"""
飞机射击游戏 - 主入口文件
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game import AirplaneShooterGame

def main():
    """游戏主函数"""
    print("=" * 50)
    print("飞机射击游戏")
    print("=" * 50)
    print("游戏说明:")
    print("1. 使用方向键(← → ↑ ↓)控制飞机移动")
    print("2. 按空格键发射子弹")
    print("3. 摧毁敌机获得分数")
    print("4. 避免被敌机撞到")
    print("5. 按R键重新开始游戏")
    print("6. 按ESC键退出游戏")
    print("=" * 50)
    print("游戏启动中...")
    
    try:
        # 创建并运行游戏
        game = AirplaneShooterGame()
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")

if __name__ == "__main__":
    main()