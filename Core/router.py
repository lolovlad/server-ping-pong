from Model.Robot import Robot
from Model.DataBase import DataBase
from socket import *
from threading import Thread
from Core.Network import NetWork

sock = socket()
sock.bind(('192.168.0.104', 2510))
sock.listen(6)


def client_core(socket_client):
    network_core = NetWork(socket_client)
    reg_message = network_core.listener()
    if reg_message["Type_Command"] is not None:
        robot_model = Robot(reg_message["Type_Robot"], reg_message["State"], reg_message["District"], network_core)
        DataBase().attach(robot_model)
    else:
        return
    print(DataBase().get_observer())
    while True:
        command = robot_model.network_core.listener()
        if command is not None:
            DataBase().add_list_command(command)
        else:
            break


while True:
    print('connection...')
    client, mass = sock.accept()
    print(mass, 'connect')
    Thread(target=client_core, args=(client,), daemon=True).start()
