"""
贪吃蛇游戏主类
"""

import pygame
import sys
from snake_game.snake import Snake
from snake_game.food import Food


class SnakeGame:
    """贪吃蛇游戏主类"""
    
    def __init__(self, width=800, height=600):
        """初始化游戏"""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("贪吃蛇游戏 - Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.score = 0
        self.high_score = 0
        
        # 游戏参数
        self.cell_size = 20
        self.grid_width = 30  # 网格宽度（单元格数）
        self.grid_height = 20  # 网格高度（单元格数）
        
        # 计算游戏区域位置（居中）
        self.game_area_width = self.grid_width * self.cell_size
        self.game_area_height = self.grid_height * self.cell_size
        self.game_area_x = (self.width - self.game_area_width) // 2
        self.game_area_y = (self.height - self.game_area_height) // 2 + 50  # 留出顶部空间显示分数
        
        # 初始化游戏对象
        self.snake = Snake(
            x=self.grid_width // 2,
            y=self.grid_height // 2,
            cell_size=self.cell_size
        )
        self.food = Food(cell_size=self.cell_size)
        
        # 生成第一个食物
        self.food.spawn(self.grid_width, self.grid_height, self.snake.body)
        
        # 加载字体 - 使用支持中文的字体
        chinese_fonts = [
            'stheitimedium',       # macOS 华文黑体 Medium
            'stheitilight',        # macOS 华文黑体 Light
            'hiraginosansgb',      # macOS 冬青黑体
            'songti',              # macOS 宋体
            'applesdgothicneo',    # macOS Apple SD Gothic Neo
            'microsoftyahei',      # Windows 微软雅黑
            'microsoftsansserif',  # Windows Microsoft Sans Serif
            'simhei',              # Windows 黑体
            'simsun',              # Windows 宋体
        ]
        
        # 查找第一个可用的中文字体
        font_name = None
        for font in chinese_fonts:
            if font in pygame.font.get_fonts():
                font_name = font
                print(f"✅ 使用中文字体: {font}")
                break
        
        # 如果找不到中文字体，使用 Arial Unicode（支持中文）
        if not font_name:
            if 'arialunicode' in pygame.font.get_fonts():
                font_name = 'arialunicode'
                print(f"✅ 使用字体: arialunicode")
            else:
                print("⚠️  使用默认字体（可能不支持中文）")
        
        try:
            self.font = pygame.font.SysFont(font_name, 36)
            self.small_font = pygame.font.SysFont(font_name, 24)
        except:
            self.font = pygame.font.SysFont(None, 36)
            self.small_font = pygame.font.SysFont(None, 24)
        
        # 颜色定义
        self.bg_color = (20, 20, 40)  # 深蓝色背景
        self.game_area_color = (30, 30, 50)  # 游戏区域背景
        self.grid_color = (40, 40, 60)  # 网格线颜色
        self.text_color = (255, 255, 255)  # 白色文字
        self.score_color = (255, 215, 0)  # 金色分数
        self.game_over_color = (255, 50, 50)  # 红色游戏结束文字
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.restart_game()
    
    def update(self):
        """更新游戏逻辑"""
        if self.game_over:
            return
            
        # 获取当前时间
        current_time = pygame.time.get_ticks()
        
        # 获取按键状态
        keys = pygame.key.get_pressed()
        
        # 更新蛇的位置
        self.snake.move(keys, current_time)
        
        # 检查碰撞
        if self.snake.check_collision(self.grid_width, self.grid_height):
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            return
        
        # 检查是否吃到食物
        if self.snake.check_food_collision(self.food.get_position()):
            self.snake.grow(1)
            self.score += 10
            self.food.spawn(self.grid_width, self.grid_height, self.snake.body)
            
            # 每得100分增加速度
            if self.score % 100 == 0 and self.snake.speed < 20:
                self.snake.speed += 1
    
    def render(self):
        """渲染画面"""
        # 绘制背景
        self.screen.fill(self.bg_color)
        
        # 绘制游戏区域背景
        game_area_rect = pygame.Rect(
            self.game_area_x - 10,
            self.game_area_y - 10,
            self.game_area_width + 20,
            self.game_area_height + 20
        )
        pygame.draw.rect(self.screen, self.game_area_color, game_area_rect)
        pygame.draw.rect(self.screen, (60, 60, 80), game_area_rect, 3)  # 边框
        
        # 绘制网格线
        for x in range(self.grid_width + 1):
            pygame.draw.line(
                self.screen,
                self.grid_color,
                (self.game_area_x + x * self.cell_size, self.game_area_y),
                (self.game_area_x + x * self.cell_size, self.game_area_y + self.game_area_height),
                1
            )
        for y in range(self.grid_height + 1):
            pygame.draw.line(
                self.screen,
                self.grid_color,
                (self.game_area_x, self.game_area_y + y * self.cell_size),
                (self.game_area_x + self.game_area_width, self.game_area_y + y * self.cell_size),
                1
            )
        
        # 绘制蛇和食物
        self.snake.draw(self.screen, self.game_area_x, self.game_area_y)
        self.food.draw(self.screen, self.game_area_x, self.game_area_y)
        
        # 绘制分数和游戏信息
        self.render_ui()
        
        # 如果游戏结束，显示游戏结束画面
        if self.game_over:
            self.render_game_over()
        
        pygame.display.flip()
    
    def render_ui(self):
        """绘制用户界面"""
        # 绘制标题
        title_text = self.font.render("贪吃蛇游戏", True, self.text_color)
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 10))
        
        # 绘制分数
        score_text = self.font.render(f"分数: {self.score}", True, self.score_color)
        self.screen.blit(score_text, (20, 20))
        
        # 绘制最高分
        high_score_text = self.font.render(f"最高分: {self.high_score}", True, self.score_color)
        self.screen.blit(high_score_text, (self.width - high_score_text.get_width() - 20, 20))
        
        # 绘制蛇的长度
        length_text = self.small_font.render(f"长度: {self.snake.get_length()}", True, self.text_color)
        self.screen.blit(length_text, (20, 60))
        
        # 绘制速度
        speed_text = self.small_font.render(f"速度: {self.snake.speed}", True, self.text_color)
        self.screen.blit(speed_text, (self.width - speed_text.get_width() - 20, 60))
        
        # 绘制控制说明
        controls_text = self.small_font.render("方向键控制移动 | ESC退出游戏", True, self.text_color)
        self.screen.blit(controls_text, (self.width // 2 - controls_text.get_width() // 2, self.height - 30))
    
    def render_game_over(self):
        """绘制游戏结束画面"""
        # 半透明覆盖层
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # 半透明黑色
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文字
        game_over_text = self.font.render("游戏结束!", True, self.game_over_color)
        self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, self.height // 2 - 50))
        
        # 最终分数
        final_score_text = self.font.render(f"最终分数: {self.score}", True, self.score_color)
        self.screen.blit(final_score_text, (self.width // 2 - final_score_text.get_width() // 2, self.height // 2))
        
        # 重新开始提示
        restart_text = self.small_font.render("按 R 或空格键重新开始", True, self.text_color)
        self.screen.blit(restart_text, (self.width // 2 - restart_text.get_width() // 2, self.height // 2 + 50))
    
    def restart_game(self):
        """重新开始游戏"""
        self.game_over = False
        self.score = 0
        
        # 重新初始化蛇
        self.snake = Snake(
            x=self.grid_width // 2,
            y=self.grid_height // 2,
            cell_size=self.cell_size
        )
        
        # 重新生成食物
        self.food.spawn(self.grid_width, self.grid_height, self.snake.body)
    
    def run(self):
        """游戏主循环"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()