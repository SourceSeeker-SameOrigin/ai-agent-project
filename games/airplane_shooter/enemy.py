"""
敌机类 - 处理敌机的创建、移动和碰撞
"""

import pygame
import random
from config import *

class Enemy:
    def __init__(self, screen_width):
        """
        初始化敌机
        
        Args:
            screen_width: 屏幕宽度，用于随机生成位置
        """
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.x = random.randint(0, screen_width - self.width)
        self.y = -self.height  # 从屏幕上方开始
        self.speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        self.color = ENEMY_COLOR
        self.health = ENEMY_HEALTH
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.active = True
        
        # 敌机类型（用于视觉效果）
        self.type = random.choice(["basic", "fast", "tough"])
        if self.type == "fast":
            self.speed *= 1.5
            self.color = ORANGE
        elif self.type == "tough":
            self.health = 2
            self.color = PURPLE
            
    def update(self):
        """更新敌机位置"""
        self.y += self.speed
        self.rect.y = self.y
        
        # 如果敌机超出屏幕，标记为不活跃
        if self.y > SCREEN_HEIGHT:
            self.active = False
            
    def draw(self, screen):
        """绘制敌机"""
        if self.active:
            # 绘制敌机主体
            pygame.draw.rect(screen, self.color, self.rect)
            
            # 添加敌机细节
            # 驾驶舱
            cockpit_rect = pygame.Rect(
                self.x + self.width // 4,
                self.y + self.height // 4,
                self.width // 2,
                self.height // 2
            )
            pygame.draw.rect(screen, DARK_BLUE, cockpit_rect)
            
            # 机翼
            left_wing = pygame.Rect(
                self.x - 5,
                self.y + self.height // 3,
                5,
                self.height // 3
            )
            right_wing = pygame.Rect(
                self.x + self.width,
                self.y + self.height // 3,
                5,
                self.height // 3
            )
            pygame.draw.rect(screen, self.color, left_wing)
            pygame.draw.rect(screen, self.color, right_wing)
            
            # 添加边框效果
            pygame.draw.rect(screen, WHITE, self.rect, 1)
            
    def take_damage(self, damage=1):
        """
        敌机受到伤害
        
        Args:
            damage: 伤害值
            
        Returns:
            bool: 敌机是否被摧毁
        """
        self.health -= damage
        if self.health <= 0:
            self.active = False
            return True
        return False
        
    def check_collision(self, player_rect):
        """
        检查敌机与玩家的碰撞
        
        Args:
            player_rect: 玩家的矩形
            
        Returns:
            bool: 是否发生碰撞
        """
        if self.active and self.rect.colliderect(player_rect):
            self.active = False
            return True
        return False
        
    def get_rect(self):
        """获取敌机的矩形"""
        return self.rect