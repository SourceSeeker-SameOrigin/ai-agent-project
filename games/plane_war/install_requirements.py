#!/usr/bin/env python3
"""
安装飞机大战游戏所需依赖
"""

import sys
import subprocess
import importlib

def check_package(package_name):
    """检查包是否已安装"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """安装Python包"""
    print(f"正在安装 {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ {package_name} 安装成功")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {package_name} 安装失败")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("飞机大战游戏 - 依赖安装")
    print("=" * 50)
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("❌ 需要Python 3.6或更高版本")
        return
    
    # 检查并安装pygame
    if check_package("pygame"):
        print("✅ Pygame 已安装")
    else:
        print("❌ Pygame 未安装")
        if install_package("pygame"):
            print("✅ 所有依赖安装完成")
        else:
            print("❌ 依赖安装失败，请手动安装:")
            print("   pip install pygame")
            return
    
    print("\n" + "=" * 50)
    print("✅ 所有依赖检查通过！")
    print("可以运行游戏了。")
    print("\n运行游戏命令:")
    print("  python run_game.py")
    print("  python main.py")
    print("\n测试游戏命令:")
    print("  python test_game.py")
    print("=" * 50)

if __name__ == "__main__":
    main()