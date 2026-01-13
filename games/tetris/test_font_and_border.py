"""
测试俄罗斯方块游戏的中文字体和边界问题
"""

import pygame
import sys
import config
from ui import GameUI

def test_font():
    """测试字体显示"""
    pygame.init()
    
    # 创建测试窗口
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("字体测试")
    
    # 创建UI实例
    ui = GameUI(screen)
    
    # 测试字体渲染
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # 清屏
        screen.fill((0, 0, 0))
        
        # 测试各种文本渲染
        test_texts = [
            ("俄罗斯方块", (100, 100)),
            ("分数", (100, 150)),
            ("等级", (100, 200)),
            ("消除行数", (100, 250)),
            ("游戏时间", (100, 300)),
            ("下一个", (100, 350)),
            ("游戏暂停", (100, 400)),
            ("游戏结束", (100, 450)),
            ("按R键重新开始", (100, 500))
        ]
        
        for text, pos in test_texts:
            # 尝试渲染
            try:
                rendered = ui.font.render(text, True, (255, 255, 255))
                screen.blit(rendered, pos)
            except:
                # 如果渲染失败，显示错误信息
                error_text = f"渲染失败: {text}"
                error_rendered = pygame.font.SysFont(None, 24).render(error_text, True, (255, 0, 0))
                screen.blit(error_rendered, pos)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

def test_border_issue():
    """测试边界问题"""
    print("测试边界问题...")
    
    # 检查配置中的边界设置
    print(f"游戏区域设置:")
    print(f"  GRID_WIDTH: {config.GRID_WIDTH}")
    print(f"  GRID_HEIGHT: {config.GRID_HEIGHT}")
    print(f"  GAME_AREA_X: {config.GAME_AREA_X}")
    print(f"  GAME_AREA_Y: {config.GAME_AREA_Y}")
    print(f"  GRID_SIZE: {config.GRID_SIZE}")
    
    # 计算游戏区域的实际像素边界
    game_area_right = config.GAME_AREA_X + config.GRID_WIDTH * config.GRID_SIZE
    game_area_bottom = config.GAME_AREA_Y + config.GRID_HEIGHT * config.GRID_SIZE
    
    print(f"游戏区域像素边界:")
    print(f"  左边界: {config.GAME_AREA_X}")
    print(f"  右边界: {game_area_right}")
    print(f"  上边界: {config.GAME_AREA_Y}")
    print(f"  下边界: {game_area_bottom}")
    
    # 检查屏幕边界
    print(f"屏幕边界:")
    print(f"  屏幕宽度: {config.SCREEN_WIDTH}")
    print(f"  屏幕高度: {config.SCREEN_HEIGHT}")
    
    # 检查是否超出边界
    if game_area_right > config.SCREEN_WIDTH:
        print(f"⚠️  警告: 游戏区域右边界超出屏幕边界 ({game_area_right} > {config.SCREEN_WIDTH})")
    
    if game_area_bottom > config.SCREEN_HEIGHT:
        print(f"⚠️  警告: 游戏区域下边界超出屏幕边界 ({game_area_bottom} > {config.SCREEN_HEIGHT})")

if __name__ == "__main__":
    print("开始测试俄罗斯方块游戏问题...")
    print("=" * 50)
    
    # 测试边界问题
    test_border_issue()
    
    print("\n" + "=" * 50)
    print("开始字体测试...")
    print("按ESC键退出字体测试窗口")
    
    # 测试字体
    test_font()