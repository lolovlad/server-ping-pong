import pygame
import time
from Class.GameSystem import GameSystem
from Model.DataBaseGame import DataBaseGame
from Class.Interfase.IObserver import Observer
from threading import Thread


def game_start(player_1, player_2, id_game):
    pygame.init()

    clock = pygame.time.Clock()
    database = DataBaseGame()
    game_system = GameSystem(database, player_1, player_2)
    game_system.game_init()

    while database.is_playing:
        game_system.update_game()

    while True:
        clock.tick(60)
        game_system.game_over()


class GameCreator(Observer):
    def __init__(self):
        self.network = None
        self.id_game = 0

    def update(self, subject):
        if type(subject) == list:
            new_player = subject[1:]
            print(new_player, "eee")
            new_player = sorted(new_player, key=lambda x: x.mmr and x.state == "search")
            if len(new_player) > 1:
                new_player[0].state = "in_game"
                new_player[1].state = "in_game"
                new_player[0].network.send_message({"Type_message": "Server", "Type_command": "Started_game",
                                                    "Side": "left"})
                new_player[1].network.send_message({"Type_message": "Server", "Type_command": "Started_game",
                                                    "Side": "right"})
                Thread(target=game_start, args=(new_player[0], new_player[1], self.id_game), daemon=True).start()
                self.id_game += 1
