"""
俄罗斯方块游戏界面和渲染
负责绘制游戏画面、分数、下一个方块等信息
"""

import pygame
import config
from shapes import Tetromino

class GameUI:
    """游戏界面类"""
    
    def __init__(self, screen):
        """初始化界面"""
        self.screen = screen
        
        # 尝试使用支持中文的字体
        font_names = ["simhei", "simsun", "microsoftyahei", "fangsong", "arial"]
        self.font = None
        self.small_font = None
        
        for font_name in font_names:
            try:
                self.font = pygame.font.SysFont(font_name, config.FONT_SIZE)
                self.small_font = pygame.font.SysFont(font_name, config.SMALL_FONT_SIZE)
                print(f"使用字体: {font_name}")
                break
            except:
                continue
        
        # 如果找不到中文字体，使用默认字体
        if self.font is None:
            self.font = pygame.font.SysFont(None, config.FONT_SIZE)
            self.small_font = pygame.font.SysFont(None, config.SMALL_FONT_SIZE)
            print("使用默认字体")
        
        # 预渲染一些静态文本
        self.title_text = self.font.render("俄罗斯方块", True, config.COLORS['text'])
        self.score_text = self.small_font.render("分数", True, config.COLORS['text'])
        self.level_text = self.small_font.render("等级", True, config.COLORS['text'])
        self.lines_text = self.small_font.render("消除行数", True, config.COLORS['text'])
        self.time_text = self.small_font.render("游戏时间", True, config.COLORS['text'])
        self.next_text = self.small_font.render("下一个", True, config.COLORS['text'])
        self.paused_text = self.font.render("游戏暂停", True, config.COLORS['text'])
        self.game_over_text = self.font.render("游戏结束", True, config.COLORS['game_over'])
        self.restart_text = self.small_font.render("按R键重新开始", True, config.COLORS['text'])
        
        # 控制说明
        self.controls = [
            "控制说明:",
            "← → : 左右移动",
            "↑ : 旋转",
            "↓ : 加速下落",
            "空格 : 硬降落",
            "P : 暂停/继续",
            "R : 重新开始",
            "ESC : 退出游戏"
        ]
    
    def draw_background(self):
        """绘制背景"""
        self.screen.fill(config.COLORS['background'])
        
        # 绘制游戏区域背景
        game_area_rect = pygame.Rect(
            config.GAME_AREA_X - 5,
            config.GAME_AREA_Y - 5,
            config.GRID_WIDTH * config.GRID_SIZE + 10,
            config.GRID_HEIGHT * config.GRID_SIZE + 10
        )
        pygame.draw.rect(self.screen, (30, 30, 50), game_area_rect)
        pygame.draw.rect(self.screen, config.COLORS['grid'], game_area_rect, 2)
    
    def draw_grid(self, game_grid):
        """绘制游戏网格和方块"""
        # 绘制网格线
        for x in range(config.GRID_WIDTH + 1):
            pygame.draw.line(
                self.screen,
                config.COLORS['grid'],
                (config.GAME_AREA_X + x * config.GRID_SIZE, config.GAME_AREA_Y),
                (config.GAME_AREA_X + x * config.GRID_SIZE, 
                 config.GAME_AREA_Y + config.GRID_HEIGHT * config.GRID_SIZE),
                1
            )
        
        for y in range(config.GRID_HEIGHT + 1):
            pygame.draw.line(
                self.screen,
                config.COLORS['grid'],
                (config.GAME_AREA_X, config.GAME_AREA_Y + y * config.GRID_SIZE),
                (config.GAME_AREA_X + config.GRID_WIDTH * config.GRID_SIZE,
                 config.GAME_AREA_Y + y * config.GRID_SIZE),
                1
            )
        
        # 绘制已锁定的方块
        for y in range(config.GRID_HEIGHT):
            for x in range(config.GRID_WIDTH):
                if game_grid[y][x]:
                    color_idx = game_grid[y][x] - 1
                    color = config.COLORS['tetromino'][color_idx]
                    
                    # 绘制方块
                    rect = pygame.Rect(
                        config.GAME_AREA_X + x * config.GRID_SIZE,
                        config.GAME_AREA_Y + y * config.GRID_SIZE,
                        config.GRID_SIZE,
                        config.GRID_SIZE
                    )
                    pygame.draw.rect(self.screen, color, rect)
                    
                    # 绘制方块边框
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
                    
                    # 绘制方块内部高光
                    highlight = pygame.Rect(
                        config.GAME_AREA_X + x * config.GRID_SIZE + 2,
                        config.GAME_AREA_Y + y * config.GRID_SIZE + 2,
                        config.GRID_SIZE - 4,
                        config.GRID_SIZE - 4
                    )
                    pygame.draw.rect(self.screen, 
                                   (min(color[0] + 50, 255), 
                                    min(color[1] + 50, 255), 
                                    min(color[2] + 50, 255)), 
                                   highlight, 1)
    
    def draw_next_piece(self, next_piece):
        """绘制下一个方块预览"""
        # 绘制预览区域背景
        preview_x = config.GAME_AREA_X + config.GRID_WIDTH * config.GRID_SIZE + 50
        preview_y = config.GAME_AREA_Y + 100
        preview_width = 6 * config.GRID_SIZE
        preview_height = 6 * config.GRID_SIZE
        
        preview_rect = pygame.Rect(
            preview_x - 5,
            preview_y - 5,
            preview_width + 10,
            preview_height + 10
        )
        pygame.draw.rect(self.screen, (30, 30, 50), preview_rect)
        pygame.draw.rect(self.screen, config.COLORS['grid'], preview_rect, 2)
        
        # 绘制"下一个"文本
        self.screen.blit(self.next_text, (preview_x + preview_width // 2 - self.next_text.get_width() // 2, preview_y - 30))
        
        # 绘制下一个方块
        if next_piece:
            # 计算方块在预览区域中的位置（居中）
            shape = next_piece.matrix
            shape_width = len(shape[0]) * config.GRID_SIZE
            shape_height = len(shape) * config.GRID_SIZE
            
            start_x = preview_x + (preview_width - shape_width) // 2
            start_y = preview_y + (preview_height - shape_height) // 2
            
            # 绘制方块
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        color = config.COLORS['tetromino'][next_piece.shape_type]
                        
                        rect = pygame.Rect(
                            start_x + x * config.GRID_SIZE,
                            start_y + y * config.GRID_SIZE,
                            config.GRID_SIZE,
                            config.GRID_SIZE
                        )
                        pygame.draw.rect(self.screen, color, rect)
                        pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
    
    def draw_info(self, score, level, lines_cleared, game_time):
        """绘制游戏信息（分数、等级、行数、时间）"""
        info_x = config.GAME_AREA_X + config.GRID_WIDTH * config.GRID_SIZE + 50
        info_y = config.GAME_AREA_Y + 250
        
        # 绘制分数
        self.screen.blit(self.score_text, (info_x, info_y))
        score_value = self.small_font.render(str(score), True, config.COLORS['text'])
        self.screen.blit(score_value, (info_x + 80, info_y))
        
        # 绘制等级
        self.screen.blit(self.level_text, (info_x, info_y + 40))
        level_value = self.small_font.render(str(level), True, config.COLORS['text'])
        self.screen.blit(level_value, (info_x + 80, info_y + 40))
        
        # 绘制消除行数
        self.screen.blit(self.lines_text, (info_x, info_y + 80))
        lines_value = self.small_font.render(str(lines_cleared), True, config.COLORS['text'])
        self.screen.blit(lines_value, (info_x + 80, info_y + 80))
        
        # 绘制游戏时间
        self.screen.blit(self.time_text, (info_x, info_y + 120))
        minutes = game_time // 60
        seconds = game_time % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        time_value = self.small_font.render(time_str, True, config.COLORS['text'])
        self.screen.blit(time_value, (info_x + 80, info_y + 120))
    
    def draw_controls(self):
        """绘制控制说明"""
        controls_x = config.GAME_AREA_X + config.GRID_WIDTH * config.GRID_SIZE + 50
        controls_y = config.GAME_AREA_Y + 350
        
        for i, control in enumerate(self.controls):
            control_text = self.small_font.render(control, True, config.COLORS['text'])
            self.screen.blit(control_text, (controls_x, controls_y + i * 25))
    
    def draw_current_piece(self, current_piece):
        """绘制当前下落的方块"""
        if current_piece:
            # 绘制方块
            for y, row in enumerate(current_piece.matrix):
                for x, cell in enumerate(row):
                    if cell:
                        color = config.COLORS['tetromino'][current_piece.shape_type]
                        
                        rect = pygame.Rect(
                            config.GAME_AREA_X + (current_piece.x + x) * config.GRID_SIZE,
                            config.GAME_AREA_Y + (current_piece.y + y) * config.GRID_SIZE,
                            config.GRID_SIZE,
                            config.GRID_SIZE
                        )
                        pygame.draw.rect(self.screen, color, rect)
                        pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
                        
                        # 绘制方块内部高光
                        highlight = pygame.Rect(
                            config.GAME_AREA_X + (current_piece.x + x) * config.GRID_SIZE + 2,
                            config.GAME_AREA_Y + (current_piece.y + y) * config.GRID_SIZE + 2,
                            config.GRID_SIZE - 4,
                            config.GRID_SIZE - 4
                        )
                        pygame.draw.rect(self.screen, 
                                       (min(color[0] + 50, 255), 
                                        min(color[1] + 50, 255), 
                                        min(color[2] + 50, 255)), 
                                       highlight, 1)
    
    def draw_ghost_piece(self, current_piece, game_grid):
        """绘制幽灵方块（预测落点）"""
        if not current_piece:
            return
        
        # 辅助函数：检查方块在指定位置是否与网格碰撞
        def check_collision(piece, grid, x_offset=0, y_offset=0):
            """检查方块在指定位置是否与网格碰撞"""
            for y, row in enumerate(piece.matrix):
                for x, cell in enumerate(row):
                    if cell:
                        grid_x = piece.x + x + x_offset
                        grid_y = piece.y + y + y_offset
                        
                        # 检查边界
                        if grid_x < 0 or grid_x >= config.GRID_WIDTH or grid_y < 0 or grid_y >= config.GRID_HEIGHT:
                            return True
                            
                        # 检查与已锁定方块的碰撞
                        if grid_y >= 0 and grid[grid_y][grid_x]:
                            return True
            return False
        
        # 计算幽灵方块的位置
        ghost_y = current_piece.y
        while not check_collision(current_piece, game_grid, 0, ghost_y + 1 - current_piece.y):
            ghost_y += 1
        
        # 如果幽灵方块就在当前方块下方，不绘制
        if ghost_y == current_piece.y:
            return
        
        # 绘制半透明的幽灵方块
        for y, row in enumerate(current_piece.matrix):
            for x, cell in enumerate(row):
                if cell:
                    color = config.COLORS['tetromino'][current_piece.shape_type]
                    # 创建半透明颜色
                    ghost_color = (color[0], color[1], color[2], 100)
                    
                    # 由于pygame不支持RGBA颜色直接绘制矩形，我们使用surface
                    ghost_surface = pygame.Surface((config.GRID_SIZE, config.GRID_SIZE), pygame.SRCALPHA)
                    ghost_surface.fill(ghost_color)
                    
                    self.screen.blit(ghost_surface, (
                        config.GAME_AREA_X + (current_piece.x + x) * config.GRID_SIZE,
                        config.GAME_AREA_Y + (ghost_y + y) * config.GRID_SIZE
                    ))
                    
                    # 绘制幽灵方块边框
                    ghost_rect = pygame.Rect(
                        config.GAME_AREA_X + (current_piece.x + x) * config.GRID_SIZE,
                        config.GAME_AREA_Y + (ghost_y + y) * config.GRID_SIZE,
                        config.GRID_SIZE,
                        config.GRID_SIZE
                    )
                    pygame.draw.rect(self.screen, (200, 200, 200, 150), ghost_rect, 1)
    
    def draw_paused(self):
        """绘制暂停画面"""
        # 创建半透明覆盖层
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # 绘制暂停文本
        text_rect = self.paused_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(self.paused_text, text_rect)
    
    def draw_game_over(self, final_score):
        """绘制游戏结束画面"""
        # 创建半透明覆盖层
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # 绘制游戏结束文本
        game_over_rect = self.game_over_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(self.game_over_text, game_over_rect)
        
        # 绘制最终分数
        final_score_text = self.font.render(f"最终分数: {final_score}", True, config.COLORS['text'])
        final_score_rect = final_score_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(final_score_text, final_score_rect)
        
        # 绘制重新开始提示
        restart_rect = self.restart_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(self.restart_text, restart_rect)
    
    def draw_title(self):
        """绘制游戏标题"""
        title_x = config.SCREEN_WIDTH // 2 - self.title_text.get_width() // 2
        self.screen.blit(self.title_text, (title_x, 20))
    
    def draw_all(self, game_state, game_grid, current_piece, next_piece, score, level, lines_cleared, game_time):
        """绘制所有游戏元素"""
        self.draw_background()
        self.draw_title()
        self.draw_grid(game_grid)
        self.draw_ghost_piece(current_piece, game_grid)
        self.draw_current_piece(current_piece)
        self.draw_next_piece(next_piece)
        self.draw_info(score, level, lines_cleared, game_time)
        self.draw_controls()
        
        if game_state == "paused":
            self.draw_paused()
        elif game_state == "game_over":
            self.draw_game_over(score)