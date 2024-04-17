import numpy as np
from enum import Enum
from ..assets import Map

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Solution:
    def __init__(self, map:Map) -> None:
        self.map = map

    def is_valid_move(self, pos:tuple, dir:Direction) -> bool:
        """
        判断是否为合法的移动
        :param pos: 当前位置
        :param dir: 移动方向
        :return: 是否合法
        """
        x, y = pos
        if dir == Direction.UP:
            dst = (x-1, y)
