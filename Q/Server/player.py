from json import dumps
from typing import List

from Q.Common.Board.tile import Tile
from Q.Player.player import Player
from Q.Player.player_funcs import PlayerFuncs
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
        jstate = dumps(Util().convert_player_state_to_jpub(state))
        jtiles = dumps(Util().convert_tiles_to_jtiles(tiles))
        self.s.send(PlayerFuncs.SETUP, [jstate, jtiles])

    def take_turn(self, s: PlayerState) -> Turn:
        """
        takes a turn for a player
        :param s: the public state
        :return: the turn the player does
        """
        jpub = Util().convert_player_state_to_jpub(s)
        self.s.send(PlayerFuncs.TAKE_TURN, [jpub])
        recv_data = self.s.recvdata()
        return recv_data.convert()

    def win(self, w: bool) -> None:
        """
        From specs: the player is informed whether it won or not
        :param w: boolean value to be used to inform the player whether they won
        """
        self.send(PlayerFuncs.WIN, [w])

    def newTiles(self, st: List[Tile]):
        """
        From specs: The player is handed a new set of tiles
        :param st: set of tiles to be handed to the player
        """
        tiles = Util().convert_tiles_to_jtiles(st)
        self.send(PlayerFuncs.SETUP, [tiles])
