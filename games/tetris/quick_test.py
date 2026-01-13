"""
快速测试修复
"""

import pygame
import sys

# 测试中文显示
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("中文测试")

# 测试字体
font_names = ["simhei", "simsun", "microsoftyahei", "fangsong", "arial", None]
fonts = []

for font_name in font_names:
    try:
        if font_name:
            font = pygame.font.SysFont(font_name, 24)
        else:
            font = pygame.font.SysFont(None, 24)
        text = font.render("俄罗斯方块测试", True, (255, 255, 255))
        fonts.append((font_name, font, text))
        print(f"字体 '{font_name}' 可用")
    except Exception as e:
        print(f"字体 '{font_name}' 不可用: {e}")

# 测试按键
print("\n按键测试：")
print("按左箭头、右箭头、下箭头测试")
print("按ESC退出")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                print("左箭头按下 - OK")
            elif event.key == pygame.K_RIGHT:
                print("右箭头按下 - OK")
            elif event.key == pygame.K_DOWN:
                print("下箭头按下 - OK")
            elif event.key == pygame.K_UP:
                print("上箭头按下 - OK")
            elif event.key == pygame.K_SPACE:
                print("空格键按下 - OK")
    
    # 显示中文文本
    screen.fill((0, 0, 50))
    
    y = 50
    for font_name, font, text_surface in fonts:
        label = font.render(f"字体: {font_name}", True, (200, 200, 200))
        screen.blit(label, (50, y))
        screen.blit(text_surface, (250, y))
        y += 40
    
    pygame.display.flip()

pygame.quit()
sys.exit()

print("\n测试完成！")