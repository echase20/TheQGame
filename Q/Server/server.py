import json
import socketserver
import threading
from threading import Timer
from typing import Any, Callable, Tuple, Dict

from Q.Referee.ref_with_config import RefereeWithConfig
from Q.Referee.referee_config import RefereeConfig
from Q.Server.player import ProxyPlayer
from Q.Server.server_config import ServerConfig
from Q.Server.states import States


class Server(socketserver.ThreadingTCPServer):
    def __init__(self, server_config: ServerConfig, server_address: Tuple[str, int],
                 RequestHandlerClass: Callable[..., socketserver.BaseRequestHandler]):
        super().__init__(server_address, RequestHandlerClass)
        self.__slots__ = "names, server_config"
        self.daemon_threads = True
        self.server_config = server_config
        self.names = {}
        self.server_tries = self.server_config.server_tries
        self.t = Timer(self.server_config.server_wait, self.check_players)
        self.t.daemon = True
        self.t3 = threading.Thread(target=self.should_start_game)
        self.t3.daemon = True
        self.t.start()
        self.t3.start()

    def start_game(self, names: Dict, ref_config: RefereeConfig):
        self.t.cancel()
        ref = RefereeWithConfig(ref_config)
        player_list = [ProxyPlayer(name, conn) for name, conn in names.items()]
        if not ref_config.quiet:
            print(player_list)
        res = ref.main(player_list)
        print(json.dumps(res))
        self.shutdown()
        self.server_close()

    def check_players(self):
        if len(self.names) >= 2:
            self.start_game(self.names, self.server_config.ref_spec)
            return
        self.timer()

    def should_start_game(self):
        while True:
            if len(self.names) == 4:
                if not self.server_config:
                    print("Starting game with four players")
                self.start_game(self.names, self.server_config.ref_spec)

    def timer(self):
        self.server_tries -= 1
        if self.server_tries == 0:
            self.t.start()
        end_result = json.dumps([[], []])
        print(end_result)


class Connection(socketserver.StreamRequestHandler):
    def __init__(self, request: Any, client_address: Any, server: socketserver.BaseServer):
        self.latest = ""
        self.state = States.SIGNUP
        self.server = server
        self.quiet = self.server.server_config.quiet
        self.check_for_name_thread = Timer(self.server.server_config.server_wait, self.check_for_name)
        super().__init__(request, client_address, server)

    def check_for_name(self):
        if self.state == States.SIGNUP:
            self.state = States.NO_NAME_GIVEN

    def get_latest_message(self):
        new = self.latest
        if new:
            self.latest = ""
        return new

    def write_method(self, func, args):
        data = json.dumps([func, args])
        if not self.quiet:
            print(data, "writing")
        self.wfile.write(data.encode())

    def handle(self):
        while True:
            msg = self.rfile.readline().strip().decode()
            if msg and self.state == States.SIGNUP and msg not in self.server.names.keys():
                if not self.quiet:
                    print("CONNECTION MADE")
                self.server.names[msg] = self
                self.state = States.RUNGAME
                continue

            if msg and self.state == States.RUNGAME:
                self.latest = msg
                if not self.quiet:
                    print(msg, "received")
