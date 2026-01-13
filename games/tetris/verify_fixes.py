"""
验证修复的逻辑
"""

import config_final as config
from shapes import Tetromino

print("=" * 50)
print("验证俄罗斯方块修复")
print("=" * 50)

# 测试1：验证控制说明位置计算
print("\n1. 验证控制说明位置计算:")
print(f"  屏幕高度: {config.SCREEN_HEIGHT}")
print(f"  游戏区域Y坐标: {config.GAME_AREA_Y}")
print(f"  网格高度: {config.GRID_HEIGHT}")
print(f"  网格大小: {config.GRID_SIZE}")
print(f"  游戏区域底部: {config.GAME_AREA_Y + config.GRID_HEIGHT * config.GRID_SIZE}")

# 原计算方式（有问题）
old_controls_y = config.GAME_AREA_Y + config.GRID_HEIGHT * config.GRID_SIZE + 30
print(f"  原控制说明Y坐标: {old_controls_y} (超出屏幕: {old_controls_y > config.SCREEN_HEIGHT})")

# 新计算方式（修复后）
new_controls_y = config.SCREEN_HEIGHT - 200
print(f"  新控制说明Y坐标: {new_controls_y} (在屏幕内: {new_controls_y <= config.SCREEN_HEIGHT})")

# 测试2：验证下一个方块预览位置计算
print("\n2. 验证下一个方块预览位置计算:")

# 测试所有形状
shape_names = ["I", "J", "L", "O", "S", "T", "Z"]

for i in range(7):
    piece = Tetromino(i)
    matrix = piece.matrix
    matrix_width = len(matrix[0])
    matrix_height = len(matrix)
    
    print(f"\n  形状 {shape_names[i]} ({i}):")
    print(f"    矩阵大小: {matrix_width}x{matrix_height}")
    
    # 预览区域设置
    preview_width = 5 * config.GRID_SIZE
    preview_height = 5 * config.GRID_SIZE
    
    # 计算偏移量
    offset_x = (preview_width - matrix_width * config.GRID_SIZE) // 2
    offset_y = (preview_height - matrix_height * config.GRID_SIZE) // 2
    
    print(f"    预览区域: {preview_width}x{preview_height}")
    print(f"    方块需要: {matrix_width * config.GRID_SIZE}x{matrix_height * config.GRID_SIZE}")
    print(f"    水平偏移: {offset_x}")
    print(f"    垂直偏移: {offset_y}")
    
    # 验证方块是否在预览区域内
    block_width = matrix_width * config.GRID_SIZE
    block_height = matrix_height * config.GRID_SIZE
    
    if offset_x >= 0 and offset_y >= 0:
        print(f"    ✓ 方块在预览区域内")
    else:
        print(f"    ✗ 方块可能超出预览区域")

# 测试3：验证原逻辑的问题
print("\n3. 验证原逻辑的问题:")
piece = Tetromino(0)  # I形状
positions = piece.get_positions()
print(f"  I形状的绝对位置: {positions}")

# 原逻辑计算
preview_center_x = 250  # 假设值
preview_center_y = 250  # 假设值

print(f"  原逻辑使用 (x-2, y-2) 偏移:")
for x, y in positions:
    block_x = preview_center_x + (x - 2) * config.GRID_SIZE
    block_y = preview_center_y + (y - 2) * config.GRID_SIZE
    print(f"    位置({x},{y}) -> 方块({block_x},{block_y})")

print("\n" + "=" * 50)
print("验证完成!")
print("=" * 50)