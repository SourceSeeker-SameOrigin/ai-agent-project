"""
测试俄罗斯方块游戏
"""

import pygame
import sys

def test_pygame():
    """测试Pygame是否正常工作"""
    try:
        pygame.init()
        screen = pygame.display.set_mode((100, 100))
        pygame.display.set_caption("测试")
        
        print("✅ Pygame初始化成功")
        print("✅ 窗口创建成功")
        
        # 测试字体
        font = pygame.font.SysFont(None, 24)
        if font:
            print("✅ 字体加载成功")
        
        pygame.quit()
        print("✅ Pygame关闭成功")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_imports():
    """测试所有导入"""
    try:
        import config
        print("✅ config.py 导入成功")
        
        from shapes import Tetromino
        print("✅ shapes.py 导入成功")
        
        from game import TetrisGame
        print("✅ game.py 导入成功")
        
        from ui import GameUI
        print("✅ ui.py 导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_game_logic():
    """测试游戏逻辑"""
    try:
        from game import TetrisGame
        
        game = TetrisGame()
        print("✅ 游戏实例创建成功")
        
        # 测试基本属性
        assert len(game.grid) == 20, "网格高度应为20"
        assert len(game.grid[0]) == 10, "网格宽度应为10"
        print("✅ 游戏网格初始化正确")
        
        # 测试方块生成
        assert game.current_piece is not None, "当前方块不应为None"
        assert game.next_piece is not None, "下一个方块不应为None"
        print("✅ 方块生成正常")
        
        # 测试移动
        initial_x = game.current_piece.x
        game.move_piece(1, 0)
        assert game.current_piece.x == initial_x + 1, "方块应向右移动"
        print("✅ 方块移动正常")
        
        # 测试旋转
        initial_rotation = game.current_piece.rotation
        game.rotate_piece()
        assert game.current_piece.rotation != initial_rotation, "方块应旋转"
        print("✅ 方块旋转正常")
        
        return True
        
    except AssertionError as e:
        print(f"❌ 断言失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🧪 开始测试俄罗斯方块游戏...")
    print("-" * 40)
    
    tests_passed = 0
    tests_total = 3
    
    # 测试1: Pygame
    print("1. 测试Pygame...")
    if test_pygame():
        tests_passed += 1
    print()
    
    # 测试2: 导入
    print("2. 测试导入...")
    if test_imports():
        tests_passed += 1
    print()
    
    # 测试3: 游戏逻辑
    print("3. 测试游戏逻辑...")
    if test_game_logic():
        tests_passed += 1
    print()
    
    print("-" * 40)
    print(f"测试结果: {tests_passed}/{tests_total} 通过")
    
    if tests_passed == tests_total:
        print("🎉 所有测试通过！游戏应该可以正常运行。")
        print("运行命令: python main.py")
    else:
        print("⚠️  有些测试未通过，请检查错误信息。")