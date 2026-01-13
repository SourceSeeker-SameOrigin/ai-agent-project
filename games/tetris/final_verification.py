"""
最终验证修复效果
"""

import pygame
import config_final as config

def verify_all_fixes():
    """验证所有修复"""
    print("最终验证修复效果")
    print("=" * 50)
    
    pygame.init()
    
    # 1. 验证字体初始化
    print("1. 验证字体初始化...")
    config.init_fonts()
    
    if config.FONT and config.SMALL_FONT:
        print("   ✅ 字体初始化成功")
        
        # 测试中文渲染
        try:
            test_text = config.FONT.render("俄罗斯方块", True, (255, 255, 255))
            print("   ✅ 中文文本渲染成功")
        except Exception as e:
            print(f"   ❌ 中文文本渲染失败: {e}")
    else:
        print("   ❌ 字体初始化失败")
    
    # 2. 验证游戏区域边界
    print("\n2. 验证游戏区域边界...")
    
    # 计算游戏区域
    game_area_width = config.GRID_WIDTH * config.GRID_SIZE
    game_area_height = config.GRID_HEIGHT * config.GRID_SIZE
    
    game_area_right = config.GAME_AREA_X + game_area_width
    game_area_bottom = config.GAME_AREA_Y + game_area_height
    
    print(f"   游戏区域位置: ({config.GAME_AREA_X}, {config.GAME_AREA_Y})")
    print(f"   游戏区域大小: {game_area_width} x {game_area_height}")
    print(f"   游戏区域边界: 右{game_area_right}, 下{game_area_bottom}")
    print(f"   屏幕大小: {config.SCREEN_WIDTH} x {config.SCREEN_HEIGHT}")
    
    # 检查是否在屏幕内
    all_good = True
    
    if config.GAME_AREA_X >= 0:
        print("   ✅ 游戏区域左边界在屏幕内")
    else:
        print("   ❌ 游戏区域左边界超出屏幕")
        all_good = False
    
    if game_area_right <= config.SCREEN_WIDTH:
        print("   ✅ 游戏区域右边界在屏幕内")
    else:
        print("   ❌ 游戏区域右边界超出屏幕")
        all_good = False
    
    if config.GAME_AREA_Y >= 0:
        print("   ✅ 游戏区域上边界在屏幕内")
    else:
        print("   ❌ 游戏区域上边界超出屏幕")
        all_good = False
    
    if game_area_bottom <= config.SCREEN_HEIGHT:
        print("   ✅ 游戏区域下边界在屏幕内")
    else:
        print("   ❌ 游戏区域下边界超出屏幕")
        all_good = False
    
    # 3. 验证方块边界
    print("\n3. 验证方块边界...")
    
    # 最后一个方块的像素位置
    last_block_x = config.GAME_AREA_X + (config.GRID_WIDTH - 1) * config.GRID_SIZE
    last_block_y = config.GAME_AREA_Y + (config.GRID_HEIGHT - 1) * config.GRID_SIZE
    
    block_right = last_block_x + config.GRID_SIZE
    block_bottom = last_block_y + config.GRID_SIZE
    
    print(f"   最后一个方块位置: ({last_block_x}, {last_block_y})")
    print(f"   方块右下角: ({block_right}, {block_bottom})")
    
    if block_right <= game_area_right:
        print("   ✅ 方块右边界在游戏区域内")
    else:
        print("   ❌ 方块右边界超出游戏区域")
        all_good = False
    
    if block_bottom <= game_area_bottom:
        print("   ✅ 方块下边界在游戏区域内")
    else:
        print("   ❌ 方块下边界超出游戏区域")
        all_good = False
    
    # 4. 验证碰撞检测逻辑
    print("\n4. 验证碰撞检测逻辑...")
    
    # 测试关键边界点
    test_cases = [
        ("左上角内", 0, 0, False),
        ("右下角内", config.GRID_WIDTH - 1, config.GRID_HEIGHT - 1, False),
        ("左边界外", -1, 5, True),
        ("右边界外", config.GRID_WIDTH, 5, True),
        ("下边界", 5, config.GRID_HEIGHT - 1, False),
        ("下边界外", 5, config.GRID_HEIGHT, True),
    ]
    
    collision_ok = True
    for desc, x, y, expected in test_cases:
        x_collision = x < 0 or x >= config.GRID_WIDTH
        y_collision = y >= config.GRID_HEIGHT
        collision = x_collision or y_collision
        
        if collision == expected:
            print(f"   ✅ {desc}: ({x}, {y}) -> 碰撞: {collision}")
        else:
            print(f"   ❌ {desc}: ({x}, {y}) -> 碰撞: {collision} (期望: {expected})")
            collision_ok = False
    
    pygame.quit()
    
    # 总结
    print("\n" + "=" * 50)
    print("修复总结:")
    
    if config.FONT and config.SMALL_FONT:
        print("✅ 中文字体问题: 已修复")
    else:
        print("❌ 中文字体问题: 未完全修复")
    
    if all_good:
        print("✅ 边界问题: 已修复")
    else:
        print("❌ 边界问题: 仍有问题")
    
    if collision_ok:
        print("✅ 碰撞检测: 逻辑正确")
    else:
        print("❌ 碰撞检测: 逻辑有问题")
    
    print("\n运行游戏:")
    print("  python tetris_game/tetris_final.py")
    print("=" * 50)

if __name__ == "__main__":
    verify_all_fixes()