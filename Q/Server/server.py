import json
import socketserver
import sys
import threading
from threading import Timer
from typing import Any

from Q.Server.server_callback import ServerCallbacks

ServerAddress = ("127.0.0.1", 8001)
names = {}
callback = ServerCallbacks()

def check_players(should_close: bool):
    if len(names) >= 2:
        callback.start_game(names)
        t1.cancel()
        t2.cancel()
        sys.exit()
    elif should_close:
        end_result = json.dumps([[],[]])
        print(end_result)
        t1.cancel()
        t2.cancel()
        t3.join()

def should_start_game():
    while True:
        if len(names) == 4:
            callback.start_game(names)
            t1.cancel()
            t2.cancel()
            sys.exit()

t1 = Timer(20, check_players, args=[False], kwargs=None)
t2 = Timer(40, check_players, args=[True], kwargs=None)
t3 = threading.Thread(target=should_start_game)


class MyTCPClientHandler(socketserver.StreamRequestHandler):
    def __init__(self, request: Any, client_address: Any, server: socketserver.BaseServer):
        self.latest = ""
        self.first_message = True
        super().__init__(request, client_address, server)

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

            if msg and self.first_message and msg not in names.keys():
                names[msg] = self
                self.first_message = False
                continue
            if msg and not self.first_message:
                self.latest = msg


if __name__ == "__main__":
    TCPServerInstance = socketserver.ThreadingTCPServer(ServerAddress, MyTCPClientHandler)
    t1.start()
    t2.start()
    t3.start()
    TCPServerInstance.serve_forever()

