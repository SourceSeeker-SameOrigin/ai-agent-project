#!/usr/bin/env python3
"""
列出系统中所有可用的字体
"""

import pygame

pygame.init()

print("=" * 80)
print("🔍 系统中所有可用的字体（前 100 个）：")
print("=" * 80)

all_fonts = pygame.font.get_fonts()
print(f"\n总共找到 {len(all_fonts)} 个字体\n")

# 显示前100个
for i, font in enumerate(all_fonts[:100], 1):
    print(f"{i:3d}. {font}")

print("\n" + "=" * 80)
print("🔍 搜索可能的中文字体（包含关键字）：")
print("=" * 80)

keywords = ['ping', 'fang', 'hei', 'song', 'kai', 'yahei', 'gothic', 'sans', 'mincho']
chinese_fonts = []

for font in all_fonts:
    for keyword in keywords:
        if keyword in font.lower():
            chinese_fonts.append(font)
            break

if chinese_fonts:
    print(f"\n找到 {len(chinese_fonts)} 个可能的中文字体：\n")
    for i, font in enumerate(chinese_fonts, 1):
        print(f"{i:2d}. {font}")
        # 测试渲染
        try:
            test_font = pygame.font.SysFont(font, 24)
            test_surface = test_font.render("测试中文", True, (255, 255, 255))
            if test_surface.get_width() > 0:
                print(f"    ✅ 可以渲染中文")
            else:
                print(f"    ❌ 无法渲染中文")
        except Exception as e:
            print(f"    ❌ 错误: {e}")
else:
    print("\n❌ 未找到任何可能的中文字体")

pygame.quit()

