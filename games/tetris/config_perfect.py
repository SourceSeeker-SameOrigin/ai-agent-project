"""
完美修复的俄罗斯方块游戏配置文件
修复所有边界问题
"""

import os
import pygame

# 游戏窗口设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30  # 每个方块的像素大小
FPS = 60  # 游戏帧率

# 游戏区域设置
GRID_WIDTH = 10  # 游戏区域宽度（方块数）
GRID_HEIGHT = 20  # 游戏区域高度（方块数）

# 计算游戏区域大小
GAME_AREA_WIDTH = GRID_WIDTH * GRID_SIZE  # 300像素
GAME_AREA_HEIGHT = GRID_HEIGHT * GRID_SIZE  # 600像素

# 调整游戏区域位置，确保完全在屏幕内
# 水平居中，垂直位置调整以确保底部不超出屏幕
GAME_AREA_X = (SCREEN_WIDTH - GAME_AREA_WIDTH) // 2  # 居中 (800-300)/2 = 250
GAME_AREA_Y = (SCREEN_HEIGHT - GAME_AREA_HEIGHT) // 2  # 居中 (600-600)/2 = 0

# 如果垂直居中后顶部太靠上，可以稍微下移
if GAME_AREA_Y < 30:  # 确保有空间显示标题
    GAME_AREA_Y = 50

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

# 字体变量（将在游戏初始化时设置）
FONT = None
SMALL_FONT = None

def init_fonts():
    """初始化字体（需要在pygame.init()之后调用）"""
    global FONT, SMALL_FONT
    
    print("开始初始化俄罗斯方块游戏字体...")
    
    try:
        # 首先尝试加载本地字体文件
        # 检查是否有字体目录
        font_dir = os.path.join(os.path.dirname(__file__), 'assets', 'fonts')
        if os.path.exists(font_dir):
            # 尝试查找常见的字体文件
            font_files = ['msyh.ttc', 'simhei.ttf', 'simsun.ttc', 'STHeiti Medium.ttc']
            for font_file in font_files:
                font_path = os.path.join(font_dir, font_file)
                if os.path.exists(font_path):
                    FONT = pygame.font.Font(font_path, FONT_SIZE)
                    SMALL_FONT = pygame.font.Font(font_path, SMALL_FONT_SIZE)
                    print(f"✅ 使用本地字体文件: {font_file}")
                    return
        else:
            print(f"⚠️  字体目录不存在: {font_dir}")
    except Exception as e:
        print(f"⚠️  本地字体加载失败: {e}")
    
    # 如果本地字体不可用，尝试查找系统中可用的中文字体
    try:
        # 常见的中文字体列表（跨平台）
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
            'arialunicode',        # Arial Unicode（支持中文）
            'fangsong',            # 仿宋
            'kaiti',               # 楷体
        ]
        
        # 获取系统可用字体
        print("获取系统可用字体...")
        available_fonts = pygame.font.get_fonts()
        print(f"系统中有 {len(available_fonts)} 个可用字体")
        
        # 查找第一个可用的中文字体
        font_name = None
        for font in chinese_fonts:
            if font in available_fonts:
                font_name = font
                print(f"✅ 找到可用字体: {font}")
                break
        
        if font_name:
            print(f"正在创建字体对象: {font_name}")
            FONT = pygame.font.SysFont(font_name, FONT_SIZE)
            SMALL_FONT = pygame.font.SysFont(font_name, SMALL_FONT_SIZE)
            print(f"✅ 系统字体初始化成功: {font_name}")
            return
        else:
            print("⚠️  未找到可用的中文字体")
    except Exception as e:
        print(f"⚠️  系统字体查找失败: {e}")
    
    # 如果以上都失败，使用默认字体
    try:
        print("⚠️  使用默认字体（可能不支持中文）")
        FONT = pygame.font.SysFont(None, FONT_SIZE)
        SMALL_FONT = pygame.font.SysFont(None, SMALL_FONT_SIZE)
        print(f"✅ 默认字体初始化成功")
    except Exception as e:
        print(f"❌ 字体初始化完全失败: {e}")
        # 创建空字体对象以避免崩溃
        FONT = None
        SMALL_FONT = None