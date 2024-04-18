from .solution import Solution, Direction
from typing import List,Tuple
import json
import os
import numpy as np

class Solution_plus(Solution):
    """
    解决第二个任务
    若箱子被推到洞口后会消失，且箱子和洞口一一对应
    """
    def __init__(self, map:List[Tuple[int,int]],matrix_size:Tuple[int,int],level:int):
        self.level = level
        super().__init__(map,matrix_size)
        self.parse_box_target()
        self.get_box_positions_()


    def get_box_positions_(self) -> List[Tuple[int]]:
        """
        由于任务的变化，这里我们按照box_target的顺序返回箱子的位置
        """
        self.box_positions = []
        for k,v in self.box_target.items():
            self.box_positions.append(k)

    def parse_box_target(self):
        """
        解析箱子和目标的对应关系
        """
        self.box_target = {}
        json_path = os.path.join(os.path.dirname(__file__),"task2",f"level{self.level}.json")
        with open(json_path,"r") as f:
            box_target = json.load(f)
        for k,v in box_target.items():
            self.box_target[tuple(map(int,k.split(',')))] = tuple(map(int,v.split(',')))

    def is_solved(self, cur_boxes: List[Tuple[int]]) -> bool:
        """
        判断是否完成任务
        """
        for i in range(len(cur_boxes)):
            if cur_boxes[i] not in self.box_target:
                return False
        return True
    
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
        for i in range(len(box_positions)):
            if box_positions[i] == self.box_target[box_positions[i]]:
                # 如果箱子在目标位置上，则不更新箱子的位置，相当于删去箱子
                pass
            else:
                # 如果箱子不在对应的目标位置上，则更新箱子的位置
                map_matrix[box_positions[i]] = 3 if map_matrix[box_positions[i]] == 0 else 5
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

    def is_valid_move(self, cur_pos: Tuple, cur_boxes: List[Tuple[int]], dir: Direction) -> bool:
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
        for i in range(len(cur_boxes)):
            if cur_boxes[i] == self.box_target[cur_boxes[i]]:
                # 如果箱子在目标位置上，则不更新箱子的位置，相当于删去箱子
                pass
            else:
                # 如果箱子不在对应的目标位置上，则更新箱子的位置
                map_matrix[cur_boxes[i]] = 3 if map_matrix[cur_boxes[i]] == 0 else 5
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

    def heuristic(self, cur_boxes: List[Tuple[int]]) -> int:
        """
        重构启发式函数
        """
        h = 0
        for i in range(len(cur_boxes)):
            h += self.manhattan_distance(cur_boxes[i],self.box_target[cur_boxes[i]])
        return h
    
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
        