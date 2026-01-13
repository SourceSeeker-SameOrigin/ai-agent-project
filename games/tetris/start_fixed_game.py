"""
启动修复后的俄罗斯方块游戏
修复问题：
1. 控制说明没展示
2. 右侧的下一个方块不在矩形框里面
"""

import subprocess
import sys
import os

print("=" * 60)
print("启动修复后的俄罗斯方块游戏")
print("=" * 60)
print("\n修复的问题：")
print("✅ 1. 控制说明显示 - 已修复")
print("✅ 2. 下一个方块预览位置 - 已修复")
print("✅ 3. 中文乱码问题 - 已修复")
print("✅ 4. 箭头按键不响应 - 已修复")
print("✅ 5. 方块超出边界 - 已修复")
print("\n控制说明：")
print("← → : 左右移动")
print("↑ : 旋转")
print("↓ : 加速下落")
print("空格 : 硬降落")
print("P : 暂停/继续")
print("R : 重新开始")
print("ESC : 退出游戏")
print("\n" + "=" * 60)

# 检查依赖
try:
    import pygame
    print("✓ pygame 已安装")
except ImportError:
    print("✗ pygame 未安装，正在安装...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    print("✓ pygame 安装完成")

# 运行修复后的游戏
print("\n启动修复后的游戏...")
try:
    os.system("python tetris_fixed.py")
except Exception as e:
    print(f"启动游戏时出错: {e}")
    print("尝试直接运行...")
    import tetris_fixed
    tetris_fixed.main()