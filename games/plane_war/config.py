"""
飞机大战游戏配置文件
包含游戏常量、颜色、路径等配置
"""

import os
import pygame

# 游戏窗口设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GAME_TITLE = "飞机大战 - Plane War"

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

# 玩家设置
PLAYER_SPEED = 5
PLAYER_HEALTH = 100
PLAYER_SHOOT_COOLDOWN = 200  # 毫秒
PLAYER_BULLET_SPEED = 8

# 敌机设置
ENEMY_SPEED_MIN = 1
ENEMY_SPEED_MAX = 3
ENEMY_SPAWN_RATE = 60  # 每60帧生成一个敌机
ENEMY_HEALTH = 30
ENEMY_SHOOT_CHANCE = 0.01  # 每帧射击概率

# 子弹设置
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
ENEMY_BULLET_SPEED = 4

# 爆炸效果
EXPLOSION_DURATION = 20  # 帧数
EXPLOSION_PARTICLES = 30

# 游戏难度
DIFFICULTY_INCREASE_RATE = 0.001  # 每帧难度增加
MAX_DIFFICULTY = 5.0

# 分数系统
ENEMY_KILL_SCORE = 100
BOSS_KILL_SCORE = 1000
HEALTH_PICKUP_SCORE = 50
SCORE_MULTIPLIER = 1.0

# 道具设置
POWERUP_SPAWN_RATE = 300  # 每300帧生成一个道具
POWERUP_TYPES = ['health', 'speed', 'fire_rate', 'shield']

# 资源路径
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# 字体变量（将在游戏初始化时设置）
FONT_SMALL = None
FONT_MEDIUM = None
FONT_LARGE = None

def init_fonts():
    """初始化字体（需要在pygame.init()之后调用）"""
    global FONT_SMALL, FONT_MEDIUM, FONT_LARGE
    
    print("开始初始化字体...")
    
    try:
        # 首先尝试加载本地字体文件
        FONT_PATH = os.path.join(ASSETS_DIR, 'fonts', 'msyh.ttc')
        print(f"检查本地字体文件: {FONT_PATH}")
        if os.path.exists(FONT_PATH):
            FONT_SMALL = pygame.font.Font(FONT_PATH, 20)
            FONT_MEDIUM = pygame.font.Font(FONT_PATH, 30)
            FONT_LARGE = pygame.font.Font(FONT_PATH, 40)
            print("✅ 使用本地字体文件: msyh.ttc")
            print(f"字体初始化结果: SMALL={FONT_SMALL}, MEDIUM={FONT_MEDIUM}, LARGE={FONT_LARGE}")
            return
        else:
            print(f"⚠️  本地字体文件不存在: {FONT_PATH}")
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
            FONT_SMALL = pygame.font.SysFont(font_name, 24)
            FONT_MEDIUM = pygame.font.SysFont(font_name, 36)
            FONT_LARGE = pygame.font.SysFont(font_name, 48)
            print(f"✅ 系统字体初始化成功: {font_name}")
            print(f"字体初始化结果: SMALL={FONT_SMALL}, MEDIUM={FONT_MEDIUM}, LARGE={FONT_LARGE}")
            return
        else:
            print("⚠️  未找到可用的中文字体")
    except Exception as e:
        print(f"⚠️  系统字体查找失败: {e}")
    
    # 如果以上都失败，使用默认字体
    try:
        print("⚠️  使用默认字体（可能不支持中文）")
        FONT_SMALL = pygame.font.SysFont(None, 24)
        FONT_MEDIUM = pygame.font.SysFont(None, 36)
        FONT_LARGE = pygame.font.SysFont(None, 48)
        print(f"✅ 默认字体初始化成功")
        print(f"字体初始化结果: SMALL={FONT_SMALL}, MEDIUM={FONT_MEDIUM}, LARGE={FONT_LARGE}")
    except Exception as e:
        print(f"❌ 字体初始化完全失败: {e}")
        # 创建空字体对象以避免崩溃
        FONT_SMALL = None
        FONT_MEDIUM = None
        FONT_LARGE = None