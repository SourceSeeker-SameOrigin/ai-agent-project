"""
道具类
包含各种增益道具：生命恢复、速度提升、射速提升、护盾等
"""

import pygame
import random
import config


class PowerUp:
    """道具类"""
    
    def __init__(self, x, y, powerup_type=None):
        """初始化道具
        
        Args:
            x: 初始x坐标
            y: 初始y坐标
            powerup_type: 道具类型（health, speed, fire_rate, shield）
        """
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 2
        self.is_alive = True
        
        # 如果没有指定类型，随机选择
        if powerup_type is None:
            self.type = random.choice(config.POWERUP_TYPES)
        else:
            self.type = powerup_type
            
        # 根据类型设置颜色和效果
        if self.type == "health":
            self.color = config.GREEN
            self.effect_amount = 30  # 恢复30点生命
            self.symbol = "+"
        elif self.type == "speed":
            self.color = config.YELLOW
            self.effect_amount = 1.5  # 速度提升50%
            self.symbol = "⚡"
        elif self.type == "fire_rate":
            self.color = config.BLUE
            self.effect_amount = 1.5  # 射速提升50%
            self.symbol = "🔥"
        elif self.type == "shield":
            self.color = config.CYAN
            self.effect_amount = 50  # 增加50点护盾
            self.symbol = "🛡️"
            
        # 动画效果
        self.animation_timer = 0
        self.pulse_size = 1.0
        
    def update(self):
        """更新道具状态"""
        # 向下移动
        self.y += self.speed
        
        # 动画效果
        self.animation_timer += 1
        self.pulse_size = 1.0 + 0.1 * abs(pygame.math.Vector2(0, 1).rotate(self.animation_timer * 5).y)
        
        # 检查是否离开屏幕
        if self.y > config.SCREEN_HEIGHT:
            self.is_alive = False
            
    def get_rect(self):
        """获取碰撞矩形
        
        Returns:
            pygame.Rect: 道具碰撞矩形
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def apply_effect(self, player):
        """对玩家应用道具效果
        
        Args:
            player: Player对象
            
        Returns:
            str: 道具效果描述
        """
        if self.type == "health":
            player.heal(self.effect_amount)
            return f"生命值 +{self.effect_amount}"
            
        elif self.type == "speed":
            player.speed_multiplier = self.effect_amount
            # 效果持续10秒
            pygame.time.set_timer(pygame.USEREVENT + 1, 10000)  # 10秒后重置速度
            return f"速度提升 {int((self.effect_amount - 1) * 100)}%"
            
        elif self.type == "fire_rate":
            player.fire_rate_multiplier = self.effect_amount
            # 效果持续10秒
            pygame.time.set_timer(pygame.USEREVENT + 2, 10000)  # 10秒后重置射速
            return f"射速提升 {int((self.effect_amount - 1) * 100)}%"
            
        elif self.type == "shield":
            player.add_shield(self.effect_amount)
            return f"护盾 +{self.effect_amount}"
            
        return ""
        
    def draw(self, screen):
        """绘制道具
        
        Args:
            screen: Pygame屏幕表面
        """
        if not self.is_alive:
            return
            
        # 计算动画大小
        draw_width = int(self.width * self.pulse_size)
        draw_height = int(self.height * self.pulse_size)
        draw_x = self.x - (draw_width - self.width) // 2
        draw_y = self.y - (draw_height - self.height) // 2
        
        # 绘制道具主体
        pygame.draw.rect(screen, self.color, 
                        (draw_x, draw_y, draw_width, draw_height), 
                        border_radius=8)
        
        # 绘制边框
        pygame.draw.rect(screen, config.WHITE, 
                        (draw_x, draw_y, draw_width, draw_height), 
                        2, border_radius=8)
        
        # 绘制符号（使用文本渲染）
        try:
            font = pygame.font.SysFont(None, 24)
            text = font.render(self.symbol, True, config.WHITE)
            text_rect = text.get_rect(center=(self.x + self.width // 2, 
                                            self.y + self.height // 2))
            screen.blit(text, text_rect)
        except:
            # 如果符号渲染失败，绘制简单图形
            if self.type == "health":
                pygame.draw.polygon(screen, config.WHITE, [
                    (self.x + self.width // 2, self.y + 5),
                    (self.x + 5, self.y + self.height - 5),
                    (self.x + self.width - 5, self.y + self.height - 5)
                ])
            elif self.type == "speed":
                pygame.draw.line(screen, config.WHITE,
                               (self.x + 5, self.y + self.height // 2),
                               (self.x + self.width - 5, self.y + self.height // 2), 3)
                pygame.draw.line(screen, config.WHITE,
                               (self.x + self.width // 2, self.y + 5),
                               (self.x + self.width // 2, self.y + self.height - 5), 3)
            elif self.type == "fire_rate":
                pygame.draw.circle(screen, config.WHITE,
                                 (self.x + self.width // 2, self.y + self.height // 2),
                                 self.width // 3)
            elif self.type == "shield":
                pygame.draw.rect(screen, config.WHITE,
                               (self.x + 5, self.y + 5, self.width - 10, self.height - 10), 2)