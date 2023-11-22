from typing import Dict

from Q.Referee.referee import Referee
from Q.Server.callback import Callback
from Q.Server.player import ProxyPlayer


class ServerCallbacks(Callback):
    def start_game(self, names: Dict):
        ref = Referee()
        player_list = [ProxyPlayer(name, conn) for name, conn in names.items()]
        print(ref.main(player_list))
