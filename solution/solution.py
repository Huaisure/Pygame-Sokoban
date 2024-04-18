import numpy as np
from enum import Enum
from typing import List, Tuple
from queue import PriorityQueue

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Solution:
    def __init__(self, map:List[Tuple[int,int]],matrix_size:Tuple[int,int]) -> None:
        self.map = map
        self.matrix_size = matrix_size[1],matrix_size[0]
        self.map_matrix = self.convert_map()
        self.goal_positions = self.get_target_positions()  # 目标位置
        self.box_positions = self.get_box_positions()  # 箱子位置
        self.pos = self.get_player_pos()# 玩家的位置

        # 由于地图中的元素除了玩家和箱子外，都是不可变的，所以我们可以有一个没有玩家和箱子的地图
        self.fixed_map_matrix = np.copy(self.map_matrix)
        self.fixed_map_matrix[self.fixed_map_matrix == 4] = 0
        self.fixed_map_matrix[self.fixed_map_matrix == 3] = 0
        self.fixed_map_matrix[self.fixed_map_matrix == 5] = 2

        ###### A*算法相关 ######
        # 进行A*算法时不能改变原有的地图，我们只需要维护玩家的位置和箱子的位置即可
        self.open_set = PriorityQueue()  # A*算法中的开放列表
        self.came_from = {}  # 跟踪路径
        self.g_score = {}  # 从初始状态到当前状态的成本
        self.f_score = {}  # 预估的总成本
        ########################

    def convert_map(self) -> np.ndarray:
        """
        将地图转换为numpy数组
        wall: 1, space: 0, target: 2, box: 3, player: 4, box on target: 5
        :return: numpy数组
        """
        map_array = np.zeros(self.matrix_size, dtype=int)
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                char = self.map[i][j]
                if char == "#":
                    map_array[i][j] = 1
                elif char == " ":
                    map_array[i][j] = 0
                elif char == ".":
                    map_array[i][j] = 2
                elif char == "$":
                    map_array[i][j] = 3
                elif char == "@":
                    map_array[i][j] = 4
                elif char == "*":
                    map_array[i][j] = 5
        return map_array

    def is_valid_move(self, cur_pos:tuple, cur_boxes:List[Tuple[int,int]],dir:Direction) -> bool:
        """
        判断是否为合法的移动
        :param cur_pos: 当前位置
        :param cur_boxes: 当前箱子的位置
        :param dir: 移动方向
        :return: 是否合法
        """
        x, y = cur_pos
        # TODO
        map_matrix = np.copy(self.fixed_map_matrix)
        for box in cur_boxes:
            map_matrix[box] = 3 if map_matrix[box] == 0 else 5
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
    
    def get_possible_moves(self, pos:tuple, boxes:List[Tuple[int,int]]) -> List[Direction]:
        """
        获取可能的移动
        :param pos: 当前位置
        :return: 可能的移动
        """
        moves = []
        for dir in Direction:
            if self.is_valid_move(pos, boxes, dir):
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
    
    def move_player(self, pos:Tuple[int,int] ,dir: Direction, box_positions:List[Tuple[int,int]])->Tuple[Tuple[int,int],Tuple[List[Tuple[int,int]]]]:
        """
        移动玩家
        :param pos: 当前位置
        :param dir: 移动方向
        :param box_positions: 箱子的位置
        :return: 移动后玩家的位置和箱子的位置, 以及是否被剪枝
        """
        new_boxes = [box for box in box_positions]
        x, y = pos
        dx, dy = (dir.value == 1) * -1 + (dir.value == 2), (dir.value == 3) * -1 + (dir.value == 4)
        map_matrix = np.copy(self.fixed_map_matrix) 
        for box in box_positions:
            map_matrix[box] = 3 if map_matrix[box] == 0 else 5
        next_pos = (x+dx, y+dy)
        next_next_pos = (x+2*dx, y+2*dy)
        is_pruned = False
        if next_pos in box_positions:
            new_boxes.remove(next_pos)
            new_boxes.append(next_next_pos)
            is_pruned = self.is_pruned(next_next_pos)
            # if is_pruned:
            #     print("pruned")
        return (x+dx, y+dy), tuple(new_boxes), is_pruned
    
    def is_pruned(self,box:Tuple[int,int])->bool:
        """
        判断是否被剪枝，如果箱子无法再被移动，且箱子不在目标上，则被剪枝
        """
        x, y = box
        # 如果箱子在目标位置上，则不剪枝
        if box in self.goal_positions:
            return False
        # 如果箱子周围存左上、左下、右上、右下都是墙，则剪枝
        left = (self.fixed_map_matrix[x][y-1] == 1)
        right = (self.fixed_map_matrix[x][y+1] == 1)
        up = (self.fixed_map_matrix[x-1][y] == 1)
        down = (self.fixed_map_matrix[x+1][y] == 1)
        if (left and up) or (left and down) or (right and up) or (right and down):
            return True
        return False
    
    def is_solved(self, cur_boxes:List[Tuple[int,int]]) -> bool:
        """
        判断是否解决
        :return: 是否解决
        """
        return set(cur_boxes) == set(self.goal_positions)
    
    def get_box_positions(self) -> List[Tuple[int, int]]:
        """
        获取箱子的位置
        :return: 箱子的位置
        """
        box_positions = []
        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                if self.map_matrix[i][j] == 3 or self.map_matrix[i][j] == 5:
                    box_positions.append((i, j))
        return box_positions
    
    def get_target_positions(self) -> Tuple[List[Tuple[int, int]]]:
        """
        获取目标位置
        :return: 目标位置
        """
        target_positions = []
        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                if self.map_matrix[i][j] == 2 or self.map_matrix[i][j] == 5:
                    target_positions.append((i, j))
        return tuple(target_positions)
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """
        曼哈顿距离
        :param pos1: 位置1
        :param pos2: 位置2
        :return: 曼哈顿距离
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def heuristic(self, cur_boxes:List[Tuple[int,int]]) -> int:
        """
        启发式函数，采用曼哈顿距离
        :return: 启发式函数值
        """
        box_positions = cur_boxes
        target_positions = self.goal_positions
        total_distance = 0
        for box_pos in box_positions:
            min_distance = float("inf")
            for target_pos in target_positions:
                d = self.manhattan_distance(box_pos, target_pos)
                if d < min_distance:
                    min_distance = d
            total_distance += min_distance
        return total_distance

    def a_star_solution(self):
        """
        A*算法求解
        """
        start = (self.pos, tuple(self.box_positions)) # 使用tuple，list是不可哈希的
        self.g_score[start] = 0
        self.f_score[start] = self.heuristic(self.box_positions)
        self.open_set.put((self.f_score[start], start))

        while not self.open_set.empty():
            current_f, current = self.open_set.get()
            current_pos, current_boxes = current

            # 判断是否解决
            if self.is_solved(current_boxes):
                return self.reconstruct_path(current)
            
            # 生成新的移动状态
            for dir in self.get_possible_moves(current_pos, current_boxes):
                new_pos, new_boxes, is_pruned = self.move_player(current_pos, dir, current_boxes)
                new_state = (new_pos, tuple(new_boxes))
                # print(new_state)
                # print(is_pruned)
                tentative_g_score = self.g_score[current] + 1 # 代价函数，这里是移动一步，所以是1

                # 如果新状态没有被访问过或者代价更小
                if new_state not in self.g_score or tentative_g_score < self.g_score[new_state]:
                    self.came_from[new_state] = (current, dir)
                    self.g_score[new_state] = tentative_g_score
                    self.f_score[new_state] = tentative_g_score + self.heuristic(new_boxes)
                    if not is_pruned:
                        self.open_set.put((self.f_score[new_state], new_state))
        return "No solution found!"

    def reconstruct_path(self, current):
        """重建路径"""
        total_path = []
        while current in self.came_from:
            current, direction = self.came_from[current]
            total_path.append(direction)
        total_path.reverse()  # 因为我们是从目标回溯到起点的
        return total_path
    
