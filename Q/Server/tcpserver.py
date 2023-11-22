import json
import socketserver
import threading
from threading import Timer

from Q.Server.server_callback import ServerCallbacks
from Q.Server.states import States

ServerAddress = ("127.0.0.1", 8000)
names = {}
callback = ServerCallbacks()

def check_players(should_close: bool):
    if len(names) >= 2:
        callback.start_game(names)
        t1.cancel()
        t2.cancel()
    elif should_close:
        t1.cancel()
        t2.cancel()
        t3.join()

def should_start_game():
    while True:
        if len(names) == 1:
            callback.start_game(names)
            t1.cancel()
            t2.cancel()

t1 = Timer(20, check_players, args=[False], kwargs=None)
t2 = Timer(40, check_players, args=[True], kwargs=None)
t3 = threading.Thread(target=should_start_game)


class MyTCPClientHandler(socketserver.StreamRequestHandler):
    def write_method(self, func, args):
        data = json.dumps([func, args])
        self.wfile.write(data.encode())

    def handle(self):
        self.state = States.SIGNUP
        while True:
            msg = self.rfile.readline().strip()
            print(msg, '= received message')
            if self.state == States.SIGNUP and msg not in names.keys():
                names[msg.decode()] = self

if __name__ == "__main__":
    TCPServerInstance = socketserver.ThreadingTCPServer(ServerAddress, MyTCPClientHandler)
    t1.start()
    t2.start()
    t3.start()
    TCPServerInstance.serve_forever()

