"""
玩家类 - 处理玩家的移动、射击和状态
"""

import pygame
import time
from bullet import Bullet
from config import *

class Player:
    def __init__(self, screen_width, screen_height):
        """
        初始化玩家
        
        Args:
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - self.height - 20
        self.speed = PLAYER_SPEED
        self.color = PLAYER_COLOR
        self.health = PLAYER_HEALTH
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # 子弹相关
        self.bullets = []
        self.last_shot_time = 0
        self.bullet_cooldown = BULLET_COOLDOWN
        
        # 玩家状态
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_moving_up = False
        self.is_moving_down = False
        
    def update(self):
        """更新玩家位置和状态"""
        # 处理移动
        if self.is_moving_left and self.x > 0:
            self.x -= self.speed
        if self.is_moving_right and self.x < self.screen_width - self.width:
            self.x += self.speed
        if self.is_moving_up and self.y > 0:
            self.y -= self.speed
        if self.is_moving_down and self.y < self.screen_height - self.height:
            self.y += self.speed
            
        # 更新矩形位置
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)
                
    def draw(self, screen):
        """绘制玩家和子弹"""
        # 绘制玩家飞机
        # 机身
        pygame.draw.rect(screen, self.color, self.rect)
        
        # 驾驶舱
        cockpit_rect = pygame.Rect(
            self.x + self.width // 4,
            self.y + self.height // 4,
            self.width // 2,
            self.height // 2
        )
        pygame.draw.rect(screen, LIGHT_BLUE, cockpit_rect)
        
        # 机翼
        left_wing = pygame.Rect(
            self.x - 10,
            self.y + self.height // 3,
            10,
            self.height // 3
        )
        right_wing = pygame.Rect(
            self.x + self.width,
            self.y + self.height // 3,
            10,
            self.height // 3
        )
        pygame.draw.rect(screen, self.color, left_wing)
        pygame.draw.rect(screen, self.color, right_wing)
        
        # 尾翼
        tail_rect = pygame.Rect(
            self.x + self.width // 3,
            self.y - 5,
            self.width // 3,
            5
        )
        pygame.draw.rect(screen, self.color, tail_rect)
        
        # 添加发光效果
        glow_rect = pygame.Rect(
            self.x - 2, self.y - 2,
            self.width + 4, self.height + 4
        )
        pygame.draw.rect(screen, (0, 255, 255, 128), glow_rect, 2)
        
        # 绘制所有子弹
        for bullet in self.bullets:
            bullet.draw(screen)
            
    def shoot(self):
        """发射子弹"""
        current_time = time.time() * 1000  # 转换为毫秒
        
        # 检查冷却时间
        if current_time - self.last_shot_time > self.bullet_cooldown:
            # 创建子弹（从飞机中心发射）
            bullet_x = self.x + self.width // 2 - BULLET_WIDTH // 2
            bullet_y = self.y
            bullet = Bullet(bullet_x, bullet_y)
            self.bullets.append(bullet)
            self.last_shot_time = current_time
            return True
        return False
        
    def handle_keydown(self, key):
        """处理按键按下事件"""
        if key == pygame.K_LEFT:
            self.is_moving_left = True
        elif key == pygame.K_RIGHT:
            self.is_moving_right = True
        elif key == pygame.K_UP:
            self.is_moving_up = True
        elif key == pygame.K_DOWN:
            self.is_moving_down = True
        elif key == pygame.K_SPACE:
            self.shoot()
            
    def handle_keyup(self, key):
        """处理按键释放事件"""
        if key == pygame.K_LEFT:
            self.is_moving_left = False
        elif key == pygame.K_RIGHT:
            self.is_moving_right = False
        elif key == pygame.K_UP:
            self.is_moving_up = False
        elif key == pygame.K_DOWN:
            self.is_moving_down = False
            
    def take_damage(self):
        """玩家受到伤害"""
        self.health -= 1
        return self.health <= 0
        
    def reset(self):
        """重置玩家状态"""
        self.x = self.screen_width // 2 - self.width // 2
        self.y = self.screen_height - self.height - 20
        self.health = PLAYER_HEALTH
        self.bullets = []
        self.rect.x = self.x
        self.rect.y = self.y
        
    def get_rect(self):
        """获取玩家的矩形"""
        return self.rect