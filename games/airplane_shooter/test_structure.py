"""
测试游戏文件结构
"""

import os

def check_file_exists(filename):
    """检查文件是否存在"""
    if os.path.exists(filename):
        print(f"✓ {filename} 存在")
        return True
    else:
        print(f"✗ {filename} 不存在")
        return False

def check_file_content(filename):
    """检查文件内容"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = len(content.split('\n'))
            print(f"  - 文件大小: {len(content)} 字符, {lines} 行")
            return True
    except Exception as e:
        print(f"  - 读取文件失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("飞机射击游戏 - 项目结构检查")
    print("=" * 50)
    
    files_to_check = [
        "config.py",
        "bullet.py", 
        "enemy.py",
        "player.py",
        "game.py",
        "main.py",
        "requirements.txt",
        "README.md",
        "run_game.bat",
        "run_game.sh"
    ]
    
    all_exists = True
    for filename in files_to_check:
        exists = check_file_exists(filename)
        if exists:
            check_file_content(filename)
        else:
            all_exists = False
    
    print("\n" + "=" * 50)
    if all_exists:
        print("✓ 所有文件都存在，项目结构完整")
        print("\n安装说明:")
        print("1. 安装依赖: pip install pygame")
        print("2. 运行游戏: python main.py")
        print("3. 或使用启动脚本: run_game.bat (Windows) 或 run_game.sh (Linux/Mac)")
    else:
        print("✗ 部分文件缺失，请检查项目结构")
    
    print("=" * 50)

if __name__ == "__main__":
    main()