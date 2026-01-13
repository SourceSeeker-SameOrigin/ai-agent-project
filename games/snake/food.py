"""
食物类
"""

import pygame
import random


class Food:
    """食物类"""
    
    def __init__(self, cell_size=20):
        """初始化食物
        
        Args:
            cell_size: 每个单元格的大小
        """
        self.cell_size = cell_size
        self.position = (0, 0)  # 食物位置 (x, y)
        self.color = (255, 0, 0)  # 红色
        self.spawned = False
    
    def spawn(self, grid_width, grid_height, snake_body):
        """生成食物
        
        Args:
            grid_width: 网格宽度
            grid_height: 网格高度
            snake_body: 蛇的身体位置列表
        """
        # 生成随机位置，确保不在蛇身上
        while True:
            x = random.randint(0, grid_width - 1)
            y = random.randint(0, grid_height - 1)
            
            # 检查是否在蛇身上
            if (x, y) not in snake_body:
                self.position = (x, y)
                self.spawned = True
                break
    
    def draw(self, screen, offset_x=0, offset_y=0):
        """绘制食物
        
        Args:
            screen: Pygame屏幕对象
            offset_x: x轴偏移
            offset_y: y轴偏移
        """
        if not self.spawned:
            return
            
        x, y = self.position
        rect = pygame.Rect(
            offset_x + x * self.cell_size,
            offset_y + y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        
        # 绘制食物（苹果形状）
        pygame.draw.rect(screen, self.color, rect)
        
        # 绘制苹果茎
        stem_rect = pygame.Rect(
            rect.centerx - self.cell_size // 8,
            rect.top - self.cell_size // 4,
            self.cell_size // 4,
            self.cell_size // 4
        )
        pygame.draw.rect(screen, (139, 69, 19), stem_rect)  # 棕色
        
        # 绘制苹果叶子
        leaf_points = [
            (rect.centerx + self.cell_size // 8, rect.top - self.cell_size // 8),
            (rect.centerx + self.cell_size // 4, rect.top),
            (rect.centerx + self.cell_size // 8, rect.top + self.cell_size // 8)
        ]
        pygame.draw.polygon(screen, (0, 255, 0), leaf_points)  # 绿色
    
    def get_position(self):
        """获取食物位置
        
        Returns:
            tuple: (x, y) 坐标
        """
        return self.position
    
    def is_spawned(self):
        """检查食物是否已生成
        
        Returns:
            bool: 是否已生成
        """
        return self.spawned