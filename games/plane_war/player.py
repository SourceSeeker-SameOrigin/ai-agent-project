"""
玩家飞机类
包含玩家控制、射击、生命值等功能
"""

import pygame
import config
from bullet import Bullet


class Player:
    """玩家飞机类"""
    
    def __init__(self, x, y):
        """初始化玩家飞机
        
        Args:
            x: 初始x坐标
            y: 初始y坐标
        """
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = config.PLAYER_SPEED
        self.health = config.PLAYER_HEALTH
        self.max_health = config.PLAYER_HEALTH
        self.shoot_cooldown = 0
        self.shoot_delay = config.PLAYER_SHOOT_COOLDOWN
        self.bullet_speed = config.PLAYER_BULLET_SPEED
        self.score = 0
        self.is_alive = True
        self.shield = 0  # 护盾值
        self.fire_rate_multiplier = 1.0  # 射速倍率
        self.speed_multiplier = 1.0  # 速度倍率
        
        # 玩家颜色渐变
        self.color = config.GREEN
        self.shield_color = config.CYAN
        
    def update(self):
        """更新玩家状态"""
        if not self.is_alive:
            return
            
        # 获取按键状态
        keys = pygame.key.get_pressed()
        
        # 移动控制
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed * self.speed_multiplier
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed * self.speed_multiplier
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed * self.speed_multiplier
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed * self.speed_multiplier
            
        # 边界检查
        self.x = max(0, min(self.x, config.SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, config.SCREEN_HEIGHT - self.height))
        
        # 射击冷却（假设每帧16.67ms，因为FPS=60）
        dt = 16.67  # 毫秒
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
            
    def shoot(self):
        """发射子弹"""
        if self.shoot_cooldown <= 0:
            # 计算实际射击延迟
            actual_delay = self.shoot_delay / self.fire_rate_multiplier
            self.shoot_cooldown = actual_delay
            
            # 创建子弹（从飞机中心发射）
            bullet_x = self.x + self.width // 2 - config.BULLET_WIDTH // 2
            bullet_y = self.y
            return Bullet(bullet_x, bullet_y, self.bullet_speed, is_player=True)
        return None
        
    def take_damage(self, damage):
        """受到伤害
        
        Args:
            damage: 伤害值
            
        Returns:
            bool: 玩家是否还活着
        """
        if self.shield > 0:
            # 护盾吸收伤害
            shield_damage = min(self.shield, damage)
            self.shield -= shield_damage
            damage -= shield_damage
            
        if damage > 0:
            self.health -= damage
            
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            
        return self.is_alive
        
    def heal(self, amount):
        """恢复生命值
        
        Args:
            amount: 恢复量
        """
        self.health = min(self.max_health, self.health + amount)
        
    def add_shield(self, amount):
        """增加护盾
        
        Args:
            amount: 护盾值
        """
        self.shield = min(100, self.shield + amount)
        
    def add_score(self, points):
        """增加分数
        
        Args:
            points: 分数值
        """
        self.score += int(points * config.SCORE_MULTIPLIER)
        
    def get_rect(self):
        """获取碰撞矩形
        
        Returns:
            pygame.Rect: 玩家碰撞矩形
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, screen):
        """绘制玩家飞机
        
        Args:
            screen: Pygame屏幕表面
        """
        if not self.is_alive:
            return
            
        # 绘制飞机主体
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # 绘制飞机细节
        # 机头
        pygame.draw.polygon(screen, config.YELLOW, [
            (self.x + self.width // 2, self.y - 10),
            (self.x + self.width // 4, self.y),
            (self.x + 3 * self.width // 4, self.y)
        ])
        
        # 机翼
        pygame.draw.rect(screen, config.BLUE, 
                        (self.x - 10, self.y + self.height // 3, 10, self.height // 3))
        pygame.draw.rect(screen, config.BLUE, 
                        (self.x + self.width, self.y + self.height // 3, 10, self.height // 3))
        
        # 绘制护盾
        if self.shield > 0:
            shield_alpha = min(255, int(self.shield * 2.55))
            shield_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(shield_surface, (*config.CYAN, shield_alpha), 
                           (0, 0, self.width + 20, self.height + 20), 3)
            screen.blit(shield_surface, (self.x - 10, self.y - 10))
            
        # 绘制生命值条
        health_width = self.width
        health_height = 5
        health_x = self.x
        health_y = self.y - 10
        
        # 背景（红色）
        pygame.draw.rect(screen, config.RED, 
                        (health_x, health_y, health_width, health_height))
        
        # 当前生命值（绿色）
        health_percent = self.health / self.max_health
        current_width = int(health_width * health_percent)
        pygame.draw.rect(screen, config.GREEN, 
                        (health_x, health_y, current_width, health_height))