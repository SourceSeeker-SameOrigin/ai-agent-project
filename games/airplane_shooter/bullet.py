"""
子弹类 - 处理子弹的创建、移动和碰撞
"""

import pygame
from config import *

class Bullet:
    def __init__(self, x, y):
        """
        初始化子弹
        
        Args:
            x: 子弹的x坐标
            y: 子弹的y坐标
        """
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.speed = BULLET_SPEED
        self.color = BULLET_COLOR
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.active = True
        
    def update(self):
        """更新子弹位置"""
        self.y -= self.speed  # 向上移动
        self.rect.y = self.y
        
        # 如果子弹超出屏幕，标记为不活跃
        if self.y < -self.height:
            self.active = False
            
    def draw(self, screen):
        """绘制子弹"""
        if self.active:
            # 绘制子弹主体
            pygame.draw.rect(screen, self.color, self.rect)
            
            # 添加子弹发光效果
            glow_rect = pygame.Rect(
                self.x - 2, self.y - 2,
                self.width + 4, self.height + 4
            )
            pygame.draw.rect(screen, (255, 255, 200, 128), glow_rect, 1)
            
    def check_collision(self, enemy_rect):
        """
        检查子弹与敌机的碰撞
        
        Args:
            enemy_rect: 敌机的矩形
            
        Returns:
            bool: 是否发生碰撞
        """
        if self.active and self.rect.colliderect(enemy_rect):
            self.active = False
            return True
        return False
        
    def get_rect(self):
        """获取子弹的矩形"""
        return self.rect