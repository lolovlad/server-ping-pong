from Core.GameСreator import GameCreator
from Model.Player import Player
from Model.DataBase import DataBase
from socket import *
from threading import Thread
from Core.Network import NetWork

sock = socket()
sock.bind(('192.168.0.108', 2510))
sock.listen(6)

DataBase().attach(GameCreator())


def client_core(socket_client):
    network_core = NetWork(socket_client)
    reg_message = network_core.listener()
    if reg_message["Type_Command"] is not None:
        user = Player(reg_message["Name_user"], reg_message["Ip_user"],  reg_message["Mmr_user"], network_core)
        DataBase().attach(user)
    else:
        return
    while True:
        command = user.network.listener()
        if command is not None:
            DataBase().add_list_command(command)
        else:
            break


while True:
    print('connection...')
    client, mass = sock.accept()
    print(mass, 'connect')
    Thread(target=client_core, args=(client,), daemon=True).start()
