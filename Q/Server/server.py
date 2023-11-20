import threading
from json import dumps

import failure as failure
from twisted.internet.protocol import connectionDone, Protocol, Factory

from Q.Player.player_funcs import PlayerFuncs
from Q.Server.states import States


class Connection(Protocol):

    def __init__(self, users):
        self.name = ""
        self.users = users
        self.state = States.SIGNUP
        self.last_received_turn = None

    def connectionMade(self):
        text = "What's your name".encode("utf-8")
        self.transport.write(text)
        t = threading.Timer(5.0, self.wait)
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
            self.state = States.RUNGAME
        elif self.state == States.RUNGAME:
            if data.decode("utf-8") == "void":
                pass
            print("DATA WE RECIEVE")
            print(data.decode())
            self.last_received_turn = data.decode("utf-8")

    def connectionLost(self, reason: failure.Failure = connectionDone) -> None:
        if self.name in self.users:
            self.users.remove(self.name)

    def send(self, player_func: PlayerFuncs, args):
        tcp_message = dumps([player_func.value, args]).encode("utf-8")
        print(tcp_message)
        self.transport.write(tcp_message)

    def turn_updated(self):
        return self.last_received_turn is not None

    def update_last_recv_turn(self):
        self.last_received_turn = None

    def recv(self):
        return self.last_received_turn



