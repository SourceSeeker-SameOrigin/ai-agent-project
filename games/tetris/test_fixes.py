"""
测试修复的问题：
1. 控制说明是否显示
2. 下一个方块是否在矩形框内
"""

import pygame
import sys
import config_final as config
from shapes import Tetromino

# 初始化pygame
pygame.init()

# 创建窗口
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("测试修复")

# 初始化字体
config.init_fonts()

# 创建一些测试方块
test_pieces = [
    Tetromino(0),  # I形状
    Tetromino(1),  # J形状
    Tetromino(2),  # L形状
    Tetromino(3),  # O形状
    Tetromino(4),  # S形状
    Tetromino(5),  # T形状
    Tetromino(6),  # Z形状
]

current_test = 0

# 控制说明
controls = [
    "控制说明:",
    "← → : 左右移动",
    "↑ : 旋转",
    "↓ : 加速下落",
    "空格 : 硬降落",
    "P : 暂停/继续",
    "R : 重新开始",
    "ESC : 退出游戏"
]

# 创建字体
font = pygame.font.SysFont(None, 24)
small_font = pygame.font.SysFont(None, 18)

def draw_next_piece_test(piece, screen):
    """测试绘制下一个方块"""
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
    pygame.draw.rect(screen, (80, 80, 100), preview_rect)
    pygame.draw.rect(screen, (40, 40, 60), preview_rect, 2)
    
    # 绘制"下一个"文本
    next_text = small_font.render("下一个", True, (220, 220, 220))
    screen.blit(next_text, (preview_x, preview_y - 40))
    
    # 绘制下一个方块（使用修复后的逻辑）
    if piece:
        # 获取方块的形状矩阵
        matrix = piece.matrix
        color_idx = piece.shape_type
        color = config.COLORS['tetromino'][color_idx]
        
        # 计算方块在预览区域中的位置
        matrix_width = len(matrix[0])
        matrix_height = len(matrix)
        
        # 计算偏移量，使方块居中
        offset_x = (preview_width - matrix_width * config.GRID_SIZE) // 2
        offset_y = (preview_height - matrix_height * config.GRID_SIZE) // 2
        
        # 绘制方块
        for y in range(matrix_height):
            for x in range(matrix_width):
                if matrix[y][x]:
                    block_x = preview_x + offset_x + x * config.GRID_SIZE
                    block_y = preview_y + offset_y + y * config.GRID_SIZE
                    
                    rect = pygame.Rect(
                        block_x,
                        block_y,
                        config.GRID_SIZE,
                        config.GRID_SIZE
                    )
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)
        
        # 显示矩阵信息
        info_text = font.render(f"形状: {piece.shape_type}, 大小: {matrix_width}x{matrix_height}", True, (255, 255, 255))
        screen.blit(info_text, (preview_x, preview_y + preview_height + 10))

def draw_controls_test(screen):
    """测试绘制控制说明"""
    controls_x = 50
    controls_y = config.SCREEN_HEIGHT - 200
    
    for i, control_text in enumerate(controls):
        control_rendered = small_font.render(control_text, True, (220, 220, 220))
        screen.blit(control_rendered, (controls_x, controls_y + i * 25))

# 主循环
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RIGHT:
                current_test = (current_test + 1) % len(test_pieces)
            elif event.key == pygame.K_LEFT:
                current_test = (current_test - 1) % len(test_pieces)
    
    # 清屏
    screen.fill((15, 15, 30))
    
    # 绘制标题
    title = font.render("测试修复：下一个方块预览和控制说明", True, (220, 220, 220))
    screen.blit(title, (50, 30))
    
    # 绘制说明
    instruction = small_font.render("使用左右箭头键切换不同形状的方块", True, (180, 180, 180))
    screen.blit(instruction, (50, 70))
    
    # 绘制下一个方块测试
    draw_next_piece_test(test_pieces[current_test], screen)
    
    # 绘制控制说明测试
    draw_controls_test(screen)
    
    # 显示当前测试的方块类型
    shape_names = ["I", "J", "L", "O", "S", "T", "Z"]
    current_shape = shape_names[current_test]
    shape_text = font.render(f"当前测试形状: {current_shape}", True, (255, 255, 255))
    screen.blit(shape_text, (50, 120))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()