import threading
import time
from json import dumps

import failure as failure
from twisted.internet.protocol import connectionDone, Protocol, Factory
from twisted.internet import reactor, protocol

from Q.Player.player_funcs import PlayerFuncs
from multiprocessing.pool import ThreadPool


# Pycharm has trouble reading Twisted methods
from Q.Server.states import States


class Server(Protocol):

    def __init__(self, users):
        self.name = ""
        self.users = users
        self.state = States.SIGNUP
        self.last_received_turn = None

    def dataReceived(self, data: bytes):
        if self.state == States.SIGNUP:
            name = data.decode()
            self.users.append(name)
            self.name = name
        if self.state == States.RUNGAME:
            pass
    def connectionLost(self, reason: failure.Failure = connectionDone) -> None:
            self.users.remove(self.name)
    def get_last_received_turn(self):
        return self.last_received_turn

    def connectionMade(self):
        text = "What's your name".encode()
        self.transport.write(text)

    def recv_data(self):
        p = threading.Thread(target=self.recv_data2)
        p.daemon = True
        p.start()

    def recv_data2(self):
        while len(self.queue):
            return self.queue.pop()

    def send(self, player_func: PlayerFuncs, args):

    def write(self, player_func, args):

def send():
    tcp_message = dumps([player_func, args])
    self.transport.write(tcp_message.encode())

    t_end = time.time() + 20
    while time.time() < t_end:
        time.sleep(1)
        if len(self.queue):
            return self.queue.pop()
    return None


class ChatFactory(Factory):

    def __init__(self):
        self.users [str] = []

    def buildProtocol(self, addr):
        return Server(self.users)

def main():
    p = threading.Thread(target=self.write, args=(player_func, args))
    p.daemon = True
    p.start()
    port = 4563
    factory = ChatFactory()
    reactor.listenTCP(port, ChatFactory())
    reactor.run()