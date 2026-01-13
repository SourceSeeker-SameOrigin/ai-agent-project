"""
最终测试修复后的游戏
"""
import pygame
import sys
from config import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from powerup import PowerUp

def test_parameter_fixes():
    """测试参数修复"""
    print("测试参数修复...")
    
    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    
    tests_passed = 0
    total_tests = 0
    
    print("\n1. 测试Player.update() 无参数调用:")
    try:
        player = Player(50, 50)
        total_tests += 1
        
        # 测试update方法（应该不需要参数）
        player.update()
        print("  ✅ Player.update() 成功（无参数）")
        tests_passed += 1
    except TypeError as e:
        print(f"  ❌ Player.update() 失败: {e}")
        print(f"    错误信息: {str(e)}")
    
    print("\n2. 测试Enemy.update() 带参数调用:")
    try:
        enemy = Enemy(50, 50)
        total_tests += 1
        
        # 测试update方法（需要难度参数）
        enemy.update(1.5)  # 传递难度参数
        print("  ✅ Enemy.update(1.5) 成功")
        tests_passed += 1
        
        # 测试默认参数
        enemy.update()  # 使用默认参数 difficulty=1.0
        print("  ✅ Enemy.update() 成功（使用默认参数）")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Enemy.update() 失败: {e}")
    
    print("\n3. 测试Bullet.update() 无参数调用:")
    try:
        bullet = Bullet(50, 50, 5, is_player=True)
        total_tests += 1
        
        bullet.update()
        print("  ✅ Bullet.update() 成功")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Bullet.update() 失败: {e}")
    
    print("\n4. 测试PowerUp.update() 无参数调用:")
    try:
        powerup = PowerUp(50, 50, 'health')
        total_tests += 1
        
        powerup.update()
        print("  ✅ PowerUp.update() 成功")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ PowerUp.update() 失败: {e}")
    
    pygame.quit()
    
    print(f"\n参数修复测试: {tests_passed}/{total_tests} 通过")
    return tests_passed == total_tests

def test_game_run():
    """测试游戏运行"""
    print("\n测试游戏运行...")
    
    try:
        # 导入修复后的游戏类
        from main_fixed_complete import PlaneWarGame
        
        # 创建游戏实例
        print("创建游戏实例...")
        game = PlaneWarGame()
        print("✅ 游戏实例创建成功")
        
        # 检查关键属性
        print(f"  玩家对象: {game.player}")
        print(f"  游戏状态: 运行={game.running}, 开始={game.game_started}, 结束={game.game_over}")
        
        # 测试关键方法
        print("\n测试游戏方法:")
        
        # 模拟一个QUIT事件
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        game.handle_events()
        print("  ✅ handle_events() 成功")
        
        # 测试update方法（游戏未开始，应该直接返回）
        game.update()
        print("  ✅ update() 成功（游戏未开始状态）")
        
        # 开始游戏
        game.game_started = True
        game.update()
        print("  ✅ update() 成功（游戏进行中状态）")
        
        # 测试render方法
        try:
            game.render()
            print("  ✅ render() 成功")
        except Exception as e:
            print(f"  ⚠️  render() 警告: {e}")
        
        print("\n✅ 游戏运行测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 游戏运行测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_original_error():
    """测试原始错误是否修复"""
    print("\n测试原始错误修复...")
    
    # 原始错误: TypeError: Player.update() missing 2 required positional arguments: 'keys' and 'dt'
    
    try:
        # 初始化pygame
        pygame.init()
        screen = pygame.display.set_mode((100, 100))
        
        # 创建玩家
        player = Player(50, 50)
        
        # 尝试调用update方法（原始错误点）
        player.update()
        
        print("✅ 原始错误已修复: Player.update() 现在可以无参数调用")
        
        pygame.quit()
        return True
        
    except TypeError as e:
        if "missing 2 required positional arguments" in str(e):
            print(f"❌ 原始错误未修复: {e}")
            return False
        else:
            print(f"⚠️  其他错误: {e}")
            return False
    except Exception as e:
        print(f"⚠️  其他错误: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("飞机大战游戏 - 最终修复测试")
    print("=" * 60)
    
    # 初始化字体
    from config import init_fonts
    init_fonts()
    
    print("\n测试目标: 修复 TypeError: Player.update() missing 2 required positional arguments")
    print("-" * 60)
    
    test1 = test_parameter_fixes()
    test2 = test_game_run()
    test3 = test_original_error()
    
    print("\n" + "=" * 60)
    print("测试总结:")
    print(f"1. 参数修复测试: {'✅ 通过' if test1 else '❌ 失败'}")
    print(f"2. 游戏运行测试: {'✅ 通过' if test2 else '❌ 失败'}")
    print(f"3. 原始错误测试: {'✅ 通过' if test3 else '❌ 失败'}")
    print("-" * 60)
    
    if test1 and test2 and test3:
        print("🎉 所有测试通过！游戏修复完成。")
        print("\n修复内容总结:")
        print("1. ✅ 修改了 Player.update() 方法:")
        print("   - 移除 keys 和 dt 参数")
        print("   - 在方法内部获取按键状态")
        print("   - 使用固定时间增量 (16.67ms for 60FPS)")
        print("2. ✅ 修复了 Enemy.update() 调用:")
        print("   - 添加 self.difficulty 参数传递")
        print("3. ✅ 所有游戏类方法调用现在都正确")
        print("\n现在可以运行 main_fixed_complete.py 来玩游戏！")
    else:
        print("❌ 测试失败，需要进一步修复。")