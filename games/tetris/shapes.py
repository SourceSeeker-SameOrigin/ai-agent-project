"""
俄罗斯方块形状定义
包含所有7种基本形状及其旋转状态
"""

import config

class Tetromino:
    """俄罗斯方块形状类"""
    
    # 7种基本形状的定义（4x4网格中的坐标）
    SHAPES = [
        # I 形状
        [
            [[0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],
            
            [[0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0]],
            
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0]],
            
            [[0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]]
        ],
        
        # J 形状
        [
            [[1, 0, 0],
             [1, 1, 1],
             [0, 0, 0]],
            
            [[0, 1, 1],
             [0, 1, 0],
             [0, 1, 0]],
            
            [[0, 0, 0],
             [1, 1, 1],
             [0, 0, 1]],
            
            [[0, 1, 0],
             [0, 1, 0],
             [1, 1, 0]]
        ],
        
        # L 形状
        [
            [[0, 0, 1],
             [1, 1, 1],
             [0, 0, 0]],
            
            [[0, 1, 0],
             [0, 1, 0],
             [0, 1, 1]],
            
            [[0, 0, 0],
             [1, 1, 1],
             [1, 0, 0]],
            
            [[1, 1, 0],
             [0, 1, 0],
             [0, 1, 0]]
        ],
        
        # O 形状
        [
            [[0, 1, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]],
            
            [[0, 1, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]],
            
            [[0, 1, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]],
            
            [[0, 1, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]]
        ],
        
        # S 形状
        [
            [[0, 1, 1],
             [1, 1, 0],
             [0, 0, 0]],
            
            [[0, 1, 0],
             [0, 1, 1],
             [0, 0, 1]],
            
            [[0, 0, 0],
             [0, 1, 1],
             [1, 1, 0]],
            
            [[1, 0, 0],
             [1, 1, 0],
             [0, 1, 0]]
        ],
        
        # T 形状
        [
            [[0, 1, 0],
             [1, 1, 1],
             [0, 0, 0]],
            
            [[0, 1, 0],
             [0, 1, 1],
             [0, 1, 0]],
            
            [[0, 0, 0],
             [1, 1, 1],
             [0, 1, 0]],
            
            [[0, 1, 0],
             [1, 1, 0],
             [0, 1, 0]]
        ],
        
        # Z 形状
        [
            [[1, 1, 0],
             [0, 1, 1],
             [0, 0, 0]],
            
            [[0, 0, 1],
             [0, 1, 1],
             [0, 1, 0]],
            
            [[0, 0, 0],
             [1, 1, 0],
             [0, 1, 1]],
            
            [[0, 1, 0],
             [1, 1, 0],
             [1, 0, 0]]
        ]
    ]
    
    def __init__(self, shape_type=None):
        """初始化方块"""
        import random
        
        if shape_type is None:
            shape_type = random.randint(0, 6)
        
        self.shape_type = shape_type
        self.rotation = 0
        self.x = config.GRID_WIDTH // 2 - 2  # 初始位置居中
        self.y = 0
        
        # 获取当前形状的矩阵
        self.matrix = self.SHAPES[shape_type][self.rotation]
        
    def rotate(self):
        """旋转方块"""
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % 4
        self.matrix = self.SHAPES[self.shape_type][self.rotation]
        return old_rotation
    
    def get_rotated(self):
        """获取旋转后的形状（不改变当前状态）"""
        new_rotation = (self.rotation + 1) % 4
        return self.SHAPES[self.shape_type][new_rotation]
    
    def get_color(self):
        """获取方块颜色"""
        return config.COLORS['tetromino'][self.shape_type]
    
    def get_positions(self):
        """获取方块在游戏区域中的位置列表"""
        positions = []
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if self.matrix[y][x]:
                    positions.append((self.x + x, self.y + y))
        return positions
    
    def clone(self):
        """克隆当前方块"""
        new_tetromino = Tetromino(self.shape_type)
        new_tetromino.rotation = self.rotation
        new_tetromino.x = self.x
        new_tetromino.y = self.y
        new_tetromino.matrix = self.matrix
        return new_tetromino