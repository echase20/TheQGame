from abc import ABC
from copy import deepcopy
from typing import List, Dict, Tuple, Optional

from Q.Common.map import Map
from Q.Common.Board.pos import Pos
from Q.Common.Board.tile import Tile
from Q.Common.rulebook import Rulebook
from Q.Player.dag import Dag
from Q.Player.player import Player
from Q.Player.turn import Turn
from Q.Player.turn_outcome import TurnOutcome

from Q.Player.strategy import PlayerStrategy
from Q.Player.public_player_data import PublicPlayerData


class InHousePlayer(Player, ABC):
    """
    # represents a Player of a game
    """

    def __init__(self, name, strategy: PlayerStrategy = Dag(), hand: List[Tile] = [], rulebook: Rulebook = Rulebook()):
        """
        # initializes a player with a given name, strategy and hand for the Q Game
        """
        super().__init__(name=name, strategy=strategy, hand=hand,rulebook=rulebook)

    def newTiles(self, st: List[Tile]):
        super().newTiles(st)

    def setup(self, given_map: Map, tiles: List[Tile]):
        super().setup(given_map, tiles)

    def win(self, w: bool):
        super().win(w)

    def take_turn(self, s: PublicPlayerData) -> Turn:
        """
        takes a turn for a player
        :param s: the public state
        :return: the turn the player does
        """
        return self.get_tile_placement_choices(s)

