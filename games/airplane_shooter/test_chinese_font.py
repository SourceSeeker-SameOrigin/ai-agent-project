#!/usr/bin/env python3
"""
测试中文字体是否可用
"""

import pygame

def test_chinese_fonts():
    """测试系统中可用的中文字体"""
    print("=" * 60)
    print("🔍 检测系统中可用的中文字体...")
    print("=" * 60)
    
    pygame.init()
    
    # 常见中文字体列表
    chinese_fonts = [
        ('PingFang SC', 'pingfangsc', 'pingfang sc'),          # macOS
        ('Heiti SC', 'heitisc', 'heiti sc'),                   # macOS
        ('STHeiti', 'stheiti'),                                 # macOS
        ('Microsoft YaHei', 'microsoftyahei', 'microsoft yahei'), # Windows
        ('SimHei', 'simhei'),                                   # Windows
        ('SimSun', 'simsun'),                                   # Windows
        ('KaiTi', 'kaiti'),                                     # Windows
        ('Arial Unicode MS', 'arial unicode ms'),               # 通用
        ('Noto Sans CJK SC', 'notosanscjk', 'noto sans cjk sc') # 开源
    ]
    
    available_fonts = []
    
    for font_names in chinese_fonts:
        font_display_name = font_names[0]
        for font_name in font_names:
            matched = pygame.font.match_font(font_name)
            if matched:
                available_fonts.append((font_display_name, matched))
                print(f"✅ 找到: {font_display_name}")
                print(f"   路径: {matched}")
                break
        else:
            print(f"❌ 未找到: {font_display_name}")
    
    print("=" * 60)
    
    if available_fonts:
        print(f"\n✅ 共找到 {len(available_fonts)} 个中文字体")
        print(f"推荐使用: {available_fonts[0][0]}")
        
        # 测试渲染中文
        print("\n🎨 测试渲染中文...")
        try:
            font = pygame.font.SysFont(available_fonts[0][0], 36)
            test_text = "飞机射击游戏 - 中文测试"
            surface = font.render(test_text, True, (255, 255, 255))
            print(f"✅ 成功渲染: {test_text}")
            print(f"   字体: {available_fonts[0][0]}")
            print(f"   尺寸: {surface.get_size()}")
        except Exception as e:
            print(f"❌ 渲染失败: {e}")
    else:
        print("\n❌ 未找到任何中文字体！")
        print("\n💡 解决方案：")
        print("   macOS: 系统自带中文字体，应该能正常显示")
        print("   Windows: 确保安装了微软雅黑或宋体")
        print("   Linux: 安装 fonts-noto-cjk 或 fonts-wqy-zenhei")
        print("\n   安装命令（Linux）:")
        print("   sudo apt-get install fonts-noto-cjk")
        print("   或")
        print("   sudo apt-get install fonts-wqy-zenhei")
    
    pygame.quit()
    print("=" * 60)

if __name__ == "__main__":
    test_chinese_fonts()

