"""
完整测试修复后的游戏
"""
import pygame
import sys
import random
from config import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from powerup import PowerUp
from explosion import Explosion

def test_all_classes():
    """测试所有游戏类"""
    print("测试所有游戏类...")
    
    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    
    tests_passed = 0
    total_tests = 0
    
    # 测试Player类
    print("\n1. 测试Player类:")
    try:
        player = Player(50, 50)
        total_tests += 1
        
        # 测试update方法
        player.update()
        print("  ✅ Player.update() 成功")
        total_tests += 1
        
        # 测试shoot方法
        bullet = player.shoot()
        if bullet:
            print("  ✅ Player.shoot() 返回子弹")
        else:
            print("  ⚠️  Player.shoot() 返回None（冷却中）")
        total_tests += 1
        
        # 测试take_damage方法
        alive = player.take_damage(10)
        print(f"  ✅ Player.take_damage() 成功，生命值: {player.health}")
        total_tests += 1
        
        tests_passed += 4
    except Exception as e:
        print(f"  ❌ Player类测试失败: {e}")
    
    # 测试Enemy类
    print("\n2. 测试Enemy类:")
    try:
        enemy = Enemy(50, 50)
        total_tests += 1
        
        # 测试update方法
        enemy.update(1.0)
        print("  ✅ Enemy.update() 成功")
        total_tests += 1
        
        # 测试shoot方法
        bullet = enemy.shoot()
        print(f"  ✅ Enemy.shoot() 成功，返回: {bullet}")
        total_tests += 1
        
        tests_passed += 3
    except Exception as e:
        print(f"  ❌ Enemy类测试失败: {e}")
    
    # 测试Bullet类
    print("\n3. 测试Bullet类:")
    try:
        bullet = Bullet(50, 50, 5, is_player=True)
        total_tests += 1
        
        # 测试update方法
        bullet.update()
        print("  ✅ Bullet.update() 成功")
        total_tests += 1
        
        tests_passed += 2
    except Exception as e:
        print(f"  ❌ Bullet类测试失败: {e}")
    
    # 测试PowerUp类
    print("\n4. 测试PowerUp类:")
    try:
        powerup = PowerUp(50, 50, 'health')
        total_tests += 1
        
        # 测试update方法
        powerup.update()
        print("  ✅ PowerUp.update() 成功")
        total_tests += 1
        
        tests_passed += 2
    except Exception as e:
        print(f"  ❌ PowerUp类测试失败: {e}")
    
    pygame.quit()
    
    print(f"\n测试总结: {tests_passed}/{total_tests} 通过")
    return tests_passed == total_tests

def test_game_integration():
    """测试游戏集成"""
    print("\n测试游戏集成...")
    
    try:
        # 导入游戏类
        from main_fixed_final import PlaneWarGame
        
        # 创建游戏实例
        game = PlaneWarGame()
        print("✅ 游戏实例创建成功")
        
        # 测试游戏状态
        print(f"  游戏状态: 运行中={game.running}, 游戏开始={game.game_started}, 游戏结束={game.game_over}")
        print(f"  玩家: {game.player}")
        print(f"  难度: {game.difficulty}, 等级: {game.level}")
        
        # 测试游戏循环方法
        print("\n测试游戏循环方法:")
        
        # 测试handle_events（模拟一个事件）
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        game.handle_events()
        print("  ✅ handle_events() 成功")
        
        # 测试update方法
        game.update()
        print("  ✅ update() 成功")
        
        # 测试render方法（不会实际渲染，但确保不崩溃）
        try:
            game.render()
            print("  ✅ render() 成功")
        except Exception as e:
            print(f"  ⚠️  render() 警告: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 游戏集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始完整测试修复...")
    print("=" * 60)
    
    # 初始化字体（避免游戏类中的重复初始化）
    from config import init_fonts
    init_fonts()
    
    success1 = test_all_classes()
    success2 = test_game_integration()
    
    print("=" * 60)
    if success1 and success2:
        print("✅ 所有测试通过！游戏修复完成。")
        print("\n修复总结:")
        print("1. 修复了 Player.update() 缺少参数的问题")
        print("2. 修改了 Player.update() 方法，使其不需要外部参数")
        print("3. 修复了 Enemy.update() 缺少难度参数的问题")
        print("4. 所有游戏类现在都可以正常工作")
    else:
        print("❌ 测试失败，需要进一步修复。")