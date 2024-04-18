from assets import Map
import pygame
from solution import Solution

def main():
    my_map = Map(level=1, size=(800, 600))
    # my_map.draw_map()
    mySolution = Solution(my_map.map_matrix, my_map.matrix_size)
    print(mySolution.a_star_solution())
    pass


if __name__ == "__main__":
    main()
