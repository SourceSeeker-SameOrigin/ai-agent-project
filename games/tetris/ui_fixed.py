"""
修复后的俄罗斯方块游戏界面和渲染
使用新的字体初始化方法，修复中文乱码问题
"""

import pygame
import config_fixed as config
from shapes import Tetromino

class GameUI:
    """游戏界面类"""
    
    def __init__(self, screen):
        """初始化界面"""
        self.screen = screen
        
        # 使用配置文件中初始化的字体
        self.font = config.FONT
        self.small_font = config.SMALL_FONT
        
        # 如果字体未初始化，尝试初始化
        if self.font is None or self.small_font is None:
            print("⚠️  字体未初始化，尝试初始化...")
            config.init_fonts()
            self.font = config.FONT
            self.small_font = config.SMALL_FONT
        
        # 预渲染一些静态文本
        self.title_text = self.font.render("俄罗斯方块", True, config.COLORS['text']) if self.font else None
        self.score_text = self.small_font.render("分数", True, config.COLORS['text']) if self.small_font else None
        self.level_text = self.small_font.render("等级", True, config.COLORS['text']) if self.small_font else None
        self.lines_text = self.small_font.render("消除行数", True, config.COLORS['text']) if self.small_font else None
        self.time_text = self.small_font.render("游戏时间", True, config.COLORS['text']) if self.small_font else None
        self.next_text = self.small_font.render("下一个", True, config.COLORS['text']) if self.small_font else None
        self.paused_text = self.font.render("游戏暂停", True, config.COLORS['text']) if self.font else None
        self.game_over_text = self.font.render("游戏结束", True, config.COLORS['game_over']) if self.font else None
        self.restart_text = self.small_font.render("按R键重新开始", True, config.COLORS['text']) if self.small_font else None
        
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
        preview_width = 5 * config.GRID_SIZE
        preview_height = 5 * config.GRID_SIZE
        
        preview_rect = pygame.Rect(
            preview_x - 5,
            preview_y - 5,
            preview_width + 10,
            preview_height + 10
        )
        pygame.draw.rect(self.screen, config.COLORS['next_piece'], preview_rect)
        pygame.draw.rect(self.screen, config.COLORS['grid'], preview_rect, 2)
        
        # 绘制"下一个"文本
        if self.next_text:
            self.screen.blit(self.next_text, (preview_x, preview_y - 40))
        
        # 绘制下一个方块
        if next_piece:
            positions = next_piece.get_positions()
            for x, y in positions:
                # 调整位置到预览区域中心
                preview_center_x = preview_x + preview_width // 2
                preview_center_y = preview_y + preview_height // 2
                
                block_x = preview_center_x + (x - 2) * config.GRID_SIZE
                block_y = preview_center_y + (y - 2) * config.GRID_SIZE
                
                color_idx = next_piece.shape_type
                color = config.COLORS['tetromino'][color_idx]
                
                rect = pygame.Rect(
                    block_x,
                    block_y,
                    config.GRID_SIZE,
                    config.GRID_SIZE
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
    
    def draw_info(self, game_info):
        """绘制游戏信息（分数、等级、行数、时间）"""
        info_x = config.GAME_AREA_X + config.GRID_WIDTH * config.GRID_SIZE + 50
        info_y = config.GAME_AREA_Y + 300
        
        # 绘制分数
        if self.score_text:
            self.screen.blit(self.score_text, (info_x, info_y))
        
        score_value = str(game_info['score'])
        if self.small_font:
            score_text = self.small_font.render(score_value, True, config.COLORS['score'])
            self.screen.blit(score_text, (info_x + 80, info_y))
        
        # 绘制等级
        if self.level_text:
            self.screen.blit(self.level_text, (info_x, info_y + 40))
        
        level_value = str(game_info['level'])
        if self.small_font:
            level_text = self.small_font.render(level_value, True, config.COLORS['text'])
            self.screen.blit(level_text, (info_x + 80, info_y + 40))
        
        # 绘制消除行数
        if self.lines_text:
            self.screen.blit(self.lines_text, (info_x, info_y + 80))
        
        lines_value = str(game_info['lines_cleared'])
        if self.small_font:
            lines_text = self.small_font.render(lines_value, True, config.COLORS['text'])
            self.screen.blit(lines_text, (info_x + 80, info_y + 80))
        
        # 绘制游戏时间
        if self.time_text:
            self.screen.blit(self.time_text, (info_x, info_y + 120))
        
        time_value = f"{game_info['game_time']:.1f}秒"
        if self.small_font:
            time_text = self.small_font.render(time_value, True, config.COLORS['text'])
            self.screen.blit(time_text, (info_x + 80, info_y + 120))
    
    def draw_current_piece(self, current_piece):
        """绘制当前正在下落的方块"""
        if not current_piece:
            return
            
        positions = current_piece.get_positions()
        
        for x, y in positions:
            # 检查方块是否在游戏区域内
            if y >= 0:  # 只绘制在游戏区域内的方块
                color_idx = current_piece.shape_type
                color = config.COLORS['tetromino'][color_idx]
                
                rect = pygame.Rect(
                    config.GAME_AREA_X + x * config.GRID_SIZE,
                    config.GAME_AREA_Y + y * config.GRID_SIZE,
                    config.GRID_SIZE,
                    config.GRID_SIZE
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
    
    def draw_controls(self):
        """绘制控制说明"""
        controls_x = 50
        controls_y = config.GAME_AREA_Y + config.GRID_HEIGHT * config.GRID_SIZE + 30
        
        if not self.small_font:
            return
            
        for i, control_text in enumerate(self.controls):
            control_rendered = self.small_font.render(control_text, True, config.COLORS['text'])
            self.screen.blit(control_rendered, (controls_x, controls_y + i * 25))
    
    def draw_game_status(self, game_status):
        """绘制游戏状态（暂停、游戏结束）"""
        screen_center_x = config.SCREEN_WIDTH // 2
        screen_center_y = config.SCREEN_HEIGHT // 2
        
        if game_status == config.STATUS_PAUSED and self.paused_text:
            text_rect = self.paused_text.get_rect(center=(screen_center_x, screen_center_y))
            self.screen.blit(self.paused_text, text_rect)
            
            # 绘制继续提示
            if self.small_font:
                continue_text = self.small_font.render("按P键继续游戏", True, config.COLORS['text'])
                continue_rect = continue_text.get_rect(center=(screen_center_x, screen_center_y + 50))
                self.screen.blit(continue_text, continue_rect)
                
        elif game_status == config.STATUS_GAME_OVER and self.game_over_text:
            text_rect = self.game_over_text.get_rect(center=(screen_center_x, screen_center_y))
            self.screen.blit(self.game_over_text, text_rect)
            
            # 绘制重新开始提示
            if self.restart_text:
                restart_rect = self.restart_text.get_rect(center=(screen_center_x, screen_center_y + 50))
                self.screen.blit(self.restart_text, restart_rect)
    
    def draw_title(self):
        """绘制游戏标题"""
        if self.title_text:
            title_rect = self.title_text.get_rect(center=(config.SCREEN_WIDTH // 2, 30))
            self.screen.blit(self.title_text, title_rect)
    
    def draw(self, game_grid, game_info, current_piece, next_piece, game_status):
        """绘制完整的游戏画面"""
        # 绘制背景
        self.draw_background()
        
        # 绘制游戏网格和已锁定的方块
        self.draw_grid(game_grid)
        
        # 绘制当前正在下落的方块
        self.draw_current_piece(current_piece)
        
        # 绘制下一个方块预览
        self.draw_next_piece(next_piece)
        
        # 绘制游戏信息
        self.draw_info(game_info)
        
        # 绘制控制说明
        self.draw_controls()
        
        # 绘制游戏状态（暂停、游戏结束）
        self.draw_game_status(game_status)
        
        # 绘制游戏标题
        self.draw_title()