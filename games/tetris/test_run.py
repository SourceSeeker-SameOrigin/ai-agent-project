"""
测试游戏是否可以正常运行
"""

import pygame
import sys
import time

def test_game():
    """测试游戏运行"""
    print("🧪 测试俄罗斯方块游戏...")
    print("=" * 50)
    
    try:
        # 测试Pygame初始化
        pygame.init()
        print("✅ Pygame初始化成功")
        
        # 测试导入
        import config
        print("✅ config.py 导入成功")
        
        from game import TetrisGame
        print("✅ game.py 导入成功")
        
        from ui import GameUI
        print("✅ ui.py 导入成功")
        
        # 测试游戏实例创建
        game = TetrisGame()
        print("✅ 游戏实例创建成功")
        
        # 测试UI实例创建
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        ui = GameUI(screen)
        print("✅ UI实例创建成功")
        
        # 测试游戏状态
        game_grid = game.get_grid()
        game_info = game.get_game_info()
        print("✅ 游戏状态获取成功")
        
        # 测试渲染
        current_piece = game.current_piece if hasattr(game, 'current_piece') else None
        next_piece = game_info.get('next_piece')
        
        ui.draw_all(
            game_state=game_info.get('status', config.STATUS_PLAYING),
            game_grid=game_grid,
            current_piece=current_piece,
            next_piece=next_piece,
            score=game_info.get('score', 0),
            level=game_info.get('level', 1),
            lines_cleared=game_info.get('lines', 0),
            game_time=game_info.get('time', 0)
        )
        print("✅ 游戏渲染成功")
        
        pygame.quit()
        print("✅ Pygame关闭成功")
        
        print("=" * 50)
        print("🎉 所有测试通过！游戏可以正常运行。")
        print("运行命令: python main.py")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_game()
    sys.exit(0 if success else 1)