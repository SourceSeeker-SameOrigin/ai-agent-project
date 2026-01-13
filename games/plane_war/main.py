"""
飞机大战游戏主文件 - 完全修复版本
修复所有参数传递问题
"""

import pygame
import sys
import random
import time
from config import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from powerup import PowerUp
from explosion import Explosion


class PlaneWarGame:
    """飞机大战游戏主类"""
    
    def __init__(self):
        """初始化游戏"""
        pygame.init()
        pygame.mixer.init()
        
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        
        # 初始化字体
        init_fonts()
        
        # 检查字体是否初始化成功
        self.check_fonts()
        
        # 游戏时钟
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.game_started = False
        
        # 游戏状态
        self.score = 0
        self.level = 1
        self.difficulty = 1.0
        self.frame_count = 0
        
        # 游戏对象组
        self.player = None
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.powerups = []
        self.explosions = []
        
        # 游戏控制
        self.enemy_spawn_timer = 0
        self.powerup_spawn_timer = 0
        self.game_start_time = 0
        
        # 初始化游戏
        self.init_game()
    
    def check_fonts(self):
        """检查字体是否初始化成功"""
        global FONT_SMALL, FONT_MEDIUM, FONT_LARGE
        
        if FONT_MEDIUM is None:
            print("⚠️  警告: 字体初始化失败，尝试重新初始化")
            try:
                # 尝试使用系统字体
                font_name = None
                chinese_fonts = [
                    'stheitimedium', 'stheitilight', 'hiraginosansgb',
                    'songti', 'applesdgothicneo', 'microsoftsansserif',
                    'arialunicode'
                ]
                
                available_fonts = pygame.font.get_fonts()
                for font in chinese_fonts:
                    if font in available_fonts:
                        font_name = font
                        break
                
                if font_name:
                    FONT_SMALL = pygame.font.SysFont(font_name, 24)
                    FONT_MEDIUM = pygame.font.SysFont(font_name, 36)
                    FONT_LARGE = pygame.font.SysFont(font_name, 48)
                    print(f"✅ 字体重新初始化成功: {font_name}")
                else:
                    FONT_SMALL = pygame.font.SysFont(None, 24)
                    FONT_MEDIUM = pygame.font.SysFont(None, 36)
                    FONT_LARGE = pygame.font.SysFont(None, 48)
                    print("⚠️  使用默认字体")
            except Exception as e:
                print(f"❌ 字体重新初始化失败: {e}")
    
    def init_game(self):
        """初始化游戏状态"""
        # 创建玩家
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        
        # 清空所有对象
        self.enemies.clear()
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        self.powerups.clear()
        self.explosions.clear()
        
        # 重置游戏状态
        self.score = 0
        self.level = 1
        self.difficulty = 1.0
        self.frame_count = 0
        self.game_over = False
        self.game_started = False
        self.enemy_spawn_timer = 0
        self.powerup_spawn_timer = 0
        
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.init_game()
                    elif not self.game_started:
                        self.game_started = True
                        self.game_start_time = time.time()
                        
                elif event.key == pygame.K_r and self.game_over:
                    self.init_game()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_started:
                    self.game_started = True
                    self.game_start_time = time.time()
                    
    def update(self):
        """更新游戏逻辑"""
        if not self.game_started or self.game_over:
            return
            
        self.frame_count += 1
        
        # 更新玩家（已修复：Player.update() 现在不需要参数）
        self.player.update()
        
        # 玩家射击
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            bullet = self.player.shoot()
            if bullet:
                self.player_bullets.append(bullet)
        
        # 生成敌机
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= ENEMY_SPAWN_RATE / self.difficulty:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
            
        # 生成道具
        self.powerup_spawn_timer += 1
        if self.powerup_spawn_timer >= POWERUP_SPAWN_RATE:
            self.spawn_powerup()
            self.powerup_spawn_timer = 0
            
        # 更新敌机（已修复：传递难度参数）
        for enemy in self.enemies[:]:
            enemy.update(self.difficulty)
            
            # 敌机射击
            if random.random() < ENEMY_SHOOT_CHANCE * self.difficulty:
                bullet = enemy.shoot()
                if bullet:
                    self.enemy_bullets.append(bullet)
                    
            # 检查敌机是否飞出屏幕
            if enemy.y > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                
        # 更新玩家子弹
        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.player_bullets.remove(bullet)
                
        # 更新敌机子弹
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.y > SCREEN_HEIGHT:
                self.enemy_bullets.remove(bullet)
                
        # 更新道具
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.y > SCREEN_HEIGHT:
                self.powerups.remove(powerup)
                
        # 更新爆炸效果
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.particles == []:
                self.explosions.remove(explosion)
                
        # 检查碰撞
        self.check_collisions()
        
        # 更新难度
        self.difficulty = min(MAX_DIFFICULTY, 1.0 + self.frame_count * DIFFICULTY_INCREASE_RATE)
        
        # 更新等级
        self.level = int(self.difficulty) + 1
    
    def spawn_enemy(self):
        """生成敌机"""
        enemy_type = random.choice(["normal", "fast", "heavy"])
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = -50
        enemy = Enemy(x, y, enemy_type)
        self.enemies.append(enemy)
    
    def spawn_powerup(self):
        """生成道具"""
        powerup_type = random.choice(POWERUP_TYPES)
        x = random.randint(0, SCREEN_WIDTH - 30)
        y = -30
        powerup = PowerUp(x, y, powerup_type)
        self.powerups.append(powerup)
    
    def check_collisions(self):
        """检查所有碰撞"""
        # 玩家子弹与敌机碰撞
        for bullet in self.player_bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.check_collision(enemy.get_rect()):
                    # 敌机受到伤害
                    if not enemy.take_damage(10):
                        # 敌机被摧毁
                        self.score += enemy.score_value
                        self.create_explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2)
                        self.enemies.remove(enemy)
                    
                    # 移除子弹
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    break
        
        # 敌机子弹与玩家碰撞
        for bullet in self.enemy_bullets[:]:
            if bullet.check_collision(self.player.get_rect()):
                # 玩家受到伤害
                if not self.player.take_damage(10):
                    # 玩家死亡
                    self.game_over = True
                    self.create_explosion(self.player.x + self.player.width // 2, 
                                        self.player.y + self.player.height // 2)
                
                # 移除子弹
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)
        
        # 敌机与玩家碰撞
        for enemy in self.enemies[:]:
            if enemy.get_rect().colliderect(self.player.get_rect()):
                # 双方都受到伤害
                if not enemy.take_damage(50):
                    self.score += enemy.score_value
                    self.create_explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2)
                    self.enemies.remove(enemy)
                
                if not self.player.take_damage(30):
                    self.game_over = True
                    self.create_explosion(self.player.x + self.player.width // 2, 
                                        self.player.y + self.player.height // 2)
        
        # 道具与玩家碰撞
        for powerup in self.powerups[:]:
            if powerup.get_rect().colliderect(self.player.get_rect()):
                # 应用道具效果
                self.apply_powerup(powerup)
                self.powerups.remove(powerup)
    
    def create_explosion(self, x, y):
        """创建爆炸效果"""
        explosion = Explosion(x, y)
        self.explosions.append(explosion)
    
    def apply_powerup(self, powerup):
        """应用道具效果"""
        if powerup.type == 'health':
            self.player.heal(30)
            self.score += HEALTH_PICKUP_SCORE
        elif powerup.type == 'speed':
            self.player.speed_multiplier = 1.5
            # 5秒后恢复
            pygame.time.set_timer(pygame.USEREVENT, 5000)
        elif powerup.type == 'fire_rate':
            self.player.fire_rate_multiplier = 2.0
            # 5秒后恢复
            pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
        elif powerup.type == 'shield':
            self.player.add_shield(50)
    
    def render(self):
        """渲染游戏画面"""
        # 清空屏幕
        self.screen.fill(BLACK)
        
        # 绘制游戏对象
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
            
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
            
        for powerup in self.powerups:
            powerup.draw(self.screen)
            
        for explosion in self.explosions:
            explosion.draw(self.screen)
        
        # 绘制玩家
        if self.player:
            self.player.draw(self.screen)
        
        # 绘制UI
        self.draw_ui()
        
        # 更新显示
        pygame.display.flip()
    
    def draw_ui(self):
        """绘制用户界面"""
        # 绘制分数
        if FONT_MEDIUM:
            score_text = FONT_MEDIUM.render(f"分数: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
        
        # 绘制生命值
        if self.player:
            health_text = f"生命: {self.player.health}/{self.player.max_health}"
            if FONT_SMALL:
                health_surface = FONT_SMALL.render(health_text, True, GREEN)
                self.screen.blit(health_surface, (10, 50))
        
        # 绘制等级
        if FONT_SMALL:
            level_text = FONT_SMALL.render(f"等级: {self.level}", True, YELLOW)
            self.screen.blit(level_text, (10, 80))
        
        # 绘制游戏状态
        if not self.game_started:
            if FONT_LARGE:
                title_text = FONT_LARGE.render("飞机大战", True, CYAN)
                title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
                self.screen.blit(title_text, title_rect)
            
            if FONT_MEDIUM:
                start_text = FONT_MEDIUM.render("按空格键或点击开始游戏", True, YELLOW)
                start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(start_text, start_rect)
        
        elif self.game_over:
            if FONT_LARGE:
                game_over_text = FONT_LARGE.render("游戏结束", True, RED)
                game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
                self.screen.blit(game_over_text, game_over_rect)
            
            if FONT_MEDIUM:
                final_score_text = FONT_MEDIUM.render(f"最终分数: {self.score}", True, YELLOW)
                final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(final_score_text, final_score_rect)
                
                restart_text = FONT_MEDIUM.render("按R键重新开始", True, GREEN)
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """运行游戏主循环"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """游戏主函数"""
    game = PlaneWarGame()
    game.run()


if __name__ == "__main__":
    main()