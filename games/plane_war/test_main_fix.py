"""
测试主文件修复
"""

import pygame
import sys
from config import *

def test_main():
    """测试主文件"""
    print("测试主文件修复...")
    
    try:
        # 初始化pygame
        pygame.init()
        
        # 创建屏幕
        screen = pygame.display.set_mode((100, 100))
        
        # 初始化字体
        init_fonts()
        
        print(f"FONT_MEDIUM: {FONT_MEDIUM}")
        
        # 测试字体渲染
        if FONT_MEDIUM:
            text = FONT_MEDIUM.render("测试", True, WHITE)
            print(f"✅ 字体渲染成功: {text}")
            
            # 测试blit
            screen.fill(BLACK)
            screen.blit(text, (10, 10))
            print("✅ 文本绘制成功")
        else:
            print("❌ 字体未初始化")
            
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    if test_main():
        print("\n🎉 主文件修复测试通过！")
        print("现在可以运行 main.py 来玩游戏了。")
    else:
        print("\n⚠️  测试失败，请检查问题。")