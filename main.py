from assets import Map
import pygame


def main():
    my_map = Map(level=1, size=(800, 600))
    my_map.draw_map()
    pass


if __name__ == "__main__":
    main()
