import pygame
from pygame.math import Vector2
from Class.Interfase.ISolid import Solide
from Class.Paddle import Paddle
from Class.Ball import Ball
from Class.Map import Map
from Class.EventSystem import EventSystem
from Model.DataBase import DataBase
import random


class GameSystem:
    def __init__(self, database, player_1, player_2):
        self.__player = {}
        self.__ball = None
        self.__event_system = None
        self.__main_display = None
        self.__paddle_left = None
        self.__paddle_right = None
        self.__ball = None
        self.__map = None
        self.__database = database
        self.__main_sprites = pygame.sprite.RenderPlain()

        self.__player_1 = player_1
        self.__player_2 = player_2

    def game_init(self):
        self.__main_display = pygame.display.set_mode((self.__database.WINDOW_WIDTH,
                                                       self.__database.WINDOW_HEIGHT + self.__database.DISPLAY_HEIGHT),
                                                      0, 32)

        self.__database.set_position_ball((self.__main_display.get_rect().centerx,
                                           self.__main_display.get_rect().centery - self.__database.DISPLAY_HEIGHT))

        self.__paddle_left = Paddle(self.__database.get_position_paddles()[0], [10, 100],
                                    self.__database.WHITE, 4, 4, 13, 1, (1, 0))

        self.__paddle_right = Paddle(self.__database.get_position_paddles()[1], [10, 100],
                                     self.__database.WHITE, 4, 4, 13, 2, (-1, 0))

        self.__ball = Ball(self.__database.get_position_ball(), [10, 10], self.__database.WHITE,
                           5, 2, 8, (random.uniform(-0.5, 0.5), random.uniform(-0.2, 0.2)))
        self.__map = Map(self.__database.RED, self.__database.border_position, self.__database.border_size,
                         self.__database.BUR, self.__database.energy_position, self.__database.energy_size)

        self.__event_system = EventSystem({"paddle": {"left": [self.__player_1, self.__paddle_left],
                                                      "right": [self.__player_2, self.__paddle_right]},
                                           "ball": self.__ball, "map": self.__map}, self,
                                          self.__database)

    def update_game(self):
        self.__event_system.update()

    def restart(self):
        self.__paddle_left.energy = 33
        self.__paddle_left.position = self.__database.get_position_paddles()[0]
        self.__paddle_left.direction = (0, 0)
        self.__paddle_left.is_power_hit = False
        self.__paddle_right.energy = 33
        self.__paddle_right.position = self.__database.get_position_paddles()[1]
        self.__paddle_right.direction = (0, 0)
        self.__paddle_right.is_power_hit = False
        self.__ball.position = self.__database.get_position_ball()
        self.__ball.direction = Vector2((random.uniform(-0.5, 0.5), random.uniform(-0.2, 0.2)))

    def game_over(self, player_winner):
        self.__database.is_playing = False
        if player_winner == 1:
            player_winner = self.__player_1.get_name()
        else:
            player_winner = self.__player_2.get_name()

        message = {
            "Type_message": "Server",
            "Type_command": "Game_over",
            "Win": player_winner
        }

        self.__player_1.network.send_message(message)
        self.__player_2.network.send_message(message)
        self.__player_1.state = "main_menu"
        self.__player_2.state = "main_menu"
