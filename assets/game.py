from .elements import Element

from typing import List, Tuple
import pygame
import os
import sys
import json


BUTTON_HEIGHT = 50


class Game(Element):
    """
    游戏类
    绘制地图，读取地图
    """

    def __init__(
        self,
        level: int,
        size: tuple = (800, 600),
        task: int = 1,
        if_random: bool = False,
    ) -> None:

        # 用于在更新地图时，两种不同的任务模式
        self.task = task

        ### 随机生成箱子、目标和玩家的位置
        self.if_random = if_random

        ### 初始化pygame
        pygame.display.init()
        pygame.display.set_caption("Sokoban")
        self.map_size = size
        self.screen = pygame.display.set_mode(
            (self.map_size[0], self.map_size[1] + BUTTON_HEIGHT)
        )
        pygame.font.init()
        super().__init__()
        self.init_button()

        ### 初始化游戏地图
        self.level = level
        self.game_info = self.get_game_info()

    def get_game_info(self) -> dict:
        """
        从文件中读取地图, 在这个函数中需要完成一些基本量的获取
        self.matrix_size: 地图的大小
        self.player_pos: 玩家的位置
        self.box_target: 箱子和目标的对应关系
        self.target_pos: 目标的位置
        self.map_matrix: 地图矩阵
        self.box_positions: 箱子的位置
        :return: 地图矩阵
        """
        self.box_positions = []
        self.target_positions = []
        self.box_target = {}
        self.matrix_size = (0, 0)
        map_path = os.path.join(
            os.path.dirname(__file__), "levels", f"level{self.level}.json"
        )
        game_info = {}
        with open(map_path, "r") as f:
            # 更新为json格式
            dict = json.load(f)
            matrix = dict["layout"]
            # 将地图中的空格填充为最长的行
            max_length = max([len(row) for row in matrix])
            matrix = [list(row.ljust(max_length, " ")) for row in matrix]
            self.matrix_size = (len(matrix), len(matrix[0]))
            # matrix读取了地图，其中没有箱子和目标的位置，以及玩家的位置，只有墙和空地
            if not self.if_random:
                # 如果不随机生成地图，加载下面的内容
                box_target = dict["box_target"]
                i = 0
                for k, v in box_target.items():
                    # 更新箱子和目标的位置
                    matrix[int(k.split(",")[0])][int(k.split(",")[1])] = "$"
                    matrix[int(v.split(",")[0])][int(v.split(",")[1])] = "."
                    self.target_positions.append(tuple(map(int, v.split(","))))
                    self.box_positions.append(tuple(map(int, k.split(","))))
                    # 用序号代替箱子，因为箱子的位置可能会变化
                    self.box_target[i] = tuple(map(int, v.split(",")))
                    i += 1
                self.player_pos = tuple(map(int, dict["player"].split(",")))
                matrix[self.player_pos[0]][self.player_pos[1]] = "@"
            else:
                # 随机生成箱子、目标和玩家的位置，这里我们保证和原来的箱子的数量一致
                box_target = dict["box_target"]
                num_of_box = len(box_target)
                # 检测可选的位置
                available_pos = []
                # 除第一行和最后一行，每一行的墙之间的位置都可以放置箱子
                for i in range(1, len(matrix) - 1):
                    for j in range(len(dict["layout"][i])):
                        if dict["layout"][i][j] == " ":  # 空地
                            available_pos.append((i, j))

                # 随机生成箱子和目标的位置
                import random

                random.shuffle(available_pos)
                for i in range(2 * num_of_box):
                    if i % 2 == 1:
                        matrix[available_pos[i][0]][available_pos[i][1]] = "."
                        self.target_positions.append(tuple(available_pos[i]))
                        self.box_target[i // 2] = tuple(available_pos[i])
                    else:
                        matrix[available_pos[i][0]][available_pos[i][1]] = "$"
                        self.box_positions.append(tuple(available_pos[i]))

                # 随机生成玩家的位置
                self.player_pos = available_pos[-1]
                matrix[self.player_pos[0]][self.player_pos[1]] = "@"

        self.map_matrix = matrix
        game_info["layout"] = self.map_matrix
        game_info["player_pos"] = self.player_pos
        game_info["box_target"] = self.box_target
        game_info["box_positions"] = self.box_positions
        game_info["target_positions"] = self.target_positions
        game_info["matrix_size"] = self.matrix_size
        game_info["level"] = self.level

        return game_info

    def box_to_target(self, box_pos: Tuple[int, int]) -> bool:
        """
        判断箱子是否在目标位置
        """
        index = self.box_positions.index(box_pos)
        return self.box_target[index] == box_pos

    def draw_map(self, a_star_solution) -> None:
        """
        绘制地图
        :return: None
        """
        move_sequence = a_star_solution
        self.path = move_sequence
        move_index = 0
        last_move_time = pygame.time.get_ticks()
        move_interval = 200  # 移动间隔，以毫秒为单位
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill((221, 213, 172))
            self.draw_button()
            if self.playing:
                current_time = pygame.time.get_ticks()
                if current_time - last_move_time > move_interval:
                    if move_index < len(move_sequence):
                        # print(move_sequence[move_index])
                        self.update_position(move_sequence[move_index])
                        move_index += 1
                        last_move_time = current_time

            self.draw_map_elements()
            pygame.display.update()
            clock.tick(60)

    def draw_map_elements(self) -> None:
        """
        绘制地图元素
        """
        screen = self.screen

        # 根据matrix_size和screen的size调整每个元素的大小
        new_image_size = min(
            self.map_size[0] // self.matrix_size[0],
            self.map_size[1] // self.matrix_size[1],
        )

        self.player = pygame.transform.scale(
            self.player, (new_image_size, new_image_size)
        )
        self.box = pygame.transform.scale(self.box, (new_image_size, new_image_size))
        self.wall = pygame.transform.scale(self.wall, (new_image_size, new_image_size))
        self.target = pygame.transform.scale(
            self.target, (new_image_size, new_image_size)
        )
        self.box_on_target = pygame.transform.scale(
            self.box_on_target, (new_image_size, new_image_size)
        )
        self.space = pygame.transform.scale(
            self.space, (new_image_size, new_image_size)
        )

        # 铺上底色, self.space
        for i in range(self.map_size[1] // new_image_size):
            for j in range(self.map_size[0] // new_image_size):
                screen.blit(
                    self.space, (j * new_image_size, i * new_image_size + BUTTON_HEIGHT)
                )
        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                x_pos = j * new_image_size
                y_pos = i * new_image_size + BUTTON_HEIGHT
                if self.map_matrix[i][j] == "#":
                    screen.blit(self.wall, (x_pos, y_pos))
                elif self.map_matrix[i][j] == "$":
                    screen.blit(self.box, (x_pos, y_pos))
                elif self.map_matrix[i][j] == "@":
                    screen.blit(self.player, (x_pos, y_pos))
                elif self.map_matrix[i][j] == ".":
                    screen.blit(self.target, (x_pos, y_pos))
                elif self.map_matrix[i][j] == "*":
                    screen.blit(self.box_on_target, (x_pos, y_pos))
                elif self.map_matrix[i][j] == " ":
                    screen.blit(self.space, (x_pos, y_pos))
        pass

    def update_position(self, direction):
        """
        更新玩家位置和箱子位置
        :param direction: 移动方向
        """
        x, y = self.player_pos
        dx, dy = 0, 0
        if direction.value == 1:
            dx = -1
        elif direction.value == 2:
            dx = 1
        elif direction.value == 3:
            dy = -1
        elif direction.value == 4:
            dy = 1
        new_x, new_y = x + dx, y + dy

        if self.task == 1:

            if (
                self.map_matrix[new_x][new_y] == "$"
                or self.map_matrix[new_x][new_y] == "*"
            ):
                # 如果推箱子了，更新箱子
                new_box_x, new_box_y = new_x + dx, new_y + dy
                if self.map_matrix[new_box_x][new_box_y] == ".":
                    self.map_matrix[new_box_x][new_box_y] = "*"
                else:
                    self.map_matrix[new_box_x][new_box_y] = "$"

            self.player_pos = new_x, new_y
            # 如果原来的位置为target，更新为target
            self.map_matrix[x][y] = "." if (x, y) in self.target_positions else " "
            self.map_matrix[new_x][new_y] = "@"

        elif self.task == 2:
            if (
                self.map_matrix[new_x][new_y] == "$"
                or self.map_matrix[new_x][new_y] == "*"
            ):
                box_pos = (new_x, new_y)
                new_box_x, new_box_y = new_x + dx, new_y + dy
                self.box_positions[self.box_positions.index(box_pos)] = (
                    new_box_x,
                    new_box_y,
                )
                # 判断箱子如果推到了目标位置
                if self.box_to_target((new_box_x, new_box_y)):
                    # 将目标位置的箱子删除，变为空地
                    self.map_matrix[new_box_x][new_box_y] = "."
                else:
                    if self.map_matrix[new_box_x][new_box_y] == ".":
                        self.map_matrix[new_box_x][new_box_y] = "*"
                    else:
                        self.map_matrix[new_box_x][new_box_y] = "$"
                # 如果原来的位置为target，更新为target
            self.player_pos = new_x, new_y

            self.map_matrix[x][y] = "." if (x, y) in self.target_positions else " "
            self.map_matrix[new_x][new_y] = "@"
            # 打印map_matrix
            # for row in self.map_matrix:
            #     print(row)
            # pass

    def init_button(self):
        self.button_color = (0, 200, 0)  # 按钮颜色
        self.button_hover_color = (0, 255, 0)  # 鼠标悬停时的颜色
        self.quit_button_color = (200, 0, 0)  # Quit按钮颜色
        self.quit_button_hover_color = (255, 0, 0)  # Quit按钮鼠标悬停颜色

        self.button_rect = pygame.Rect(0, 0, 200, 50)  # 按钮的位置和大小
        self.quit_button_rect = pygame.Rect(200, 0, 200, 50)  # Quit按钮的位置和大小

        self.button_text = "Create Solution"
        self.font = pygame.font.Font(None, 36)  # 文字字体和大小
        self.playing = False  # 控制是否开始播放解决方案

    def draw_button(self):
        mouse_pos = pygame.mouse.get_pos()  # 获取鼠标位置
        mouse_clicked = pygame.mouse.get_pressed()[0]  # 检查鼠标是否被点击

        if self.button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(
                self.screen, self.button_hover_color, self.button_rect
            )  # 鼠标悬停效果
            if mouse_clicked and not self.playing:
                if self.path is None:
                    pygame.quit()  # 退出游戏
                    print("Game exited")
                    sys.exit()
                self.playing = True  # 设置播放状态为True

        else:
            pygame.draw.rect(self.screen, self.button_color, self.button_rect)

        if self.path is None:
            self.button_text = "No Solution"
        text_surf = self.font.render(self.button_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surf, text_rect)

        if self.quit_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(
                self.screen, self.quit_button_hover_color, self.quit_button_rect
            )
            if mouse_clicked:
                pygame.quit()  # 退出游戏
                print("Game exited")
                sys.exit()
        else:
            pygame.draw.rect(self.screen, self.quit_button_color, self.quit_button_rect)
        quit_text_surf = self.font.render("Quit", True, (255, 255, 255))
        quit_text_rect = quit_text_surf.get_rect(center=self.quit_button_rect.center)
        self.screen.blit(quit_text_surf, quit_text_rect)
