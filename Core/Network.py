from socket import *
from json import *
from Model.DataBase import DataBase


class NetWork:
    def __init__(self, sock):
        self.__socket_main = sock
        self.send_message({"Type_command": "Server", "Information": "LogIn"})

    def listener(self):
        try:
            message = self.__socket_main.recv(1024).decode()
            js_convert_message = loads(message)
            return js_convert_message
        except ConnectionResetError:
            model = list(filter(lambda x: x.network_core.get_socket().getsockname() == self.__socket_main.getsockname(),
                                DataBase().get_observer()))
            DataBase().detach(model[0])
            return None

    def send_message(self, message):
        message = dumps(message)
        self.__socket_main.send(message.encode())

    def close(self):
        self.__socket_main.close()

    def get_socket(self):
        return self.__socket_main
