import pygame
import os


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
        base_dir = os.path.dirname(__file__)
        self.player = pygame.image.load(os.path.join(base_dir,"img/player.png")).convert()
        self.box = pygame.image.load(os.path.join(base_dir,"img/box.png")).convert()
        self.wall = pygame.image.load(os.path.join(base_dir,"img/wall.png")).convert()
        self.target = pygame.image.load(os.path.join(base_dir,"img/target.png")).convert()
        self.box_on_target = pygame.image.load(os.path.join(base_dir,"img/box_on_target.png")).convert()
        self.space = pygame.image.load(os.path.join(base_dir,"img/space.png")).convert()
