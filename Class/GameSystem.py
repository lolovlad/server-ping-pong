import pygame
from pygame.math import Vector2
from Class.Interfase.ISolid import Solide
from Class.Paddle import Paddle
from Class.Ball import Ball
from Class.Map import Map
from Class.EventSystem import EventSystem
from Class.Display import Display
from Model.DataBase import DataBase
import random


class GameSystem:
    def __init__(self, database):
        self.__player = {}
        self.__ball = None
        self.__event_system = None
        self.__display = None
        self.__main_display = None
        self.__paddle_left = None
        self.__ball = None
        self.__map = None
        self.__database = database
        self.__main_sprites = pygame.sprite.RenderPlain()

    def game_init(self):
        self.__main_display = pygame.display.set_mode((self.__database.WINDOW_WIDTH,
                                                       self.__database.WINDOW_HEIGHT + self.__database.DISPLAY_HEIGHT),
                                                      0, 32)

        self.__database.set_position_paddles((self.__main_display.get_rect().left + 50,
                                              self.__main_display.get_rect().centery - self.__database.DISPLAY_HEIGHT),
                                             (0, 0))

        self.__database.set_position_ball((self.__main_display.get_rect().centerx,
                                           self.__main_display.get_rect().centery - self.__database.DISPLAY_HEIGHT))

        self.__paddle_left = Paddle(self.__database.get_position_paddles()[0], [10, 100],
                                    self.__database.WHITE, 4, 4, 13, 1)
        self.__ball = Ball(self.__database.get_position_ball(), [10, 10], self.__database.WHITE,
                           5, 2, 8, (random.uniform(-0.5, 0.5), random.uniform(-0.2, 0.2)))
        self.__map = Map(self.__database.RED, self.__database.border_position, self.__database.border_size,
                         self.__database.BUR, self.__database.energy_position, self.__database.energy_size)

        self.__event_system = EventSystem({"paddle": self.__paddle_left, "ball": self.__ball, "map": self.__map}, self,
                                          self.__database)
        self.__display = Display(self.__database.WINDOW_HEIGHT + self.__database.DISPLAY_HEIGHT,
                                 self.__database.WINDOW_WIDTH, self.__database.WHITE, self.__database.BLACK,
                                 self.__main_display, self.__database)

        self.__main_sprites.add(*self.__map.get_borders_render())
        self.__main_sprites.add(*self.__map.get_energy_render())
        self.__main_sprites.add(self.__paddle_left, self.__ball)

    def update_game(self):
        self.__main_display.fill((0, 0, 0))
        self.__event_system.update()
        self.__display.render_score_bord()
        self.__main_sprites.draw(self.__main_display)

    def restart(self):
        self.__paddle_left.energy = 33
        self.__paddle_left.position = self.__database.get_position_paddles()[0]
        self.__paddle_left.direction = (0, 0)
        self.__paddle_left.is_power_hit = False
        self.__ball.position = self.__database.get_position_ball()
        self.__ball.direction = Vector2((random.uniform(-0.5, 0.5), random.uniform(-0.2, 0.2)))

    def game_over(self, i=0):
        DataBase().is_playing = False
        self.__main_display.fill(self.__database.BLACK)
        self.__display.render_score_bord(i, ((self.__database.WINDOW_HEIGHT + self.__database.DISPLAY_HEIGHT) // 2,
                                             self.__database.WINDOW_WIDTH // 2))
        pygame.display.update()
