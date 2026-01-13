"""
测试下一个方块预览问题
"""

import pygame
import sys
import config_final as config
from shapes import Tetromino

# 初始化pygame
pygame.init()

# 创建一个小窗口用于测试
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("测试下一个方块预览")

# 初始化字体
config.init_fonts()

# 创建一个方块
tetromino = Tetromino(0)  # I形状

# 获取方块的位置
positions = tetromino.get_positions()
print("方块位置:", positions)

# 计算预览区域
preview_x = 100
preview_y = 100
preview_width = 5 * config.GRID_SIZE
preview_height = 5 * config.GRID_SIZE

# 绘制预览区域
preview_rect = pygame.Rect(
    preview_x - 5,
    preview_y - 5,
    preview_width + 10,
    preview_height + 10
)

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # 清屏
    screen.fill((0, 0, 0))
    
    # 绘制预览区域
    pygame.draw.rect(screen, (80, 80, 100), preview_rect)
    pygame.draw.rect(screen, (40, 40, 60), preview_rect, 2)
    
    # 绘制方块（使用当前有问题的逻辑）
    preview_center_x = preview_x + preview_width // 2
    preview_center_y = preview_y + preview_height // 2
    
    for x, y in positions:
        # 当前有问题的逻辑
        block_x = preview_center_x + (x - 2) * config.GRID_SIZE
        block_y = preview_center_y + (y - 2) * config.GRID_SIZE
        
        rect = pygame.Rect(
            block_x,
            block_y,
            config.GRID_SIZE,
            config.GRID_SIZE
        )
        pygame.draw.rect(screen, (0, 240, 240), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 1)
        
        # 显示坐标信息
        font = pygame.font.SysFont(None, 16)
        coord_text = font.render(f"({x},{y})", True, (255, 255, 255))
        screen.blit(coord_text, (block_x, block_y - 15))
    
    # 显示预览区域中心
    pygame.draw.circle(screen, (255, 0, 0), (preview_center_x, preview_center_y), 3)
    
    # 显示说明
    font = pygame.font.SysFont(None, 20)
    text = font.render("红色点: 预览区域中心", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    
    pygame.display.flip()

pygame.quit()
sys.exit()