import asyncio
import json
import threading
import time
from json import dumps

from twisted.internet.protocol import connectionDone, Protocol, Factory
from twisted.internet import reactor, protocol


from Q.Referee.referee import Referee
from Q.Server.player import ProxyPlayer
from Q.Server.server import Connection


class ServerFactory(Factory):
    def __init__(self):
        self.users = {}
        self.timed_out = False
        self.run_signup_period_again = True
        self.wait_for_connections()

        t = threading.Thread(target=self.wait_for_players)
        t.start()

    def wait_for_players(self):
        while not self.timed_out:
            if len(self.users) == 1:
                self.timed_out = True
                self.start_game()
                break
        if self.timed_out:
            print(json.dumps([[], []]))

    def start_game(self):
        player_list = []
        for name, connection in self.users.items():
            print(name)
            print(connection)
            player_list.append(ProxyPlayer(name, connection))

        print(player_list)
        res = Referee().main(player_list)
        print(res)

    def buildProtocol(self, addr):
        print("HERE")
        return Connection(self.users)

    def wait_for_connections(self):
        t = threading.Timer(20.0, self.check_for_connections)
        t.start()

    def check_for_connections(self):
        if len(self.users) > 1 and not self.timed_out:
            self.timed_out = True
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
