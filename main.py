from assets import Game
import pygame
from solution import Solution, Solution_plus
import time

def main():
    # 生成游戏类
    level = int(input("请输入关卡号（1-10）："))
    my_game = Game(level=level,size=(800, 600))

    task = int(input("完成任务1 or 任务2：(请输入1或2)"))

    if task == 1:
        # 生成解决类
        mySolution = Solution(my_game.map_matrix, my_game.matrix_size)
        # A*算法求解， 任务1：若箱子被推到洞口后不会消失（可以再次被推出来），且箱子和洞口不存在一一对应的关系，找到最优的移动路线
        path = mySolution.a_star_solution()
    else:
        # 若箱子被推到洞口后会消失，且箱子和洞口一一对应，找到最优的移动路线
        mySolution_plus = Solution_plus(my_game.map_matrix, my_game.matrix_size, level=level)
        path = mySolution_plus.a_star_solution()
    print(path)
    # my_game.draw_map(path)
    pass


if __name__ == "__main__":
    main()
