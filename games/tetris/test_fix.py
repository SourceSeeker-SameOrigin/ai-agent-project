"""
测试修复效果
"""

import pygame
import config_fixed as config
from ui_fixed import GameUI

def test_font_fix():
    """测试字体修复"""
    print("测试字体修复...")
    
    pygame.init()
    
    # 初始化字体
    config.init_fonts()
    
    # 创建测试窗口
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("字体修复测试")
    
    # 创建UI实例
    ui = GameUI(screen)
    
    # 测试文本
    test_texts = [
        "俄罗斯方块",
        "分数",
        "等级",
        "消除行数",
        "游戏时间",
        "下一个",
        "游戏暂停",
        "游戏结束",
        "按R键重新开始"
    ]
    
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
        
        # 显示测试文本
        y = 20
        for text in test_texts:
            # 尝试使用小字体
            if ui.small_font:
                rendered = ui.small_font.render(text, True, (255, 255, 255))
                screen.blit(rendered, (20, y))
                y += 30
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("✅ 字体测试完成")

def test_border_fix():
    """测试边界修复"""
    print("\n测试边界修复...")
    
    # 计算游戏区域边界
    game_area_right = config.GAME_AREA_X + config.GRID_WIDTH * config.GRID_SIZE
    game_area_bottom = config.GAME_AREA_Y + config.GRID_HEIGHT * config.GRID_SIZE
    
    print(f"游戏区域边界:")
    print(f"  左上角: ({config.GAME_AREA_X}, {config.GAME_AREA_Y})")
    print(f"  右下角: ({game_area_right}, {game_area_bottom})")
    print(f"  宽度: {config.GRID_WIDTH * config.GRID_SIZE} 像素")
    print(f"  高度: {config.GRID_HEIGHT * config.GRID_SIZE} 像素")
    
    # 检查是否超出屏幕
    if game_area_right <= config.SCREEN_WIDTH and game_area_bottom <= config.SCREEN_HEIGHT:
        print("✅ 游戏区域在屏幕范围内")
    else:
        print("❌ 游戏区域超出屏幕范围")
    
    # 测试方块位置
    print(f"\n方块位置测试:")
    print(f"  方块大小: {config.GRID_SIZE} 像素")
    print(f"  网格宽度: {config.GRID_WIDTH} 个方块")
    print(f"  网格高度: {config.GRID_HEIGHT} 个方块")
    
    # 测试底部边界
    last_block_y = config.GRID_HEIGHT - 1
    last_block_pixel_y = config.GAME_AREA_Y + last_block_y * config.GRID_SIZE
    block_bottom = last_block_pixel_y + config.GRID_SIZE
    
    print(f"  最后一个方块的Y坐标: {last_block_y}")
    print(f"  最后一个方块的像素Y坐标: {last_block_pixel_y}")
    print(f"  方块底部像素Y坐标: {block_bottom}")
    print(f"  游戏区域底部像素Y坐标: {game_area_bottom}")
    
    if block_bottom <= game_area_bottom:
        print("✅ 方块底部在游戏区域内")
    else:
        print("❌ 方块底部超出游戏区域")

def test_collision_logic():
    """测试碰撞检测逻辑"""
    print("\n测试碰撞检测逻辑...")
    
    # 模拟碰撞检测
    print("碰撞检测规则:")
    print("  1. x < 0 或 x >= GRID_WIDTH: 碰撞")
    print("  2. y >= GRID_HEIGHT: 碰撞 (注意：y < 0 不算碰撞，因为方块可以从上方进入)")
    print("  3. 如果 y >= 0 且 grid[y][x] != 0: 碰撞")
    
    # 测试边界情况
    test_cases = [
        ("左上角", -1, -1, True),
        ("右上角", config.GRID_WIDTH, -1, True),
        ("左下角", -1, config.GRID_HEIGHT, True),
        ("右下角", config.GRID_WIDTH, config.GRID_HEIGHT, True),
        ("正常位置", 5, 5, False),
        ("底部边界", 5, config.GRID_HEIGHT - 1, False),
        ("超出底部", 5, config.GRID_HEIGHT, True),
    ]
    
    print("\n边界测试:")
    for name, x, y, expected in test_cases:
        x_check = x < 0 or x >= config.GRID_WIDTH
        y_check = y >= config.GRID_HEIGHT
        result = x_check or y_check
        status = "✅" if result == expected else "❌"
        print(f"  {status} {name}: ({x}, {y}) -> 碰撞: {result} (期望: {expected})")

if __name__ == "__main__":
    print("开始测试修复效果...")
    print("=" * 50)
    
    # 测试边界修复
    test_border_fix()
    
    # 测试碰撞检测逻辑
    test_collision_logic()
    
    print("\n" + "=" * 50)
    print("开始字体测试...")
    print("按ESC键退出测试窗口")
    
    # 测试字体修复
    test_font_fix()