#!/usr/bin/env python3
"""
安装游戏依赖
"""

import sys
import subprocess
import os

def install_package(package):
    """安装Python包"""
    print(f"正在安装 {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} 安装成功")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ {package} 安装失败")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("飞机射击游戏 - 依赖安装")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("错误: 需要Python 3.6或更高版本")
        return False
    
    print(f"Python版本: {sys.version}")
    
    # 安装依赖
    dependencies = ["pygame==2.5.2"]
    
    success = True
    for dep in dependencies:
        if not install_package(dep):
            success = False
    
    if success:
        print("\n" + "=" * 50)
        print("所有依赖安装完成！")
        print("现在可以运行游戏了:")
        print("python main.py")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("部分依赖安装失败，请手动安装:")
        print("pip install pygame==2.5.2")
        print("=" * 50)
    
    return success

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)