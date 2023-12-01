from typing import List

from Q.Common.Board.tile import Tile
from Q.Common.game_state import GameState
from Q.Common.map import Map
from Q.Common.player_game_state import PlayerGameState
from Q.Common.rulebook import Rulebook
from Q.Player.in_housep_player import InHousePlayer
from Q.Player.player import Player
from Q.Player.turn import Turn
from Q.Referee.observer import Observer
from Q.Referee.referee import Referee
from Q.Referee.referee_config import RefereeConfig


class RefereeWithConfig(Referee):
    def __init__(self, referee_config: RefereeConfig):
        self.referee_config = referee_config

        observer = Observer() if self.referee_config.observe else None
        super().__init__(observer)

    def main(self, player_list: List[Player]) -> List[List[str]]:
        return self.start_from_state(player_list, self.referee_config.state0)



