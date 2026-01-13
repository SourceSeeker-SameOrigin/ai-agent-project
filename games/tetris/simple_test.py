"""
简单测试俄罗斯方块游戏的问题
"""

import pygame
import sys

def test_font_simple():
    """简单测试字体"""
    pygame.init()
    
    # 创建小窗口
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("字体测试")
    
    # 尝试不同的字体
    font_names = ["simhei", "simsun", "microsoftyahei", "fangsong", "arial"]
    
    print("系统可用字体:")
    available_fonts = pygame.font.get_fonts()
    print(f"总共有 {len(available_fonts)} 个字体")
    
    # 检查我们需要的字体是否可用
    for font_name in font_names:
        if font_name in available_fonts:
            print(f"✅ {font_name} 可用")
        else:
            print(f"❌ {font_name} 不可用")
    
    # 创建字体对象
    fonts = []
    for font_name in font_names:
        try:
            font = pygame.font.SysFont(font_name, 24)
            fonts.append((font_name, font))
            print(f"✅ 成功创建字体: {font_name}")
        except Exception as e:
            print(f"❌ 创建字体 {font_name} 失败: {e}")
    
    # 如果都失败了，使用默认字体
    if not fonts:
        try:
            font = pygame.font.SysFont(None, 24)
            fonts.append(("default", font))
            print("✅ 使用默认字体")
        except Exception as e:
            print(f"❌ 默认字体也失败: {e}")
            return
    
    # 测试渲染中文
    test_texts = ["俄罗斯方块", "分数", "游戏结束", "测试中文"]
    
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
        
        y = 20
        for font_name, font in fonts:
            # 显示字体名称
            name_text = font.render(f"字体: {font_name}", True, (255, 255, 255))
            screen.blit(name_text, (20, y))
            y += 30
            
            # 测试中文渲染
            for text in test_texts:
                try:
                    rendered = font.render(text, True, (255, 255, 255))
                    screen.blit(rendered, (40, y))
                    y += 25
                except Exception as e:
                    error_text = f"渲染失败: {text}"
                    error_rendered = pygame.font.SysFont(None, 20).render(error_text, True, (255, 0, 0))
                    screen.blit(error_rendered, (40, y))
                    y += 25
            
            y += 20
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

def test_border_calculation():
    """测试边界计算"""
    print("\n边界计算测试:")
    
    # 模拟游戏配置
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    GRID_SIZE = 30
    GAME_AREA_X = 200
    GAME_AREA_Y = 50
    
    # 计算游戏区域边界
    game_area_right = GAME_AREA_X + GRID_WIDTH * GRID_SIZE
    game_area_bottom = GAME_AREA_Y + GRID_HEIGHT * GRID_SIZE
    
    print(f"游戏区域:")
    print(f"  左上角: ({GAME_AREA_X}, {GAME_AREA_Y})")
    print(f"  右下角: ({game_area_right}, {game_area_bottom})")
    print(f"  宽度: {GRID_WIDTH * GRID_SIZE} 像素")
    print(f"  高度: {GRID_HEIGHT * GRID_SIZE} 像素")
    
    # 检查方块位置
    print(f"\n方块位置检查:")
    print(f"  方块大小: {GRID_SIZE} 像素")
    print(f"  最大X坐标: {GRID_WIDTH - 1}")
    print(f"  最大Y坐标: {GRID_HEIGHT - 1}")
    
    # 检查底部边界
    print(f"\n底部边界检查:")
    print(f"  最后一个方块的Y坐标: {GRID_HEIGHT - 1}")
    print(f"  最后一个方块的像素Y坐标: {GAME_AREA_Y + (GRID_HEIGHT - 1) * GRID_SIZE}")
    print(f"  方块底部像素Y坐标: {GAME_AREA_Y + (GRID_HEIGHT - 1) * GRID_SIZE + GRID_SIZE}")
    print(f"  游戏区域底部像素Y坐标: {game_area_bottom}")
    
    # 检查是否超出
    block_bottom = GAME_AREA_Y + (GRID_HEIGHT - 1) * GRID_SIZE + GRID_SIZE
    if block_bottom > game_area_bottom:
        print(f"⚠️  警告: 方块底部超出游戏区域 ({block_bottom} > {game_area_bottom})")
        print(f"  超出: {block_bottom - game_area_bottom} 像素")
    else:
        print(f"✅ 方块底部在游戏区域内")

if __name__ == "__main__":
    print("开始测试...")
    print("=" * 50)
    
    # 测试边界计算
    test_border_calculation()
    
    print("\n" + "=" * 50)
    print("开始字体测试...")
    print("按ESC键退出测试窗口")
    
    # 测试字体
    test_font_simple()