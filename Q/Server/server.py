import json
import socketserver
import sys
import threading
from threading import Timer
from typing import Any, Callable, Tuple

from Q.Server.server_callback import ServerCallbacks
from Q.Server.server_config import ServerConfig
from Q.Server.states import States



class Server(socketserver.ThreadingTCPServer):
    def __init__(self, server_config: ServerConfig, server_address: Tuple[str, int],
                 RequestHandlerClass: Callable[..., socketserver.BaseRequestHandler]):
        super().__init__(server_address, RequestHandlerClass)
        self.__slots__ = "names, server_config"

        self.server_config = server_config
        self.callback = ServerCallbacks()
        self.check_counter = 0
        self.names = {}
        self.t = Timer(self.server_config.server_wait, self.check_players, args=[False], kwargs=None)
        self.t3 = threading.Thread(target=self.should_start_game)
        self.t.start()
        self.t3.start()

    def check_players(self):
        if len(self.names) >= 2:
            self.callback.start_game(self.names, self.server_config.ref_spec)
            self.t.cancel()
            self.t3.join()
            sys.exit()
        self.timer()

    def should_start_game(self):
        while True:
            if len(self.names) == 4:
                if not self.server_config:
                    print("Starting game with four players")
                self.callback.start_game(self.names, self.server_config.ref_spec)
                self.t.cancel()
                sys.exit()

    def timer(self):
        self.check_counter += 1
        if self.check_counter > self.server_config.server_tries:
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
        latest = self.latest
        self.latest = ""
        return latest

    def write_method(self, func, args):
        data = json.dumps([func, args])
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
                    print()
                    print(msg, "MESSAGE SENT OVER")


