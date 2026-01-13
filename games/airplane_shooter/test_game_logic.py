"""
测试游戏逻辑（不依赖pygame）
"""

from config import *
from player import Player
from enemy import Enemy
from bullet import Bullet

def test_bullet_creation():
    """测试子弹创建"""
    print("测试子弹创建...")
    bullet = Bullet(100, 100)
    assert bullet.x == 100
    assert bullet.y == 100
    assert bullet.active == True
    print("✓ 子弹创建测试通过")

def test_enemy_creation():
    """测试敌机创建"""
    print("测试敌机创建...")
    enemy = Enemy(800)
    assert enemy.width == ENEMY_WIDTH
    assert enemy.height == ENEMY_HEIGHT
    assert enemy.active == True
    print("✓ 敌机创建测试通过")

def test_player_creation():
    """测试玩家创建"""
    print("测试玩家创建...")
    player = Player(800, 600)
    assert player.width == PLAYER_WIDTH
    assert player.height == PLAYER_HEIGHT
    assert player.health == PLAYER_HEALTH
    print("✓ 玩家创建测试通过")

def test_config_values():
    """测试配置值"""
    print("测试配置值...")
    assert SCREEN_WIDTH == 800
    assert SCREEN_HEIGHT == 600
    assert FPS == 60
    assert PLAYER_SPEED == 5
    assert ENEMY_SPEED_MIN == 1
    assert ENEMY_SPEED_MAX == 3
    print("✓ 配置值测试通过")

def main():
    """主测试函数"""
    print("=" * 50)
    print("飞机射击游戏 - 逻辑测试")
    print("=" * 50)
    
    try:
        test_config_values()
        test_bullet_creation()
        test_enemy_creation()
        test_player_creation()
        
        print("\n" + "=" * 50)
        print("所有逻辑测试通过！")
        print("=" * 50)
        print("\n游戏代码结构正确，可以安装pygame后运行完整游戏。")
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        return False
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()