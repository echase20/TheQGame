import json
from typing import Dict

from Q.Referee.referee import Referee
from Q.Server.player import ProxyPlayer
from Q.Util.util import Util


class ServerCallbacks():
    def start_game(self, names: Dict):
        ref = Referee()
        player_list = [ProxyPlayer(name, conn) for name, conn in names.items()]
        res = ref.main(player_list)
        print(json.dumps(Util().pair_results_to_jresults(res)))
