from elements import Element
import pygame
import os


class Map(Element):
    """
    地图类
    绘制地图，读取地图
    """

    def __init__(self, level: int, size: tuple = (800, 600)) -> None:
        pygame.display.init()
        pygame.display.set_caption("pySokoban")
        size = (800, 600)
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        super().__init__()
        self.level = level
        self.map_matrix = self.get_map()
        self.matrix_size = None
        pass

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
                matrix_size = max(matrix_size[0], len(row)), matrix_size[1] + 1
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

            self.draw_map_elements(screen)
            pygame.display.update()
            clock.tick(fps)

    def draw_map_elements(self) -> None:
        """
        绘制地图元素
        """
        screen = self.screen



        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                if self.map_matrix[i][j] == "#":
                    screen.blit(self.wall, (j * 50, i * 50))
                elif self.map_matrix[i][j] == "$":
                    screen.blit(self.box, (j * 50, i * 50))
                elif self.map_matrix[i][j] == "@":
                    screen.blit(self.player, (j * 50, i * 50))
                elif self.map_matrix[i][j] == ".":
                    screen.blit(self.target, (j * 50, i * 50))
                elif self.map_matrix[i][j] == "*":
                    screen.blit(self.box_on_target, (j * 50, i * 50))
                elif self.map_matrix[i][j] == " ":
                    screen.blit(self.space, (j * 50, i * 50))
        pass
