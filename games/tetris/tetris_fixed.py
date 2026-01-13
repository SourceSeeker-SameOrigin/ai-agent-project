"""
修复后的俄罗斯方块游戏
修复问题：
1. 控制说明没展示
2. 右侧的下一个方块不在矩形框里面
"""

import pygame
import sys
import time
import config_final as config
from game_fixed import TetrisGame
from ui_fixed_final import GameUI

class TetrisApp:
    """俄罗斯方块应用程序类"""
    
    def __init__(self):
        """初始化游戏"""
        pygame.init()
        
        # 初始化字体
        config.init_fonts()
        
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("俄罗斯方块")
        
        # 创建游戏时钟
        self.clock = pygame.time.Clock()
        
        # 创建游戏实例和UI
        self.game = TetrisGame()
        self.ui = GameUI(self.screen)
        
        # 按键状态（用于连续移动）
        self.key_states = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_DOWN: False
        }
        
        # 按键延迟计时器
        self.key_timers = {
            pygame.K_LEFT: 0,
            pygame.K_RIGHT: 0,
            pygame.K_DOWN: 0
        }
        
        # 按键延迟设置（秒）
        self.key_delays = {
            'initial': 0.2,  # 首次按键延迟
            'repeat': 0.05   # 重复按键延迟
        }
        
        # 游戏运行标志
        self.running = True
        
    def handle_events(self):
        """处理游戏事件"""
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
                elif event.key == pygame.K_r:
                    # 重新开始游戏
                    self.game.reset_game()
                    
                elif event.key == pygame.K_p:
                    # 暂停/继续游戏
                    self.game.toggle_pause()
                    
                elif event.key == pygame.K_SPACE:
                    # 硬降落
                    if self.game.game_status == config.STATUS_PLAYING:
                        self.game.hard_drop()
                        
                elif event.key == pygame.K_UP:
                    # 旋转方块
                    if self.game.game_status == config.STATUS_PLAYING:
                        self.game.rotate_piece()
                        
                elif event.key == pygame.K_LEFT:
                    # 左移
                    if self.game.game_status == config.STATUS_PLAYING:
                        self.game.move_piece(-1, 0)
                    self.key_states[pygame.K_LEFT] = True
                    self.key_timers[pygame.K_LEFT] = current_time + self.key_delays['initial']
                    
                elif event.key == pygame.K_RIGHT:
                    # 右移
                    if self.game.game_status == config.STATUS_PLAYING:
                        self.game.move_piece(1, 0)
                    self.key_states[pygame.K_RIGHT] = True
                    self.key_timers[pygame.K_RIGHT] = current_time + self.key_delays['initial']
                    
                elif event.key == pygame.K_DOWN:
                    # 加速下落
                    if self.game.game_status == config.STATUS_PLAYING:
                        self.game.move_piece(0, 1)
                    self.key_states[pygame.K_DOWN] = True
                    self.key_timers[pygame.K_DOWN] = current_time + self.key_delays['initial']
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.key_states[pygame.K_LEFT] = False
                elif event.key == pygame.K_RIGHT:
                    self.key_states[pygame.K_RIGHT] = False
                elif event.key == pygame.K_DOWN:
                    self.key_states[pygame.K_DOWN] = False
        
        # 处理连续按键
        if self.game.game_status == config.STATUS_PLAYING:
            self.handle_continuous_input(current_time)
    
    def handle_continuous_input(self, current_time):
        """处理连续按键输入"""
        # 左右移动
        if self.key_states[pygame.K_LEFT] and current_time >= self.key_timers[pygame.K_LEFT]:
            self.game.move_piece(-1, 0)
            self.key_timers[pygame.K_LEFT] = current_time + self.key_delays['repeat']
            
        if self.key_states[pygame.K_RIGHT] and current_time >= self.key_timers[pygame.K_RIGHT]:
            self.game.move_piece(1, 0)
            self.key_timers[pygame.K_RIGHT] = current_time + self.key_delays['repeat']
            
        # 加速下落
        if self.key_states[pygame.K_DOWN] and current_time >= self.key_timers[pygame.K_DOWN]:
            self.game.move_piece(0, 1)
            self.key_timers[pygame.K_DOWN] = current_time + self.key_delays['repeat']
    
    def update(self, delta_time):
        """更新游戏状态"""
        self.game.update(delta_time)
    
    def render(self):
        """渲染游戏画面"""
        # 获取游戏状态
        game_grid = self.game.get_grid()
        game_info = self.game.get_game_info()
        current_piece = self.game.current_piece
        next_piece = self.game.next_piece
        game_status = self.game.game_status
        
        # 使用UI绘制所有内容
        self.ui.draw(game_grid, game_info, current_piece, next_piece, game_status)
        
        # 更新显示
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        last_time = time.time()
        
        while self.running:
            # 计算时间增量
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time
            
            # 处理事件
            self.handle_events()
            
            # 更新游戏状态
            self.update(delta_time)
            
            # 渲染游戏画面
            self.render()
            
            # 控制帧率
            self.clock.tick(config.FPS)
        
        # 退出游戏
        pygame.quit()
        sys.exit()

def main():
    """主函数"""
    app = TetrisApp()
    app.run()

if __name__ == "__main__":
    main()