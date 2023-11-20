import asyncio
import threading
import time
from json import dumps

import failure as failure
from twisted.internet.protocol import connectionDone, Protocol, Factory
from twisted.internet import reactor, protocol

from Q.Player.player_funcs import PlayerFuncs
from multiprocessing.pool import ThreadPool


# Pycharm has trouble reading Twisted methods
from Q.Referee.referee import Referee
from Q.Server.states import States


class Connection(Protocol):

    def __init__(self, users, ref):
        self.name = ""
        self.users = users
        self.ref = ref
        self.state = States.SIGNUP
        self.last_received_turn = None

    def connectionMade(self):
        text = "What's your name".encode("utf-8")
        self.transport.write(text)
        t = threading.Timer(3.0, self.wait)
        t.start()

    def wait(self):
        if not self.name:
            self.transport.abortConnection()
            print("client took too long")

    def dataReceived(self, data: bytes):
        if self.state == States.SIGNUP:
            name = data.decode("utf-8")
            self.users[name] = self
            self.name = name
            print(self.name + " signed up!")
            text = (self.name + " signed up!").encode("utf-8")
            self.transport.write(text)
        if self.state == States.RUNGAME:
            if data.decode("utf-8") == "void":
                pass
            self.last_received_turn = data.decode("utf-8")

    def connectionLost(self, reason: failure.Failure = connectionDone) -> None:
        if self.name in self.users:
            self.users.remove(self.name)

    def send(self, player_func: PlayerFuncs, args):
        tcp_message = dumps([player_func, args])
        self.transport.write(tcp_message.encode())

    def turn_updated(self):
        return self.last_received_turn != None

    def update_last_recv_turn(self):
        self.last_received_turn = None

    def recv(self):
        return self.last_received_turn
    """
    def recv_data(self):
        p = threading.Thread(target=self.recv_data2)
        p.daemon = True
        p.start()

    def recv_data2(self):
        while len(self.queue):
            return self.queue.pop()
    """


class ServerFactory(Factory):

    def __init__(self):
        self.users = {}
        self.game_start = False
        self.run_again = True
        self.wait_for_connections()
       # while not self.game_start and len(self.users) != 4:
        #    pass


    def buildProtocol(self, addr):
        return Connection(self.users, self.ref)

    def wait_for_connections(self):
        t = threading.Timer(20.0, self.check_for_connections)
        t.start()


    def check_for_connections(self):
        if len(self.users) < 2:
            self.game_start = False
        else:
            self.game_start = True
            return
        if self.run_again and self.game_start == False:
            self.run_again = False
            self.wait_for_connections()

def main():
    """
    p = threading.Thread(target=self.write, args=(player_func, args))
    p.daemon = True
    p.start()
    """
    port = 8000
    reactor.listenTCP(port, ServerFactory())
    reactor.run()

if __name__ == '__main__':
    main()