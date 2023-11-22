import asyncio
import json
import threading
import time
from json import dumps

from twisted.internet.protocol import connectionDone, Protocol, Factory
from twisted.internet import reactor, protocol, task

from Q.Referee.referee import Referee
from Q.Server.player import ProxyPlayer
from Q.Server.server import Connection


class ServerFactory(Factory):
    protocol = Connection

    def __init__(self):
        self.users = {}
        self.timed_out = False
        self.run_signup_period_again = True

        self.s = task.LoopingCall(self.wait_for_players)
        self.s.start(0.1)
        reactor.callLater(20, self.check_start)
        reactor.callLater(40, self.check_start)
        reactor.callLater(40, self.stop)

    def wait_for_players(self):
        if len(self.users) == 1:
            self.start_game()

    def check_start(self):
        if len(self.users) > 2:
            self.start_game()

    def stop(self):
        if self.s.running:
            self.s.stop()

    def start_game(self):
        self.stop()
        player_list = []
        for name, connection in self.users.items():
            player_list.append(ProxyPlayer(name, connection))

        res = Referee().main(player_list)
        print(res)


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
