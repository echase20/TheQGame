import json
import socketserver
from typing import Any

from Q.Referee.referee_config import RefereeConfig
from Q.Server.server import MyTCPClientHandler
from Q.Server.states import States
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

class MyTCPClientHandlerConfig(MyTCPClientHandler):
    def __init__(self, request: Any, client_address: Any, server: socketserver.BaseServer, port: int,
                 waiting_rounds: int, period_length: int, wait_for_name_length: int, referee: RefereeConfig):
        self.server_address = ("127.0.0.1",port)
        self.waiting_rounds = waiting_rounds
        self.period_length = period_length
        self.wait_for_name_length = wait_for_name_length
        self.referee = referee
        super().__init__(request, client_address, server)

    def check_for_name(self):
        super().check_for_name()

    def get_latest_message(self):
        return super().get_latest_message()

    def write_method(self, func, args):
        super().write_method(func,args)

    def handle(self):
        super().handle()

if __name__ == "__main__":
    TCPServerInstance = socketserver.ThreadingTCPServer(ServerAddress, MyTCPClientHandler)
    t1.start()
    t2.start()
    t3.start()
    TCPServerInstance.serve_forever()
