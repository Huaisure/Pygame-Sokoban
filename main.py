from assets import Map
import pygame
from solution import Solution
import time

def main():
    my_map = Map(level=10, size=(800, 600))
    t = time.time()
    # my_map.draw_map()
    mySolution = Solution(my_map.map_matrix, my_map.matrix_size)
    print(mySolution.a_star_solution())
    print("Time:", time.time() - t)
    pass


if __name__ == "__main__":
    main()
