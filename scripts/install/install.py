"""
安装脚本 - 检查并安装游戏依赖
"""

import sys
import subprocess

def check_pygame():
    """检查pygame是否已安装"""
    try:
        import pygame
        print("✅ Pygame 已安装")
        return True
    except ImportError:
        print("❌ Pygame 未安装")
        return False

def install_pygame():
    """安装pygame"""
    print("正在安装 Pygame...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("✅ Pygame 安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ Pygame 安装失败")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("飞机射击游戏 - 依赖检查")
    print("=" * 50)
    
    if not check_pygame():
        print("\n需要安装 Pygame 才能运行游戏")
        response = input("是否安装 Pygame? (y/n): ")
        if response.lower() == 'y':
            if install_pygame():
                print("\n✅ 所有依赖已安装完成!")
                print("现在可以运行游戏了:")
                print("  python main.py")
            else:
                print("\n❌ 安装失败，请手动安装:")
                print("  pip install pygame")
        else:
            print("\n❌ 游戏需要 Pygame 才能运行")
            print("请手动安装: pip install pygame")
    else:
        print("\n✅ 所有依赖已满足!")
        print("现在可以运行游戏了:")
        print("  python main.py")
    
    print("\n游戏控制说明:")
    print("  - 方向键或WASD: 移动飞机")
    print("  - 空格键: 发射子弹")
    print("  - ESC键: 退出游戏")
    print("  - R键: 游戏结束后重新开始")

if __name__ == "__main__":
    main()