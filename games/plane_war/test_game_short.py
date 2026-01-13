"""
简短游戏测试
测试爆炸修复和射击功能
"""

import pygame
import sys
import time
from config import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from explosion import Explosion

def test_game():
    """测试游戏功能"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("游戏测试")
    
    # 创建玩家
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    
    # 创建敌机
    enemy = Enemy(SCREEN_WIDTH // 2, 100, "normal")
    
    # 游戏对象列表
    player_bullets = []
    enemies = [enemy]
    explosions = []
    
    # 测试变量
    test_start_time = time.time()
    test_duration = 5  # 测试5秒
    shots_fired = 0
    explosions_created = 0
    
    print("开始游戏测试...")
    print("按空格键射击，按ESC退出")
    
    clock = pygame.time.Clock()
    running = True
    
    while running and time.time() - test_start_time < test_duration:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # 更新玩家
        player.update()
        
        # 玩家射击（按空格键）
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            bullet = player.shoot()
            if bullet:
                player_bullets.append(bullet)
                shots_fired += 1
        
        # 更新子弹
        for bullet in player_bullets[:]:
            bullet.update()
            if bullet.y < 0:
                player_bullets.remove(bullet)
        
        # 更新敌机
        for enemy in enemies[:]:
            enemy.update(1.0)  # 难度1.0
            
            # 检查子弹与敌机碰撞
            for bullet in player_bullets[:]:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    # 创建爆炸
                    explosion = Explosion(enemy.x + enemy.width // 2, 
                                         enemy.y + enemy.height // 2, 
                                         "medium")
                    explosions.append(explosion)
                    explosions_created += 1
                    
                    # 移除子弹和敌机
                    player_bullets.remove(bullet)
                    enemies.remove(enemy)
                    break
        
        # 更新爆炸
        for explosion in explosions[:]:
            explosion.update()
            if not explosion.is_alive:
                explosions.remove(explosion)
        
        # 绘制
        screen.fill(BLACK)
        
        # 绘制玩家
        player.draw(screen)
        
        # 绘制敌机
        for enemy in enemies:
            enemy.draw(screen)
        
        # 绘制子弹
        for bullet in player_bullets:
            bullet.draw(screen)
        
        # 绘制爆炸
        for explosion in explosions:
            explosion.draw(screen)
        
        # 显示测试信息
        font = pygame.font.SysFont(None, 24)
        info_text = [
            f"测试时间: {int(time.time() - test_start_time)}/{test_duration}秒",
            f"射击次数: {shots_fired}",
            f"爆炸次数: {explosions_created}",
            "按空格键射击敌机"
        ]
        
        for i, text in enumerate(info_text):
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (10, 10 + i * 25))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    
    print("\n测试结果:")
    print(f"✅ 射击测试: 成功发射 {shots_fired} 发子弹")
    print(f"✅ 爆炸测试: 成功创建 {explosions_created} 个爆炸效果")
    print(f"✅ 游戏运行: 正常运行 {test_duration} 秒")
    
    if shots_fired > 0 and explosions_created > 0:
        print("\n🎮 所有测试通过！游戏功能正常。")
        return True
    else:
        print("\n⚠️  测试完成，但某些功能未测试到。")
        return False

if __name__ == "__main__":
    success = test_game()
    sys.exit(0 if success else 1)