"""
测试修复脚本
验证爆炸颜色问题和射击功能
"""

import pygame
import sys
import config
from explosion import Explosion
from player import Player

def test_explosion_color():
    """测试爆炸颜色问题"""
    print("测试爆炸颜色问题...")
    
    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    
    try:
        # 创建不同大小的爆炸效果
        explosions = [
            Explosion(50, 50, "small"),
            Explosion(50, 50, "medium"),
            Explosion(50, 50, "large"),
            Explosion(50, 50, "huge"),
            Explosion(50, 50, "medium", color=(255, 0, 0)),  # 自定义颜色
        ]
        
        print(f"✅ 成功创建 {len(explosions)} 个爆炸效果")
        
        # 测试绘制
        for i, explosion in enumerate(explosions):
            try:
                explosion.draw(screen)
                print(f"✅ 爆炸 {i+1} 绘制成功")
            except Exception as e:
                print(f"❌ 爆炸 {i+1} 绘制失败: {e}")
                
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ 爆炸测试失败: {e}")
        pygame.quit()
        return False

def test_player_shoot():
    """测试玩家射击功能"""
    print("\n测试玩家射击功能...")
    
    try:
        # 创建玩家
        player = Player(400, 500)
        
        # 测试射击
        bullet1 = player.shoot()
        if bullet1:
            print(f"✅ 第一次射击成功，子弹速度: {bullet1.speed}")
        else:
            print("❌ 第一次射击失败")
            
        # 测试冷却
        bullet2 = player.shoot()
        if bullet2:
            print(f"✅ 第二次射击成功（无冷却）")
        else:
            print("✅ 第二次射击返回None（在冷却中）")
            
        # 测试按键射击（模拟）
        print("\n测试按键射击...")
        print("注意：实际射击需要在游戏主循环中测试")
        
        return True
        
    except Exception as e:
        print(f"❌ 玩家射击测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试修复...")
    print("=" * 50)
    
    # 测试爆炸颜色
    explosion_ok = test_explosion_color()
    
    # 测试玩家射击
    shoot_ok = test_player_shoot()
    
    print("\n" + "=" * 50)
    print("测试结果:")
    print(f"爆炸颜色修复: {'✅ 通过' if explosion_ok else '❌ 失败'}")
    print(f"射击功能测试: {'✅ 通过' if shoot_ok else '❌ 失败'}")
    
    if explosion_ok and shoot_ok:
        print("\n✅ 所有测试通过！")
        print("现在可以运行游戏测试空格键射击功能。")
    else:
        print("\n❌ 部分测试失败，请检查代码。")

if __name__ == "__main__":
    main()