import sys

from Q.Client.client import Client
from Q.Client.referee import ProxyRef
from Q.Player.in_housep_player import InHousePlayer

HOST = 'localhost'
PORT = 8001
if __name__ == "__main__":
    name = input()
    player = InHousePlayer(name)
    c = Client(name, HOST, PORT)
    ProxyRef(c, player)
