from .elements import Element

from enum import Enum
from typing import List
import pygame
import os
import sys

BUTTON_HEIGHT = 50


class Game(Element):
    """
    游戏类
    绘制地图，读取地图
    """

    def __init__(self, level: int, size: tuple = (800, 600)) -> None:

        ### 初始化pygame
        pygame.display.init()
        pygame.display.set_caption("Sokoban")
        self.map_size = size
        self.screen = pygame.display.set_mode((self.map_size[0], self.map_size[1] + BUTTON_HEIGHT))
        pygame.font.init()
        super().__init__()    
        self.init_button()


        ### 初始化游戏地图
        self.level = level
        self.matrix_size = None
        self.map_matrix = self.get_map()
        self.player_pos = self.get_player_pos()
        self.target_pos = self.get_target_pos()
        

    def get_map(self) -> list:
        """
        从文件中读取地图
        :return: 地图矩阵
        """
        matrix = []
        self.matrix_size = (0, 0)
        map_path = os.path.join(
            os.path.dirname(__file__),"levels",  f"level{self.level}"
        )
        with open(map_path, "r") as f:
            for row in f.read().splitlines():
                matrix.append(list(row))
                self.matrix_size = max(self.matrix_size[0], len(row)), self.matrix_size[1] + 1
        return matrix

    def get_player_pos(self) -> tuple:
        """
        获取玩家的位置
        :return: 玩家的位置
        """
        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                if self.map_matrix[i][j] == "@":
                    return i, j
        return None
    
    def get_target_pos(self) -> list:
        """
        获取目标位置
        :return: 目标位置
        """
        target_pos = []
        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                if self.map_matrix[i][j] == ".":
                    target_pos.append((i, j))
        return target_pos

    def draw_map(self, a_star_solution) -> None:
        """
        绘制地图
        :return: None
        """
        move_sequence = a_star_solution
        move_index = 0
        last_move_time = pygame.time.get_ticks()
        move_interval = 200  # 移动间隔，以毫秒为单位
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill((221,213,172))
            self.draw_button()
            if self.playing:
                current_time = pygame.time.get_ticks()
                if current_time - last_move_time > move_interval:
                    if move_index < len(move_sequence):
                        print(move_sequence[move_index])
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
                screen.blit(self.space, (j * new_image_size, i * new_image_size+BUTTON_HEIGHT))
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

        if self.map_matrix[new_x][new_y] == "$" or self.map_matrix[new_x][new_y] == "*":
            # 如果推箱子了，更新箱子
            new_box_x, new_box_y = new_x + dx, new_y + dy
            if self.map_matrix[new_box_x][new_box_y] == ".":
                self.map_matrix[new_box_x][new_box_y] = "*"
            else:
                self.map_matrix[new_box_x][new_box_y] = "$"
            
        self.player_pos = new_x, new_y
        # 如果原来的位置为target，更新为target
        self.map_matrix[x][y] = "." if (x,y) in self.target_pos else " "
        self.map_matrix[new_x][new_y] = "@"

    
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
            pygame.draw.rect(self.screen, self.button_hover_color, self.button_rect)  # 鼠标悬停效果
            if mouse_clicked and not self.playing:
                self.playing = True  # 设置播放状态为True
        else:
            pygame.draw.rect(self.screen, self.button_color, self.button_rect)

        text_surf = self.font.render(self.button_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surf, text_rect)

        if self.quit_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.quit_button_hover_color, self.quit_button_rect)
            if mouse_clicked:
                pygame.quit()  # 退出游戏
                print("Game exited")
                sys.exit()
        else:
            pygame.draw.rect(self.screen, self.quit_button_color, self.quit_button_rect)
        quit_text_surf = self.font.render('Quit', True, (255, 255, 255))
        quit_text_rect = quit_text_surf.get_rect(center=self.quit_button_rect.center)
        self.screen.blit(quit_text_surf, quit_text_rect)
