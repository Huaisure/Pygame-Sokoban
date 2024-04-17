import numpy as np
from enum import Enum
from ..assets import Map
from typing import List, Tuple

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Solution:
    def __init__(self, map:Map) -> None:
        self.map = map
        self.map_matrix = self.convert_map()
        self.pos = self.get_player_pos()# 玩家的位置

    def convert_map(self) -> np.ndarray:
        """
        将地图转换为numpy数组
        wall: 1, space: 0, target: 2, box: 3, player: 4, box on target: 5
        :return: numpy数组
        """
        map_array = np.zeros(self.map.matrix_size, dtype=int)
        for i in range(len(self.map.map_matrix)):
            for j in range(len(self.map.map_matrix[i])):
                char = self.map.map_matrix[i][j]
                if char == "#":
                    map_array[i][j] = 1
                elif char == " ":
                    map_array[i][j] = 0
                elif char == "O":
                    map_array[i][j] = 2
                elif char == "X":
                    map_array[i][j] = 3
                elif char == "P":
                    map_array[i][j] = 4
                elif char == "B":
                    map_array[i][j] = 5
        return map_array

    def is_valid_move(self, pos:tuple, dir:Direction) -> bool:
        """
        判断是否为合法的移动
        :param pos: 当前位置
        :param dir: 移动方向
        :return: 是否合法
        """
        x, y = pos
        map_matrix = self.map_matrix
        dx,dy = 0,0
        # 1: wall, 2: target, 3: box, 4: player, 5: box on target
        if dir == Direction.UP:
            dx = -1
        elif dir == Direction.DOWN:
            dx = 1
        elif dir == Direction.LEFT:
            dy = -1
        elif dir == Direction.RIGHT:
            dy = 1
        next_pos = (x+dx, y+dy)
        next_next_pos = (x+2*dx, y+2*dy)

        if map_matrix[next_pos] == 1:
            return False
        if map_matrix[next_pos] == 3 or map_matrix[next_pos] == 5:
            if map_matrix[next_next_pos] == 1 or map_matrix[next_next_pos] == 3 or map_matrix[next_next_pos] == 5:
                return False
        return True
    
    def get_possible_moves(self, pos:tuple) -> List[Direction]:
        """
        获取可能的移动
        :param pos: 当前位置
        :return: 可能的移动
        """
        moves = []
        for dir in Direction:
            if self.is_valid_move(pos, dir):
                moves.append(dir)
        return moves

    def get_player_pos(self) -> Tuple[int, int]:
        """
        获取玩家的位置
        :return: 玩家的位置
        """
        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                if self.map_matrix[i][j] == 4:
                    return (i, j)
        return None
    
    def move_player(self, dir: Direction) -> bool:
        """
        移动玩家
        :param dir: 移动方向
        """
        pos = self.pos
        x, y = pos
        dx, dy = (dir.value == 1) * -1 + (dir.value == 2), (dir.value == 3) * -1 + (dir.value == 4)
        self.map_matrix[x][y] = 0
        # 如果推动箱子了，那么更新箱子的位置
        if self.map_matrix[x+dx][y+dy] == 3 or self.map_matrix[x+dx][y+dy] == 5:
            # 如果x+2dx, y+2dy是目标位置
            if self.map_matrix[x+2*dx][y+2*dy] == 2:
                self.map_matrix[x+dx][y+dy] = 5
            else:
                self.map_matrix[x+dx][y+dy] = 3
        self.map_matrix[x+dx][y+dy] = 4
        self.pos = (x+dx, y+dy)
        return True
    
    def is_solved(self) -> bool:
        """
        判断是否解决
        :return: 是否解决
        """
        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                if self.map_matrix[i][j] == 3:
                    return False
        return True
    
    