"""
测试字体修复
"""

import pygame
import sys
from config import *

def test_font_initialization():
    """测试字体初始化"""
    pygame.init()
    
    print("测试字体初始化...")
    
    # 初始化字体
    init_fonts()
    
    print(f"FONT_SMALL: {FONT_SMALL}")
    print(f"FONT_MEDIUM: {FONT_MEDIUM}")
    print(f"FONT_LARGE: {FONT_LARGE}")
    
    # 测试渲染
    if FONT_MEDIUM:
        try:
            text = FONT_MEDIUM.render("测试文本", True, WHITE)
            print(f"✅ 字体渲染成功: {text.get_size()}")
            return True
        except Exception as e:
            print(f"❌ 字体渲染失败: {e}")
            return False
    else:
        print("❌ 字体未初始化")
        return False

def test_game_initialization():
    """测试游戏初始化"""
    print("\n测试游戏初始化...")
    
    try:
        from main_fixed_final import PlaneWarGame
        game = PlaneWarGame()
        print("✅ 游戏初始化成功")
        
        # 测试draw_ui方法
        game.screen.fill(BLACK)
        game.draw_ui()
        print("✅ UI绘制成功")
        
        pygame.quit()
        return True
    except Exception as e:
        print(f"❌ 游戏初始化失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("字体修复测试")
    print("=" * 50)
    
    font_ok = test_font_initialization()
    game_ok = test_game_initialization()
    
    print("\n" + "=" * 50)
    print("测试结果:")
    print(f"字体初始化: {'✅ 成功' if font_ok else '❌ 失败'}")
    print(f"游戏初始化: {'✅ 成功' if game_ok else '❌ 失败'}")
    
    if font_ok and game_ok:
        print("\n🎉 所有测试通过！字体问题已修复。")
        print("现在可以运行 main_fixed_final.py 来玩游戏了。")
    else:
        print("\n⚠️  测试失败，请检查问题。")