import json
import socketserver
import sys
import threading
from threading import Timer

from Q.Server.server_callback import ServerCallbacks
from Q.Server.states import States

ServerAddress = ("127.0.0.1", 8000)
names = {}
callback = ServerCallbacks()

class MyTCPClientHandler(socketserver.StreamRequestHandler):
    def write_method(self, func, args):
        data = json.dumps([func, args])
        self.wfile.write(data.encode())

    def should_start_game(self):
        if self.state == States.RUNGAME:
            return False
        if len(self.client_address) == 2:
            return True

    def handle(self):
        self.state = States.SIGNUP
        while True:
            print("hello")
            msg = self.rfile.readline().strip()
            print(msg, '= received message')
            if self.state == States.SIGNUP and msg not in names.keys():
                names[msg.decode()] = self

def check_players(should_close: bool):
    if len(names) >= 2:
        callback.start_game(names)
    elif should_close:
        sys.exit()

def should_start_game():
    t1 = Timer(20, check_players, args=None, kwargs=None)
    t1.start()

    t2 = Timer(40, check_players, args=[True], kwargs=None)
    t2.start()
    while True:
        if len(names) == 4:
            callback.start_game(names)


if __name__ == "__main__":
    t = threading.Thread(target=should_start_game)
    TCPServerInstance = socketserver.ThreadingTCPServer(ServerAddress, MyTCPClientHandler)
    t.start()
    TCPServerInstance.serve_forever()

