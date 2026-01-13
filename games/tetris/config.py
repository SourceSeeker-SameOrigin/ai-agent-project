"""
俄罗斯方块游戏配置文件
定义游戏的基本参数和常量
"""

# 游戏窗口设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30  # 每个方块的像素大小
FPS = 60  # 游戏帧率

# 游戏区域设置
GRID_WIDTH = 10  # 游戏区域宽度（方块数）
GRID_HEIGHT = 20  # 游戏区域高度（方块数）
GAME_AREA_X = 200  # 游戏区域左上角X坐标
GAME_AREA_Y = 50   # 游戏区域左上角Y坐标

# 颜色定义
COLORS = {
    'background': (15, 15, 30),
    'grid': (40, 40, 60),
    'text': (220, 220, 220),
    'score': (255, 215, 0),
    'next_piece': (80, 80, 100),
    'game_over': (220, 20, 60),
    'tetromino': {
        0: (0, 240, 240),    # I - 青色
        1: (0, 0, 240),      # J - 蓝色
        2: (240, 160, 0),    # L - 橙色
        3: (240, 240, 0),    # O - 黄色
        4: (0, 240, 0),      # S - 绿色
        5: (160, 0, 240),    # T - 紫色
        6: (240, 0, 0),      # Z - 红色
    }
}

# 游戏控制设置
FALL_SPEED = 0.5  # 初始下落速度（秒）
SPEED_INCREASE = 0.05  # 每级速度增加
MAX_SPEED = 0.1  # 最大下落速度

# 分数设置
SCORE_PER_LINE = 100
SCORE_PER_TETRIS = 800  # 一次消除4行的奖励
LEVEL_UP_LINES = 10  # 每消除多少行升一级

# 字体设置
FONT_SIZE = 24
SMALL_FONT_SIZE = 18

# 游戏状态
STATUS_PLAYING = 0
STATUS_PAUSED = 1
STATUS_GAME_OVER = 2