import asyncio
import json
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
from Q.Server.player import ProxyPlayer
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
        return self.last_received_turn is not None

    def update_last_recv_turn(self):
        self.last_received_turn = None

    def recv(self):
        return self.last_received_turn


class ServerFactory(Factory):
    def __init__(self):
        self.users = {}
        self.timed_out = False
        self.run_signup_period_again = True
        self.wait_for_connections()
        while not self.timed_out:
            if len(self.users) == 4:
                self.start_game()
                break
        if self.timed_out:
            print(json.dumps([[], []]))

    def start_game(self):
        player_list = []
        for name, connection in self.users:
            player_list.append(ProxyPlayer(name, connection))

        res = Referee().main(player_list)
        print(json.dumps(res))

    def buildProtocol(self, addr):
        return Connection(self.users, self.ref)

    def wait_for_connections(self):
        t = threading.Timer(20.0, self.check_for_connections)
        t.start()

    def check_for_connections(self):
        if len(self.users) > 2:
            self.start_game()
            return

        if len(self.users) < 2 and not self.run_signup_period_again:
            self.timed_out = True
            return

        if self.run_signup_period_again and not self.timed_out:
            self.run_signup_period_again = False
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
