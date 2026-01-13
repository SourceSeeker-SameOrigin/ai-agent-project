"""
测试俄罗斯方块游戏的问题
"""

import pygame
import sys

# 初始化pygame
pygame.init()

# 测试中文显示
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("测试中文显示")

# 测试不同字体
fonts_to_try = [
    None,  # 默认字体
    "simhei",  # 黑体
    "simsun",  # 宋体
    "microsoftyahei",  # 微软雅黑
    "arial",  # 英文字体
    "fangsong"  # 仿宋
]

# 测试文本
test_text = "俄罗斯方块测试"

for i, font_name in enumerate(fonts_to_try):
    try:
        if font_name:
            font = pygame.font.SysFont(font_name, 24)
        else:
            font = pygame.font.SysFont(None, 24)
        
        text_surface = font.render(test_text, True, (255, 255, 255))
        print(f"字体 '{font_name}' 渲染成功: {text_surface.get_size()}")
    except Exception as e:
        print(f"字体 '{font_name}' 渲染失败: {e}")

# 测试按键
print("\n测试按键输入...")
print("请按左箭头、右箭头、下箭头测试，按ESC退出")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                print("左箭头按下")
            elif event.key == pygame.K_RIGHT:
                print("右箭头按下")
            elif event.key == pygame.K_DOWN:
                print("下箭头按下")
            elif event.key == pygame.K_UP:
                print("上箭头按下")
            elif event.key == pygame.K_SPACE:
                print("空格键按下")
    
    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()
sys.exit()