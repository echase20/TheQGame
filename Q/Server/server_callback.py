import json
from typing import Dict

from Q.Referee.ref_with_config import RefereeWithConfig
from Q.Referee.referee import Referee
from Q.Referee.referee_config import RefereeConfig
from Q.Server.player import ProxyPlayer
from Q.Util.util import Util


class ServerCallbacks():
    def start_game(self, names: Dict, ref_config: RefereeConfig):
        ref = RefereeWithConfig(ref_config)
        player_list = [ProxyPlayer(name, conn) for name, conn in names.items()]
        if not ref_config.quiet:
            print(player_list)
        res = ref.main(player_list)

        print(json.dumps(res))
