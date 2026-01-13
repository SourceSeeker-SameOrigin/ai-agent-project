"""
简单字体测试
"""

import pygame
import sys

# 初始化pygame
pygame.init()

print("=== 简单字体测试 ===")

# 测试1：直接创建字体
print("\n1. 直接创建字体对象:")
try:
    # 尝试创建中文字体
    font = pygame.font.SysFont('stheitimedium', 36)
    print(f"✅ 字体创建成功: {font}")
    
    # 测试渲染
    text_surface = font.render("测试中文", True, (255, 255, 255))
    print(f"✅ 文本渲染成功: {text_surface.get_size()}")
except Exception as e:
    print(f"❌ 字体创建失败: {e}")

# 测试2：测试config.py中的字体初始化
print("\n2. 测试config.py字体初始化:")
try:
    # 导入config模块
    import config
    print("导入config模块...")
    
    # 调用init_fonts
    config.init_fonts()
    
    print(f"config.FONT_SMALL: {config.FONT_SMALL}")
    print(f"config.FONT_MEDIUM: {config.FONT_MEDIUM}")
    print(f"config.FONT_LARGE: {config.FONT_LARGE}")
    
    if config.FONT_MEDIUM:
        # 测试渲染
        text = config.FONT_MEDIUM.render("配置字体测试", True, (255, 255, 255))
        print(f"✅ config字体渲染成功: {text.get_size()}")
    else:
        print("❌ config字体初始化失败")
        
except Exception as e:
    print(f"❌ config测试失败: {e}")

# 测试3：测试从config导入
print("\n3. 测试从config导入:")
try:
    from config import FONT_SMALL, FONT_MEDIUM, FONT_LARGE, init_fonts
    
    # 重新初始化
    init_fonts()
    
    print(f"导入的FONT_SMALL: {FONT_SMALL}")
    print(f"导入的FONT_MEDIUM: {FONT_MEDIUM}")
    print(f"导入的FONT_LARGE: {FONT_LARGE}")
    
    if FONT_MEDIUM:
        text = FONT_MEDIUM.render("导入字体测试", True, (255, 255, 255))
        print(f"✅ 导入字体渲染成功: {text.get_size()}")
    else:
        print("❌ 导入字体初始化失败")
        
except Exception as e:
    print(f"❌ 导入测试失败: {e}")

print("\n测试完成！")
pygame.quit()