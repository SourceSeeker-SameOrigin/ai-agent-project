"""
游戏主类 - 管理游戏循环、状态和所有游戏对象
"""

import pygame
import sys
import random
import time
from config import *
from player import Player
from enemy import Enemy
from bullet import Bullet

class AirplaneShooterGame:
    def __init__(self):
        """初始化游戏"""
        pygame.init()
        
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        
        # 初始化游戏时钟
        self.clock = pygame.time.Clock()
        
        # 初始化字体 - 使用支持中文的字体
        # 优先级顺序：macOS 中文字体 > Windows 中文字体 > 通用字体
        chinese_fonts = [
            'stheitimedium',       # macOS 华文黑体 Medium ✅
            'stheitilight',        # macOS 华文黑体 Light ✅
            'hiraginosansgb',      # macOS 冬青黑体 ✅
            'songti',              # macOS 宋体 ✅
            'applesdgothicneo',    # macOS Apple SD Gothic Neo ✅
            'microsoftyahei',      # Windows 微软雅黑
            'microsoftsansserif',  # Windows Microsoft Sans Serif
            'simhei',              # Windows 黑体
            'simsun',              # Windows 宋体
            'notosanscjksc',       # Google Noto Sans CJK SC
        ]
        
        # 查找第一个可用的中文字体
        font_name = None
        for font in chinese_fonts:
            if font in pygame.font.get_fonts():
                font_name = font
                print(f"✅ 使用中文字体: {font}")
                break
        
        # 如果还是找不到，使用 Arial Unicode (支持中文)
        if not font_name:
            if 'arialunicode' in pygame.font.get_fonts():
                font_name = 'arialunicode'
                print(f"✅ 使用字体: arialunicode")
            else:
                # 最后的后备方案
                font_name = None
                print("⚠️  使用默认字体（可能不支持中文）")
        
        self.font_small = pygame.font.SysFont(font_name, FONT_SIZE_SMALL)
        self.font_medium = pygame.font.SysFont(font_name, FONT_SIZE_MEDIUM)
        self.font_large = pygame.font.SysFont(font_name, FONT_SIZE_LARGE)
        
        # 初始化游戏对象
        self.player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.enemies = []
        self.particles = []
        
        # 游戏状态
        self.game_state = STATE_START
        self.score = 0
        self.enemy_spawn_counter = 0
        self.game_over_time = 0
        
        # 背景星星
        self.stars = []
        self._init_stars()
        
    def _init_stars(self):
        """初始化背景星星"""
        for _ in range(100):
            star = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.1, 0.5),
                'brightness': random.randint(150, 255)
            }
            self.stars.append(star)
            
    def _update_stars(self):
        """更新背景星星位置"""
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
                
    def _draw_stars(self):
        """绘制背景星星"""
        for star in self.stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(self.screen, color, 
                             (int(star['x']), int(star['y'])), star['size'])
                             
    def _create_particles(self, x, y, color):
        """创建粒子效果"""
        for _ in range(PARTICLE_COUNT):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-3, 3),
                'color': color,
                'life': PARTICLE_LIFETIME,
                'size': random.randint(2, 5)
            }
            self.particles.append(particle)
            
    def _update_particles(self):
        """更新粒子效果"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def _draw_particles(self):
        """绘制粒子效果"""
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / PARTICLE_LIFETIME))
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(self.screen, color, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
                             
    def _spawn_enemy(self):
        """生成敌机"""
        if self.enemy_spawn_counter >= ENEMY_SPAWN_RATE:
            enemy = Enemy(SCREEN_WIDTH)
            self.enemies.append(enemy)
            self.enemy_spawn_counter = 0
        else:
            self.enemy_spawn_counter += 1
            
    def _handle_collisions(self):
        """处理所有碰撞"""
        # 子弹与敌机碰撞
        for enemy in self.enemies[:]:
            for bullet in self.player.bullets[:]:
                if bullet.check_collision(enemy.get_rect()):
                    if enemy.take_damage():
                        # 敌机被摧毁
                        self.score += SCORE_PER_ENEMY
                        self._create_particles(enemy.x + enemy.width // 2,
                                             enemy.y + enemy.height // 2,
                                             enemy.color)
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                    break
                    
        # 敌机与玩家碰撞
        for enemy in self.enemies[:]:
            if enemy.check_collision(self.player.get_rect()):
                if self.player.take_damage():
                    # 玩家被摧毁
                    self.game_state = STATE_GAME_OVER
                    self.game_over_time = time.time()
                    self._create_particles(self.player.x + self.player.width // 2,
                                         self.player.y + self.player.height // 2,
                                         self.player.color)
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
                    
    def _draw_ui(self):
        """绘制游戏UI"""
        # 绘制分数
        score_text = self.font_medium.render(f"分数: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 绘制生命值
        health_text = self.font_medium.render(f"生命: {self.player.health}", True, GREEN)
        self.screen.blit(health_text, (10, 50))
        
        # 绘制敌机数量
        enemy_count_text = self.font_small.render(f"敌机: {len(self.enemies)}", True, YELLOW)
        self.screen.blit(enemy_count_text, (10, 90))
        
    def _draw_start_screen(self):
        """绘制开始屏幕"""
        # 绘制标题
        title_text = self.font_large.render("飞机射击游戏", True, CYAN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)
        
        # 绘制控制说明
        controls = [
            "控制说明:",
            "← → ↑ ↓  - 移动飞机",
            "空格键   - 发射子弹",
            "R键      - 重新开始游戏",
            "ESC键    - 退出游戏"
        ]
        
        for i, line in enumerate(controls):
            control_text = self.font_medium.render(line, True, WHITE)
            control_rect = control_text.get_rect(center=(SCREEN_WIDTH // 2, 
                                                       SCREEN_HEIGHT // 2 + i * 40))
            self.screen.blit(control_text, control_rect)
            
        # 绘制开始提示
        start_text = self.font_medium.render("按任意键开始游戏", True, YELLOW)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 
                                               SCREEN_HEIGHT - 100))
        self.screen.blit(start_text, start_rect)
        
    def _draw_game_over_screen(self):
        """绘制游戏结束屏幕"""
        # 半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文本
        game_over_text = self.font_large.render("游戏结束!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 
                                                       SCREEN_HEIGHT // 3))
        self.screen.blit(game_over_text, game_over_rect)
        
        # 最终分数
        score_text = self.font_medium.render(f"最终分数: {self.score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 
                                               SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # 重新开始提示
        restart_text = self.font_medium.render("按R键重新开始游戏", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 
                                                   SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
        
        # 退出提示
        quit_text = self.font_medium.render("按ESC键退出游戏", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, 
                                             SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(quit_text, quit_rect)
        
    def _reset_game(self):
        """重置游戏状态"""
        self.player.reset()
        self.enemies = []
        self.particles = []
        self.score = 0
        self.enemy_spawn_counter = 0
        self.game_state = STATE_PLAYING
        
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if self.game_state == STATE_START:
                    # 从开始屏幕进入游戏
                    self.game_state = STATE_PLAYING
                    
                elif self.game_state == STATE_PLAYING:
                    # 游戏中的按键处理
                    self.player.handle_keydown(event.key)
                    
                    # 重新开始游戏
                    if event.key == pygame.K_r:
                        self._reset_game()
                        
                elif self.game_state == STATE_GAME_OVER:
                    # 游戏结束后的按键处理
                    if event.key == pygame.K_r:
                        self._reset_game()
                        
                # 通用按键
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
            elif event.type == pygame.KEYUP and self.game_state == STATE_PLAYING:
                self.player.handle_keyup(event.key)
                
    def update(self):
        """更新游戏状态"""
        if self.game_state == STATE_PLAYING:
            # 更新玩家
            self.player.update()
            
            # 生成敌机
            self._spawn_enemy()
            
            # 更新敌机
            for enemy in self.enemies[:]:
                enemy.update()
                if not enemy.active:
                    self.enemies.remove(enemy)
                    
            # 处理碰撞
            self._handle_collisions()
            
            # 更新粒子效果
            self._update_particles()
            
        # 更新背景星星
        self._update_stars()
        
    def draw(self):
        """绘制游戏画面"""
        # 绘制背景
        self.screen.fill(BACKGROUND_COLOR)
        
        # 绘制星星背景
        self._draw_stars()
        
        if self.game_state == STATE_START:
            # 绘制开始屏幕
            self._draw_start_screen()
            
        elif self.game_state == STATE_PLAYING:
            # 绘制游戏对象
            for enemy in self.enemies:
                enemy.draw(self.screen)
            self.player.draw(self.screen)
            
            # 绘制粒子效果
            self._draw_particles()
            
            # 绘制UI
            self._draw_ui()
            
        elif self.game_state == STATE_GAME_OVER:
            # 先绘制游戏画面
            for enemy in self.enemies:
                enemy.draw(self.screen)
            self.player.draw(self.screen)
            self._draw_particles()
            self._draw_ui()
            
            # 再绘制游戏结束界面
            self._draw_game_over_screen()
            
        # 更新显示
        pygame.display.flip()
        
    def run(self):
        """运行游戏主循环"""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)