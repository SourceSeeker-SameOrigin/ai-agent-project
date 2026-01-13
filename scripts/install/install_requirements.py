#!/usr/bin/env python3
"""
安装贪吃蛇游戏依赖
"""

import subprocess
import sys

def install_package(package):
    """安装Python包"""
    try:
        print(f"正在安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} 安装成功")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {package} 安装失败")
        return False

def check_pygame():
    """检查Pygame是否已安装"""
    try:
        import pygame
        print(f"✅ Pygame 已安装 (版本: {pygame.version.ver})")
        return True
    except ImportError:
        print("❌ Pygame 未安装")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("贪吃蛇游戏依赖安装")
    print("=" * 50)
    
    # 检查是否已安装Pygame
    if not check_pygame():
        print("\n开始安装依赖...")
        if install_package("pygame"):
            print("\n✅ 所有依赖安装完成！")
            print("\n现在可以运行游戏:")
            print("  python run_snake_game.py")
        else:
            print("\n❌ 依赖安装失败，请手动安装:")
            print("  pip install pygame")
    else:
        print("\n✅ 所有依赖已安装！")
        print("\n现在可以运行游戏:")
        print("  python run_snake_game.py")
    
    print("=" * 50)

if __name__ == "__main__":
    main()