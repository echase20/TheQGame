import threading
import time
from collections import defaultdict
from json import dumps

import failure as failure
from twisted.internet import reactor, defer, task
from twisted.internet.protocol import connectionDone, Protocol, Factory

from Q.Player.player_funcs import PlayerFuncs
from Q.Server.states import States


class Connection(Protocol):

    def __init__(self):
        self.name = ""
        self.state = States.SIGNUP
        self.last_received_turn = None
        self.datas = defaultdict()
        self.id_count = 0

    def connectionMade(self):
        text = "What's your name".encode("utf-8")
        self.transport.write(text)
        reactor.callLater(5, self.wait)

    def wait(self):
        if not self.name:
            self.transport.abortConnection()
            print("client took too long")

    def dataReceived(self, data: bytes):
        if self.state == States.SIGNUP:
            self.name = data.decode("utf-8")
            self.factory.users[self.name] = self
            self.state = States.RUNGAME
        elif self.state == States.RUNGAME:
            reply = data.decode()
            self.datas[self.id_count] = reply

    def see_if_received(self,d):
        self.d = d
        self.s = task.LoopingCall(self.say_hi)
        self.s.start(0.1)
        return self.s



    def say_hi(self):
        if self.datas.get(self.id_count) not None:
            self.s.stop()
            self.d.callback(self.datas.get(self.id_count))

    def connectionLost(self, reason: failure.Failure = connectionDone) -> None:
        print()

    def send(self, player_func: PlayerFuncs, args):
        tcp_message = dumps([player_func.value, args]).encode("utf-8")
        print(tcp_message)
        self.transport.write(tcp_message)




