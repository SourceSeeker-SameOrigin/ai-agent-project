"""
调试爆炸颜色问题
"""

import pygame
import config

# 初始化pygame
pygame.init()
screen = pygame.display.set_mode((100, 100))

# 测试config中的颜色
print("测试config颜色:")
print(f"config.YELLOW = {config.YELLOW}")
print(f"type(config.YELLOW) = {type(config.YELLOW)}")
print(f"len(config.YELLOW) = {len(config.YELLOW)}")

# 测试颜色元组解包
try:
    color = config.YELLOW
    print(f"\n测试元组解包:")
    print(f"color = {color}")
    print(f"(*color, 128) = {(*color, 128)}")
    
    # 测试绘制
    test_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.circle(test_surface, (*color, 128), (25, 25), 10)
    print("✅ 颜色解包和绘制成功")
except Exception as e:
    print(f"❌ 颜色解包失败: {e}")

# 测试爆炸类
print("\n测试爆炸类导入:")
try:
    from explosion import Explosion
    print("✅ 爆炸类导入成功")
    
    # 创建爆炸
    explosion = Explosion(50, 50, "small")
    print(f"爆炸颜色: {explosion.color}")
    print(f"爆炸颜色类型: {type(explosion.color)}")
    
    # 测试粒子颜色
    if explosion.particles:
        particle = explosion.particles[0]
        print(f"粒子颜色: {particle.color}")
        print(f"粒子颜色类型: {type(particle.color)}")
        
except Exception as e:
    print(f"❌ 爆炸测试失败: {e}")

pygame.quit()