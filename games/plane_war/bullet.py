"""
子弹类
包含玩家子弹和敌机子弹
"""

import pygame
import config


class Bullet:
    """子弹类"""
    
    def __init__(self, x, y, speed, is_player=True):
        """初始化子弹
        
        Args:
            x: 初始x坐标
            y: 初始y坐标
            speed: 子弹速度
            is_player: 是否为玩家子弹（True=玩家，False=敌机）
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.is_player = is_player
        self.width = config.BULLET_WIDTH
        self.height = config.BULLET_HEIGHT
        self.is_alive = True
        
        # 根据子弹类型设置颜色
        if is_player:
            self.color = config.GREEN
        else:
            self.color = config.RED
            
    def update(self):
        """更新子弹位置"""
        if self.is_player:
            # 玩家子弹向上移动
            self.y -= self.speed
        else:
            # 敌机子弹向下移动
            self.y += self.speed
            
        # 检查子弹是否离开屏幕
        if (self.y < -self.height or 
            self.y > config.SCREEN_HEIGHT or
            self.x < -self.width or 
            self.x > config.SCREEN_WIDTH):
            self.is_alive = False
            
    def get_rect(self):
        """获取碰撞矩形
        
        Returns:
            pygame.Rect: 子弹碰撞矩形
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, screen):
        """绘制子弹
        
        Args:
            screen: Pygame屏幕表面
        """
        if not self.is_alive:
            return
            
        # 绘制子弹主体
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # 添加子弹特效
        if self.is_player:
            # 玩家子弹：绿色光效
            pygame.draw.line(screen, config.CYAN,
                           (self.x + self.width // 2, self.y + self.height),
                           (self.x + self.width // 2, self.y + self.height + 5), 2)
        else:
            # 敌机子弹：红色光效
            pygame.draw.line(screen, config.ORANGE,
                           (self.x + self.width // 2, self.y),
                           (self.x + self.width // 2, self.y - 5), 2)
            
    def check_collision(self, rect):
        """检查与指定矩形的碰撞
        
        Args:
            rect: pygame.Rect对象
            
        Returns:
            bool: 是否发生碰撞
        """
        return self.get_rect().colliderect(rect)