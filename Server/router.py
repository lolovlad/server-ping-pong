import Server.Handler.Handler as Work #вызов команды task(name_command)
import Server.Listing as l
from socket import *
from threading import Thread
import json as js
import sys

sock = socket()
sock.bind(('192.168.0.104', 2510))
sock.listen(6)

listing = l.Lists()

def client(sock):
    while True:
        req = sock.recv(1024).decode()
        data = js.loads(req)
        data["sock"] = sock
        dat = Work.task(data)
        print(dat)
        sys.stdout.write("\r list_robot: {0}, list_sort: {1}, qr_flag: {2}, angle: {3}".format(listing.task_list_robot, listing.task_list_sort, listing.list_qr_flag, listing.list_cal))

while True:
    print('connection...')
    client1, mass = sock.accept()
    print(mass, 'connect')
    Thread(target=client, args=(client1,), daemon=True).start()
    #print(listing.list_qr_flag)
    #print(listing.task_list_sort)
    #print(listing.task_list_robot)
