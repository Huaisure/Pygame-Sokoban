from assets import Game
import pygame
from solution import Solution
import time

def main():
    # 生成游戏类
    my_game = Game(level=int(input("请输入关卡号（1-10）：")),size=(800, 600))
    # 生成解决类
    mySolution = Solution(my_game.map_matrix, my_game.matrix_size)
    path = mySolution.a_star_solution()
    my_game.draw_map(path)
    pass


if __name__ == "__main__":
    main()
