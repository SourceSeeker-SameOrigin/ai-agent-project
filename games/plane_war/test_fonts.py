"""
测试字体初始化
"""

import pygame
import sys
import os

# 初始化pygame
pygame.init()

# 测试字体初始化
print("测试字体初始化...")

# 测试1：检查pygame.font.get_fonts()
print("\n1. 检查系统可用字体:")
available_fonts = pygame.font.get_fonts()
print(f"系统中有 {len(available_fonts)} 个可用字体")

# 检查常见中文字体
chinese_fonts = [
    'stheitimedium',       # macOS 华文黑体 Medium
    'stheitilight',        # macOS 华文黑体 Light
    'hiraginosansgb',      # macOS 冬青黑体
    'songti',              # macOS 宋体
    'applesdgothicneo',    # macOS Apple SD Gothic Neo
    'microsoftyahei',      # Windows 微软雅黑
    'microsoftsansserif',  # Windows Microsoft Sans Serif
    'simhei',              # Windows 黑体
    'simsun',              # Windows 宋体
    'arialunicode',        # Arial Unicode（支持中文）
]

print("\n2. 检查中文字体可用性:")
for font in chinese_fonts:
    if font in available_fonts:
        print(f"✅ {font} 可用")
    else:
        print(f"❌ {font} 不可用")

# 测试3：尝试创建字体
print("\n3. 测试字体创建:")
try:
    # 尝试使用第一个可用的中文字体
    font_name = None
    for font in chinese_fonts:
        if font in available_fonts:
            font_name = font
            break
    
    if font_name:
        print(f"使用字体: {font_name}")
        test_font = pygame.font.SysFont(font_name, 36)
        print(f"✅ 字体创建成功: {test_font}")
    else:
        print("⚠️  没有找到中文字体，使用默认字体")
        test_font = pygame.font.SysFont(None, 36)
        print(f"✅ 默认字体创建成功: {test_font}")
        
except Exception as e:
    print(f"❌ 字体创建失败: {e}")

# 测试4：测试渲染文本
print("\n4. 测试文本渲染:")
try:
    if 'test_font' in locals():
        text_surface = test_font.render("测试中文", True, (255, 255, 255))
        print(f"✅ 文本渲染成功: {text_surface.get_size()}")
    else:
        print("⚠️  没有可用的字体进行测试")
except Exception as e:
    print(f"❌ 文本渲染失败: {e}")

print("\n测试完成！")