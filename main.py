from assets import Map
import pygame
from solution import Solution
import time

def main():
    map_style = "magic_sokoban6"
    my_map = Map(level=9,map_style=map_style, size=(800, 600))
    t = time.time()
    # my_map.draw_map()
    mySolution = Solution(my_map.map_matrix, my_map.matrix_size)
    print(mySolution.a_star_solution())
    print("Time:", time.time() - t)
    pass


if __name__ == "__main__":
    main()
