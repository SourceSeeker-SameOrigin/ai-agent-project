"""
测试键盘控制和中文字体问题
"""

import pygame
import sys
import time

def test_keyboard():
    """测试键盘控制"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("键盘控制测试")
    clock = pygame.time.Clock()
    
    # 测试中文字体
    print("测试中文字体...")
    try:
        # 尝试加载中文字体
        font_name = None
        chinese_fonts = [
            'stheitimedium', 'stheitilight', 'hiraginosansgb',
            'songti', 'applesdgothicneo', 'microsoftsansserif',
            'arialunicode'
        ]
        
        available_fonts = pygame.font.get_fonts()
        print(f"可用字体数量: {len(available_fonts)}")
        
        for font in chinese_fonts:
            if font in available_fonts:
                font_name = font
                print(f"找到中文字体: {font}")
                break
        
        if font_name:
            font_obj = pygame.font.SysFont(font_name, 36)
            print(f"字体对象创建成功: {font_obj}")
        else:
            font_obj = pygame.font.SysFont(None, 36)
            print("使用默认字体")
    except Exception as e:
        print(f"字体创建失败: {e}")
        font_obj = pygame.font.SysFont(None, 36)
    
    # 测试文本
    test_text = font_obj.render("测试中文字体: 飞机大战", True, (255, 255, 255))
    
    # 玩家位置
    player_x = 400
    player_y = 300
    player_speed = 5
    
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
        
        # 测试方向键
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
            print("左箭头按下")
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
            print("右箭头按下")
        if keys[pygame.K_UP]:
            player_y -= player_speed
            print("上箭头按下")
        if keys[pygame.K_DOWN]:
            player_y += player_speed
            print("下箭头按下")
        
        # 边界检查
        player_x = max(0, min(player_x, 800 - 50))
        player_y = max(0, min(player_y, 600 - 50))
        
        # 绘制
        screen.fill((0, 0, 0))
        
        # 绘制玩家
        pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, 50, 50))
        
        # 绘制文本
        screen.blit(test_text, (50, 50))
        
        # 绘制说明
        instruction = font_obj.render("按方向键移动方块，按ESC退出", True, (255, 255, 255))
        screen.blit(instruction, (50, 100))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    test_keyboard()