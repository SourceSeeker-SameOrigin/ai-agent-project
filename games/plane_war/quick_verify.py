"""
快速验证修复
"""

import subprocess
import time
import signal
import sys

def run_game_with_timeout(timeout=3):
    """运行游戏并设置超时"""
    print("启动游戏测试...")
    print("游戏将运行3秒，然后自动退出")
    print("请观察是否有错误信息")
    print("-" * 50)
    
    try:
        # 启动游戏进程
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd="./plane_war_game",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待指定时间
        time.sleep(timeout)
        
        # 终止进程
        process.terminate()
        process.wait(timeout=2)
        
        # 获取输出
        stdout, stderr = process.communicate()
        
        print("游戏输出:")
        print(stdout[:500])  # 只显示前500个字符
        
        if stderr:
            print("\n错误输出:")
            print(stderr[:500])
            
        # 检查是否有错误
        if "Traceback" in stderr or "Error" in stderr or "error" in stderr:
            print("\n❌ 发现错误！")
            return False
        else:
            print("\n✅ 游戏运行正常（无错误信息）")
            return True
            
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        return False

def main():
    """主函数"""
    print("验证游戏修复")
    print("=" * 50)
    
    # 测试1：检查语法
    print("\n1. 检查所有文件语法...")
    files_to_check = ["main.py", "player.py", "explosion.py", "enemy.py", "bullet.py", "powerup.py"]
    all_syntax_ok = True
    
    for file in files_to_check:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", f"./plane_war_game/{file}"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"  ✅ {file}: 语法正确")
            else:
                print(f"  ❌ {file}: 语法错误")
                print(f"     错误: {result.stderr[:100]}")
                all_syntax_ok = False
        except Exception as e:
            print(f"  ❌ {file}: 检查失败 - {e}")
            all_syntax_ok = False
    
    # 测试2：运行游戏
    print("\n2. 运行游戏测试...")
    game_ok = run_game_with_timeout(3)
    
    # 总结
    print("\n" + "=" * 50)
    print("验证结果:")
    print(f"语法检查: {'✅ 全部通过' if all_syntax_ok else '❌ 有错误'}")
    print(f"游戏运行: {'✅ 正常' if game_ok else '❌ 有错误'}")
    
    if all_syntax_ok and game_ok:
        print("\n🎉 所有修复验证通过！")
        print("游戏现在应该可以正常运行，空格键射击功能应该正常。")
    else:
        print("\n⚠️  验证未完全通过，请检查上述问题。")

if __name__ == "__main__":
    main()