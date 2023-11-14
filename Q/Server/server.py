from json import dumps
from typing import List

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

from Q.Player.player_funcs import PlayerFuncs

class Server():
    def __init__(self, port: int):
        self.setup(port)


    def setup(self, port: int):
        factory = protocol.ServerFactory()
        factory.protocol = Echo
        reactor.listenTCP(port, factory)
        reactor.run()

    def send(self, player_func: PlayerFuncs, args):
        tcp_message = dumps([player_func, args])



        pass



class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        self.transport.write(data)
