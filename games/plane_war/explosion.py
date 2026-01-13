"""
爆炸效果类
包含粒子系统和爆炸动画
"""

import pygame
import random
import config


class Particle:
    """粒子类"""
    
    def __init__(self, x, y, color):
        """初始化粒子
        
        Args:
            x: 初始x坐标
            y: 初始y坐标
            color: 粒子颜色
        """
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.life = random.randint(20, 40)
        self.max_life = self.life
        
    def update(self):
        """更新粒子状态"""
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        
        # 重力效果
        self.speed_y += 0.1
        
        # 粒子逐渐变小
        self.size = max(0, self.size * (self.life / self.max_life))
        
    def is_alive(self):
        """检查粒子是否还活着
        
        Returns:
            bool: 粒子是否存活
        """
        return self.life > 0
        
    def draw(self, screen):
        """绘制粒子
        
        Args:
            screen: Pygame屏幕表面
        """
        if self.is_alive():
            # 根据生命值计算透明度
            alpha = int(255 * (self.life / self.max_life))
            
            # 确保颜色是元组
            if isinstance(self.color, tuple) and len(self.color) == 3:
                color_with_alpha = (*self.color, alpha)
            else:
                # 如果颜色不是元组，使用默认橙色
                color_with_alpha = (255, 165, 0, alpha)
            
            # 创建带透明度的表面
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color_with_alpha, 
                             (self.size, self.size), self.size)
            screen.blit(particle_surface, (self.x - self.size, self.y - self.size))


class Explosion:
    """爆炸效果类"""
    
    def __init__(self, x, y, size="medium", color=None):
        """初始化爆炸效果
        
        Args:
            x: 爆炸中心x坐标
            y: 爆炸中心y坐标
            size: 爆炸大小（small, medium, large, huge）
            color: 爆炸颜色（None则根据大小自动选择）
        """
        self.x = x
        self.y = y
        self.size = size
        self.particles = []
        self.is_alive = True
        self.timer = 0
        self.max_duration = config.EXPLOSION_DURATION
        
        # 根据大小设置粒子数量
        if size == "small":
            num_particles = config.EXPLOSION_PARTICLES // 3
        elif size == "medium":
            num_particles = config.EXPLOSION_PARTICLES
        elif size == "large":
            num_particles = config.EXPLOSION_PARTICLES * 2
        elif size == "huge":
            num_particles = config.EXPLOSION_PARTICLES * 3
        else:
            num_particles = config.EXPLOSION_PARTICLES
            
        # 设置颜色
        if color is None:
            if size == "small":
                self.color = config.YELLOW
            elif size == "medium":
                self.color = config.ORANGE
            elif size == "large":
                self.color = config.RED
            elif size == "huge":
                self.color = (255, 100, 0)  # 深橙色
            else:
                self.color = config.ORANGE
        else:
            self.color = color
            
        # 创建粒子
        for _ in range(num_particles):
            # 确保颜色是元组
            if isinstance(self.color, tuple) and len(self.color) == 3:
                particle_color = (
                    max(0, min(255, self.color[0] + random.randint(-50, 50))),
                    max(0, min(255, self.color[1] + random.randint(-50, 50))),
                    max(0, min(255, self.color[2] + random.randint(-50, 50)))
                )
            else:
                # 如果颜色不是元组，使用默认橙色
                particle_color = (255, 165, 0)
                
            self.particles.append(Particle(x, y, particle_color))
            
    def update(self):
        """更新爆炸效果"""
        self.timer += 1
        
        # 更新所有粒子
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
                
        # 检查爆炸是否结束
        if self.timer >= self.max_duration and len(self.particles) == 0:
            self.is_alive = False
            
    def draw(self, screen):
        """绘制爆炸效果
        
        Args:
            screen: Pygame屏幕表面
        """
        for particle in self.particles:
            particle.draw(screen)
            
        # 绘制爆炸中心（仅在前半段时间）
        if self.timer < self.max_duration // 2:
            center_size = max(1, int(20 * (1 - self.timer / (self.max_duration // 2))))
            pygame.draw.circle(screen, config.WHITE, (int(self.x), int(self.y)), center_size)