import pygame


class Element:
    def __init__(self) -> None:
        self.player = None
        self.box = None
        self.wall = None
        self.target = None
        self.box_on_target = None
        self.space = None
        self.load()

    def load(self) -> None:
        self.player = pygame.image.load("img/player.png").convert()
        self.box = pygame.image.load("img/box.png").convert()
        self.wall = pygame.image.load("img/wall.png").convert()
        self.target = pygame.image.load("img/target.png").convert()
        self.box_on_target = pygame.image.load("img/box_on_target.png").convert()
        self.space = pygame.image.load("img/space.png").convert()
