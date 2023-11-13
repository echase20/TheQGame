from typing import List

from Q.Common.Board.tile import Tile
from Q.Common.game_state import GameState
from Q.Player.player import Player
from Q.Player.player_state import PlayerState
from Q.Player.turn import Turn
from Q.Server.server import Server
from Q.Util.util import Util


class ProxyPlayer(Player):
    def __init__(self, name: str, s: Server):
        super().__init__(name)
        self.name = name
        self.s = s
    def name(self) -> str:
        """
        Returns the player's name
        """
        return self._name

    def setup(self, state: PlayerState, tiles: List[Tile]):
        """
        Sets up the game by giving the player their tiles. We do not need to use the given_map but are keeping the
        parameter as this is a public API.
        """
        jstate = Util().convert_ppd_to_jpub(state)
        jtiles = Util().convert_tiles_to_jtiles(tiles)
        self.s.send(jstate, jtiles)

    def take_turn(self, s: PlayerState) -> Turn:
        """
        takes a turn for a player
        :param s: the public state
        :return: the turn the player does
        """
        jpub = Util().conver
        return self.get_tile_placement_choices(s)

    def win(self, w: bool) -> None:
        """
        From specs: the player is informed whether it won or not
        :param w: boolean value to be used to inform the player whether they won
        """
        pass

    def newTiles(self, st: List[Tile]):
        """
        From specs: The player is handed a new set of tiles
        :param st: set of tiles to be handed to the player
        """
        self.hand = st