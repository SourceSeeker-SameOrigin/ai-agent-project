"""
测试按键处理
"""

import pygame
import sys

# 初始化pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("按键测试")

clock = pygame.time.Clock()

# 按键状态
key_states = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
    pygame.K_DOWN: False
}

print("按键测试开始...")
print("按左箭头、右箭头、下箭头测试，按ESC退出")

running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                key_states[pygame.K_LEFT] = True
                print("左箭头按下")
            elif event.key == pygame.K_RIGHT:
                key_states[pygame.K_RIGHT] = True
                print("右箭头按下")
            elif event.key == pygame.K_DOWN:
                key_states[pygame.K_DOWN] = True
                print("下箭头按下")
            elif event.key == pygame.K_UP:
                print("上箭头按下")
            elif event.key == pygame.K_SPACE:
                print("空格键按下")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                key_states[pygame.K_LEFT] = False
                print("左箭头释放")
            elif event.key == pygame.K_RIGHT:
                key_states[pygame.K_RIGHT] = False
                print("右箭头释放")
            elif event.key == pygame.K_DOWN:
                key_states[pygame.K_DOWN] = False
                print("下箭头释放")
    
    # 检查按键状态
    if key_states[pygame.K_LEFT]:
        print("左箭头保持按下")
    if key_states[pygame.K_RIGHT]:
        print("右箭头保持按下")
    if key_states[pygame.K_DOWN]:
        print("下箭头保持按下")
    
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(10)  # 降低帧率以便观察输出

pygame.quit()
sys.exit()