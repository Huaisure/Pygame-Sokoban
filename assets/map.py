from .elements import Element
import pygame
import os


class Map(Element):
    """
    地图类
    绘制地图，读取地图
    """

    def __init__(self, level: int, size: tuple = (800, 600)) -> None:
        pygame.display.init()
        pygame.display.set_caption("Sokoban")
        self.map_size = size
        self.screen = pygame.display.set_mode(self.map_size)
        # self.screen.fill((0, 0, 0))
        # Initialise font support
        # pygame.font.init()
        super().__init__()
        self.level = level
        self.matrix_size = None
        self.map_matrix = self.get_map()

    def get_map(self) -> list:
        """
        从文件中读取地图
        :return: 地图矩阵
        """
        matrix = []
        self.matrix_size = (0, 0)
        map_path = os.path.join(
            os.path.dirname(__file__), "levels", f"level{self.level}"
        )
        with open(map_path, "r") as f:
            for row in f.read().splitlines():
                matrix.append(list(row))
                self.matrix_size = max(self.matrix_size[0], len(row)), self.matrix_size[1] + 1
        return matrix

    def draw_map(self) -> None:
        """
        绘制地图
        :param screen: 游戏窗口
        :return: None
        """
        screen = self.screen
        clock = pygame.time.Clock()
        fps = 30

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.draw_map_elements()
            pygame.display.update()
            clock.tick(fps)

    def draw_map_elements(self) -> None:
        """
        绘制地图元素
        """
        screen = self.screen

        # 根据matrix_size和screen的size调整每个元素的大小
        new_image_size = min(self.map_size[0] // self.matrix_size[0], self.map_size[1] // self.matrix_size[1])
        
        self.player = pygame.transform.scale(self.player, (new_image_size, new_image_size))
        self.box = pygame.transform.scale(self.box, (new_image_size, new_image_size))
        self.wall = pygame.transform.scale(self.wall, (new_image_size, new_image_size))
        self.target = pygame.transform.scale(self.target, (new_image_size, new_image_size))
        self.box_on_target = pygame.transform.scale(self.box_on_target, (new_image_size, new_image_size))
        self.space = pygame.transform.scale(self.space, (new_image_size, new_image_size))

        # 铺上底色, self.space
        for i in range(self.map_size[1] // new_image_size):
            for j in range(self.map_size[0] // new_image_size):
                screen.blit(self.space, (j * new_image_size, i * new_image_size))
        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                if self.map_matrix[i][j] == "#":
                    screen.blit(self.wall, (j * new_image_size, i * new_image_size))
                elif self.map_matrix[i][j] == "$":
                    screen.blit(self.box, (j * new_image_size, i * new_image_size))
                elif self.map_matrix[i][j] == "@":
                    screen.blit(self.player, (j * new_image_size, i * new_image_size))
                elif self.map_matrix[i][j] == ".":
                    screen.blit(self.target, (j * new_image_size, i * new_image_size))
                elif self.map_matrix[i][j] == "*":
                    screen.blit(self.box_on_target, (j * new_image_size, i * new_image_size))
                elif self.map_matrix[i][j] == " ":
                    screen.blit(self.space, (j * new_image_size, i * new_image_size))
        pass
