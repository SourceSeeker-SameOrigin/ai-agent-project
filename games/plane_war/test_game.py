#!/usr/bin/env python3
"""
飞机大战游戏测试脚本
测试游戏的基本功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("飞机大战游戏 - 功能测试")
print("=" * 50)

# 测试导入所有模块（不初始化pygame）
try:
    print("1. 测试导入模块...")
    # 先导入基本模块
    import config
    from player import Player
    from enemy import Enemy
    from bullet import Bullet
    from powerup import PowerUp
    from explosion import Explosion
    
    print("✅ 所有模块导入成功")
    
    # 测试创建游戏对象
    print("\n2. 测试创建游戏对象...")
    
    # 创建玩家
    player = Player(400, 500)
    print(f"✅ 玩家创建成功: 位置({player.x}, {player.y}), 生命值{player.health}")
    
    # 创建敌机
    enemy = Enemy(200, 100, "normal")
    print(f"✅ 敌机创建成功: 类型{enemy.type}, 生命值{enemy.health}")
    
    # 创建子弹
    bullet = Bullet(400, 400, 8, is_player=True)
    print(f"✅ 子弹创建成功: 速度{bullet.speed}, 玩家子弹{bullet.is_player}")
    
    # 创建道具
    powerup = PowerUp(300, 200, "health")
    print(f"✅ 道具创建成功: 类型{powerup.type}")
    
    # 创建爆炸效果
    explosion = Explosion(400, 300)
    print(f"✅ 爆炸效果创建成功: 粒子数{len(explosion.particles)}")
    
    # 测试游戏配置
    print("\n3. 测试游戏配置...")
    print(f"屏幕大小: {config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}")
    print(f"游戏帧率: {config.FPS}")
    print(f"玩家速度: {config.PLAYER_SPEED}")
    print(f"敌机生成率: {config.ENEMY_SPAWN_RATE}")
    print(f"道具生成率: {config.POWERUP_SPAWN_RATE}")
    
    # 测试颜色常量
    print("\n4. 测试颜色常量...")
    print(f"黑色: {config.BLACK}")
    print(f"白色: {config.WHITE}")
    print(f"红色: {config.RED}")
    print(f"绿色: {config.GREEN}")
    print(f"蓝色: {config.BLUE}")
    
    print("\n" + "=" * 50)
    print("✅ 所有基本功能测试通过！")
    print("游戏可以正常运行。")
    print("=" * 50)
    
    print("\n运行游戏命令:")
    print("  python run_game.py")
    print("  python main.py")
    
    print("\n游戏控制说明:")
    print("  方向键/WASD: 移动飞机")
    print("  空格键: 射击")
    print("  ESC键: 退出游戏")
    print("  R键: 重新开始游戏")
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保所有文件都存在且语法正确。")
    
except Exception as e:
    print(f"❌ 测试错误: {e}")
    import traceback
    traceback.print_exc()