"""
俄罗斯方块游戏核心逻辑
包含游戏状态管理、碰撞检测、消行等功能
"""

import random
import time
import config
from shapes import Tetromino

class TetrisGame:
    """俄罗斯方块游戏类"""
    
    def __init__(self):
        """初始化游戏"""
        self.reset_game()
        
    def reset_game(self):
        """重置游戏状态"""
        # 游戏区域网格，0表示空，1-7表示不同颜色的方块
        self.grid = [[0 for _ in range(config.GRID_WIDTH)] 
                    for _ in range(config.GRID_HEIGHT)]
        
        # 游戏状态
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_status = config.STATUS_PLAYING
        self.fall_time = 0
        self.fall_speed = config.FALL_SPEED
        
        # 当前方块和下一个方块
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        
        # 游戏时间
        self.start_time = time.time()
        self.game_time = 0
        
    def update(self, delta_time):
        """更新游戏状态"""
        if self.game_status != config.STATUS_PLAYING:
            return
            
        self.game_time = time.time() - self.start_time
        
        # 更新方块下落
        self.fall_time += delta_time
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            if not self.move_piece(0, 1):
                # 方块无法下落，锁定到网格
                self.lock_piece()
                self.check_lines()
                self.spawn_new_piece()
                
                # 检查游戏是否结束
                if self.check_game_over():
                    self.game_status = config.STATUS_GAME_OVER
    
    def move_piece(self, dx, dy):
        """移动当前方块"""
        self.current_piece.x += dx
        self.current_piece.y += dy
        
        if self.check_collision():
            # 发生碰撞，回退移动
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            return False
            
        return True
    
    def rotate_piece(self):
        """旋转当前方块"""
        old_rotation = self.current_piece.rotation
        self.current_piece.rotate()
        
        if self.check_collision():
            # 发生碰撞，尝试墙踢（wall kick）
            # 尝试向右移动
            self.current_piece.x += 1
            if not self.check_collision():
                return True
                
            # 尝试向左移动
            self.current_piece.x -= 2
            if not self.check_collision():
                return True
                
            # 尝试向上移动
            self.current_piece.x += 1
            self.current_piece.y -= 1
            if not self.check_collision():
                return True
                
            # 所有尝试都失败，恢复原状
            self.current_piece.rotation = old_rotation
            self.current_piece.matrix = self.current_piece.SHAPES[self.current_piece.shape_type][old_rotation]
            return False
            
        return True
    
    def hard_drop(self):
        """硬降落：直接落到底部"""
        while self.move_piece(0, 1):
            pass
        self.lock_piece()
        self.check_lines()
        self.spawn_new_piece()
        
        if self.check_game_over():
            self.game_status = config.STATUS_GAME_OVER
    
    def check_collision(self):
        """检查当前方块是否与网格或其他方块碰撞"""
        positions = self.current_piece.get_positions()
        
        for x, y in positions:
            # 检查边界
            if x < 0 or x >= config.GRID_WIDTH or y < 0 or y >= config.GRID_HEIGHT:
                return True
                
            # 检查与已锁定方块的碰撞
            if y >= 0 and self.grid[y][x]:
                return True
                
        return False
    
    def lock_piece(self):
        """将当前方块锁定到网格中"""
        positions = self.current_piece.get_positions()
        
        for x, y in positions:
            if y >= 0:  # 只锁定在游戏区域内的方块
                self.grid[y][x] = self.current_piece.shape_type + 1  # +1因为0表示空
    
    def spawn_new_piece(self):
        """生成新的方块"""
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        
        # 重置方块位置
        self.current_piece.x = config.GRID_WIDTH // 2 - 2
        self.current_piece.y = 0
    
    def check_lines(self):
        """检查并消除完整的行"""
        lines_to_clear = []
        
        # 找出完整的行
        for y in range(config.GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)
        
        if not lines_to_clear:
            return
            
        # 计算得分
        lines_count = len(lines_to_clear)
        if lines_count == 4:
            self.score += config.SCORE_PER_TETRIS
        else:
            self.score += lines_count * config.SCORE_PER_LINE * self.level
            
        self.lines_cleared += lines_count
        
        # 更新等级和速度
        new_level = self.lines_cleared // config.LEVEL_UP_LINES + 1
        if new_level > self.level:
            self.level = new_level
            self.fall_speed = max(config.MAX_SPEED, 
                                 config.FALL_SPEED - (self.level - 1) * config.SPEED_INCREASE)
        
        # 消除行并下移上面的行
        for line in sorted(lines_to_clear):
            # 移除该行
            del self.grid[line]
            # 在顶部添加新的空行
            self.grid.insert(0, [0 for _ in range(config.GRID_WIDTH)])
    
    def check_game_over(self):
        """检查游戏是否结束"""
        # 检查新生成的方块是否立即碰撞
        return self.check_collision()
    
    def toggle_pause(self):
        """切换暂停状态"""
        if self.game_status == config.STATUS_PLAYING:
            self.game_status = config.STATUS_PAUSED
        elif self.game_status == config.STATUS_PAUSED:
            self.game_status = config.STATUS_PLAYING
    
    def get_game_info(self):
        """获取游戏信息"""
        return {
            'score': self.score,
            'level': self.level,
            'lines': self.lines_cleared,
            'time': int(self.game_time),
            'next_piece': self.next_piece,
            'status': self.game_status
        }
    
    def get_grid(self):
        """获取游戏网格（包含当前方块）"""
        # 创建包含当前方块的网格副本
        display_grid = [row[:] for row in self.grid]
        
        if self.game_status == config.STATUS_PLAYING:
            positions = self.current_piece.get_positions()
            for x, y in positions:
                if 0 <= y < config.GRID_HEIGHT and 0 <= x < config.GRID_WIDTH:
                    display_grid[y][x] = self.current_piece.shape_type + 1
        
        return display_grid