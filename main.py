from assets import Game
import pygame
from solution import Solution, Solution_plus
import sys
import time


def main():
    # 读取任务和关卡号
    print("欢迎来到推箱子游戏！")
    print(
        "*任务1：若箱子被推到洞口后不会消失（可以再次被推出来），且箱子和洞口不存在一一对应的关系，找到最优的移动路线"
    )
    print("*任务2：若箱子被推到洞口后会消失，且箱子和洞口一一对应，找到最优的移动路线")
    task = int(input("完成任务1 or 任务2(请输入1或2)："))
    level = int(input("请输入关卡号（1-10）："))
    assert level in range(1, 11), "关卡号输入错误"

    if_random = int(input("是否随机生成地图（0:固定 or 1:随机）："))

    # 生成游戏类
    my_game = Game(level=level, size=(800, 600), task=task, if_random=if_random)

    if task == 1:
        # 生成解决类
        mySolution = Solution(my_game.game_info)
        # A*算法求解， 任务1：若箱子被推到洞口后不会消失（可以再次被推出来），且箱子和洞口不存在一一对应的关系，找到最优的移动路线
        path = mySolution.a_star_solution()
    else:
        # 若箱子被推到洞口后会消失，且箱子和洞口一一对应，找到最优的移动路线
        mySolution_plus = Solution_plus(my_game.game_info)
        path = mySolution_plus.a_star_solution()

    # 打印路径
    print("path:")
    if "No" in path:
        print("No solution")
        path = None
    else:
        for i in path:
            if i.value == 1:
                print("up->", end=" ")
            elif i.value == 2:
                print("down->", end=" ")
            elif i.value == 3:
                print("left->", end=" ")
            elif i.value == 4:
                print("right->", end=" ")
    print()

    # 可视化
    my_game.draw_map(path)
    pass


if __name__ == "__main__":
    main()
