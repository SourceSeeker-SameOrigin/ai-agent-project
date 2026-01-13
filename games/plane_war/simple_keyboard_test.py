"""
简单键盘控制测试
"""

import pygame
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("键盘测试")
    clock = pygame.time.Clock()
    
    x, y = 200, 150
    speed = 5
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print(f"按键按下: {pygame.key.name(event.key)}")
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # 获取按键状态
        keys = pygame.key.get_pressed()
        
        # 方向键控制
        if keys[pygame.K_LEFT]:
            x -= speed
            print("左箭头")
        if keys[pygame.K_RIGHT]:
            x += speed
            print("右箭头")
        if keys[pygame.K_UP]:
            y -= speed
            print("上箭头")
        if keys[pygame.K_DOWN]:
            y += speed
            print("下箭头")
        
        # 边界检查
        x = max(0, min(x, 400 - 20))
        y = max(0, min(y, 300 - 20))
        
        # 绘制
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, 20, 20))
        
        # 显示按键状态
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"位置: ({x}, {y})", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()