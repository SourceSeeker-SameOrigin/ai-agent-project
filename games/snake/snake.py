"""
贪吃蛇类
"""

import pygame


class Snake:
    """贪吃蛇类"""
    
    def __init__(self, x, y, cell_size=20):
        """初始化蛇
        
        Args:
            x: 初始x坐标
            y: 初始y坐标
            cell_size: 每个单元格的大小
        """
        self.cell_size = cell_size
        self.body = [(x, y)]  # 蛇身体由多个单元格组成
        self.direction = (1, 0)  # 初始向右移动 (dx, dy)
        self.grow_pending = 0  # 需要增长的长度
        self.speed = 4  # 移动速度（每秒移动次数）
        self.last_move_time = 0
        
        # 蛇的颜色
        self.head_color = (0, 255, 0)  # 头部绿色
        self.body_color = (0, 200, 0)  # 身体深绿色
    
    def move(self, keys, current_time):
        """根据按键和游戏时间移动蛇
        
        Args:
            keys: 按键状态
            current_time: 当前游戏时间（毫秒）
        """
        # 处理方向键输入
        if keys[pygame.K_LEFT] and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif keys[pygame.K_RIGHT] and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif keys[pygame.K_UP] and self.direction != (0, 1):
            self.direction = (0, -1)
        elif keys[pygame.K_DOWN] and self.direction != (0, -1):
            self.direction = (0, 1)
        
        # 根据时间间隔移动
        move_interval = 1000 // self.speed  # 每次移动的间隔（毫秒）
        if current_time - self.last_move_time >= move_interval:
            self.last_move_time = current_time
            
            # 计算新的头部位置
            head_x, head_y = self.body[0]
            dx, dy = self.direction
            new_head = (head_x + dx, head_y + dy)
            
            # 将新头部添加到身体前面
            self.body.insert(0, new_head)
            
            # 如果不需要增长，则移除尾部
            if self.grow_pending > 0:
                self.grow_pending -= 1
            else:
                self.body.pop()
    
    def grow(self, amount=1):
        """让蛇增长
        
        Args:
            amount: 增长的长度
        """
        self.grow_pending += amount
    
    def check_collision(self, grid_width, grid_height):
        """检查碰撞
        
        Args:
            grid_width: 网格宽度
            grid_height: 网格高度
            
        Returns:
            bool: 是否发生碰撞
        """
        head_x, head_y = self.body[0]
        
        # 检查墙壁碰撞
        if head_x < 0 or head_x >= grid_width or head_y < 0 or head_y >= grid_height:
            return True
        
        # 检查自身碰撞
        for segment in self.body[1:]:
            if segment == (head_x, head_y):
                return True
        
        return False
    
    def check_food_collision(self, food_position):
        """检查是否吃到食物
        
        Args:
            food_position: 食物的位置 (x, y)
            
        Returns:
            bool: 是否吃到食物
        """
        return self.body[0] == food_position
    
    def draw(self, screen, offset_x=0, offset_y=0):
        """绘制蛇
        
        Args:
            screen: Pygame屏幕对象
            offset_x: x轴偏移
            offset_y: y轴偏移
        """
        # 绘制身体
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(
                offset_x + x * self.cell_size,
                offset_y + y * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            
            # 头部使用不同颜色
            if i == 0:
                pygame.draw.rect(screen, self.head_color, rect)
                # 绘制头部眼睛
                eye_size = self.cell_size // 5
                if self.direction == (1, 0):  # 向右
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (rect.right - eye_size, rect.top + eye_size * 2), eye_size)
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (rect.right - eye_size, rect.bottom - eye_size * 2), eye_size)
                elif self.direction == (-1, 0):  # 向左
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (rect.left + eye_size, rect.top + eye_size * 2), eye_size)
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (rect.left + eye_size, rect.bottom - eye_size * 2), eye_size)
                elif self.direction == (0, -1):  # 向上
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (rect.left + eye_size * 2, rect.top + eye_size), eye_size)
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (rect.right - eye_size * 2, rect.top + eye_size), eye_size)
                elif self.direction == (0, 1):  # 向下
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (rect.left + eye_size * 2, rect.bottom - eye_size), eye_size)
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (rect.right - eye_size * 2, rect.bottom - eye_size), eye_size)
            else:
                pygame.draw.rect(screen, self.body_color, rect)
                # 绘制身体纹理
                pygame.draw.rect(screen, (0, 150, 0), rect, 1)
    
    def get_head_position(self):
        """获取头部位置
        
        Returns:
            tuple: (x, y) 坐标
        """
        return self.body[0]
    
    def get_length(self):
        """获取蛇的长度
        
        Returns:
            int: 蛇的长度
        """
        return len(self.body)