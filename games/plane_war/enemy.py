"""
敌机类
包含多种类型的敌机：普通敌机、快速敌机、重型敌机、BOSS
"""

import pygame
import random
import config
from bullet import Bullet


class Enemy:
    """敌机基类"""
    
    def __init__(self, x, y, enemy_type="normal"):
        """初始化敌机
        
        Args:
            x: 初始x坐标
            y: 初始y坐标
            enemy_type: 敌机类型（normal, fast, heavy, boss）
        """
        self.x = x
        self.y = y
        self.type = enemy_type
        self.is_alive = True
        self.shoot_timer = 0
        self.shoot_delay = random.randint(60, 180)  # 射击延迟（帧）
        
        # 根据类型设置属性
        if enemy_type == "normal":
            self.width = 40
            self.height = 40
            self.speed = random.uniform(config.ENEMY_SPEED_MIN, config.ENEMY_SPEED_MAX)
            self.health = config.ENEMY_HEALTH
            self.max_health = config.ENEMY_HEALTH
            self.color = config.RED
            self.score_value = config.ENEMY_KILL_SCORE
            self.shoot_chance = config.ENEMY_SHOOT_CHANCE
            
        elif enemy_type == "fast":
            self.width = 30
            self.height = 30
            self.speed = random.uniform(config.ENEMY_SPEED_MIN + 2, config.ENEMY_SPEED_MAX + 3)
            self.health = config.ENEMY_HEALTH // 2
            self.max_health = config.ENEMY_HEALTH // 2
            self.color = config.YELLOW
            self.score_value = config.ENEMY_KILL_SCORE * 2
            self.shoot_chance = config.ENEMY_SHOOT_CHANCE * 2
            
        elif enemy_type == "heavy":
            self.width = 60
            self.height = 60
            self.speed = random.uniform(config.ENEMY_SPEED_MIN, config.ENEMY_SPEED_MAX - 1)
            self.health = config.ENEMY_HEALTH * 3
            self.max_health = config.ENEMY_HEALTH * 3
            self.color = config.PURPLE
            self.score_value = config.ENEMY_KILL_SCORE * 3
            self.shoot_chance = config.ENEMY_SHOOT_CHANCE * 3
            
        elif enemy_type == "boss":
            self.width = 100
            self.height = 100
            self.speed = random.uniform(config.ENEMY_SPEED_MIN, config.ENEMY_SPEED_MAX - 0.5)
            self.health = config.ENEMY_HEALTH * 10
            self.max_health = config.ENEMY_HEALTH * 10
            self.color = config.ORANGE
            self.score_value = config.BOSS_KILL_SCORE
            self.shoot_chance = config.ENEMY_SHOOT_CHANCE * 5
            
    def update(self, difficulty=1.0):
        """更新敌机状态
        
        Args:
            difficulty: 游戏难度系数
        """
        # 移动
        self.y += self.speed * difficulty
        
        # 射击计时器
        self.shoot_timer += 1
        
        # 随机左右移动（增加难度）
        if random.random() < 0.02 * difficulty:
            self.x += random.choice([-2, 2]) * difficulty
            self.x = max(0, min(self.x, config.SCREEN_WIDTH - self.width))
            
        # 检查是否离开屏幕
        if self.y > config.SCREEN_HEIGHT:
            self.is_alive = False
            
    def shoot(self):
        """敌机射击
        
        Returns:
            Bullet or None: 如果射击则返回子弹对象，否则返回None
        """
        if random.random() < self.shoot_chance and self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            self.shoot_delay = random.randint(60, 180)
            
            # 创建子弹（从敌机底部发射）
            bullet_x = self.x + self.width // 2 - config.BULLET_WIDTH // 2
            bullet_y = self.y + self.height
            return Bullet(bullet_x, bullet_y, config.ENEMY_BULLET_SPEED, is_player=False)
        return None
        
    def take_damage(self, damage):
        """受到伤害
        
        Args:
            damage: 伤害值
            
        Returns:
            bool: 敌机是否还活着
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return self.is_alive
        
    def get_rect(self):
        """获取碰撞矩形
        
        Returns:
            pygame.Rect: 敌机碰撞矩形
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, screen):
        """绘制敌机
        
        Args:
            screen: Pygame屏幕表面
        """
        if not self.is_alive:
            return
            
        # 绘制敌机主体
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # 根据类型绘制不同细节
        if self.type == "normal":
            # 普通敌机：简单设计
            pygame.draw.circle(screen, config.WHITE, 
                             (self.x + self.width // 2, self.y + self.height // 2), 
                             self.width // 4)
                             
        elif self.type == "fast":
            # 快速敌机：流线型设计
            pygame.draw.polygon(screen, config.BLACK, [
                (self.x + self.width // 2, self.y),
                (self.x, self.y + self.height),
                (self.x + self.width, self.y + self.height)
            ])
            
        elif self.type == "heavy":
            # 重型敌机：装甲设计
            pygame.draw.rect(screen, config.GRAY, 
                           (self.x + 5, self.y + 5, self.width - 10, self.height - 10), 2)
            pygame.draw.circle(screen, config.BLACK, 
                             (self.x + self.width // 2, self.y + self.height // 2), 
                             self.width // 6)
                             
        elif self.type == "boss":
            # BOSS：复杂设计
            # 主体
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            
            # 装甲板
            pygame.draw.rect(screen, config.GRAY, 
                           (self.x + 10, self.y + 10, self.width - 20, self.height - 20))
            
            # 炮台
            pygame.draw.circle(screen, config.RED, 
                             (self.x + self.width // 4, self.y + self.height // 2), 
                             self.width // 8)
            pygame.draw.circle(screen, config.RED, 
                             (self.x + 3 * self.width // 4, self.y + self.height // 2), 
                             self.width // 8)
            
        # 绘制生命条（仅对重型敌机和BOSS）
        if self.type in ["heavy", "boss"]:
            health_width = self.width
            health_height = 5
            health_x = self.x
            health_y = self.y - 10
            
            # 背景（红色）
            pygame.draw.rect(screen, config.RED, 
                           (health_x, health_y, health_width, health_height))
            
            # 当前生命值（根据类型不同颜色）
            health_ratio = self.health / self.max_health
            current_width = int(health_width * health_ratio)
            
            if self.type == "heavy":
                health_color = config.PURPLE
            else:  # boss
                health_color = config.ORANGE
                
            pygame.draw.rect(screen, health_color, 
                           (health_x, health_y, current_width, health_height))
            
    def get_score(self):
        """获取击毁分数
        
        Returns:
            int: 分数值
        """
        return self.score_value