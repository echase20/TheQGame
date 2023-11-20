import threading
import time
from json import dumps
from typing import List, Optional

from Q.Common.Board.tile import Tile
from Q.Player.player import Player
from Q.Player.player_funcs import PlayerFuncs
from Q.Player.player_state import PlayerState
from Q.Player.turn import Turn
from Q.Server.server import Connection
from Q.Util.util import Util


class ProxyPlayer(Player):
    def __init__(self, name: str, s: Connection):
        super().__init__(name)
        self._name = name
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
        jstate = Util().convert_player_state_to_jpub(state)
        jtiles = Util().convert_tiles_to_jtiles(tiles)
        self.s.send(PlayerFuncs.SETUP, [jstate, jtiles])

    def take_turn(self, s: PlayerState) -> Turn:
        """
        takes a turn for a player
        :param s: the public state
        :return: the turn the player does
        """
        jpub = Util().convert_player_state_to_jpub(s)
        self.s.send(PlayerFuncs.TAKE_TURN, [jpub])
        get_turn = False
        started_loop = time.time()
        while started_loop + 6 > time.time() and not get_turn:
            get_turn = self.s.turn_updated()
        turn = self.s.recv()
        self.s.update_last_recv_turn()
        if turn is None:
            raise Exception("There was no turn provided in the allocated amount of time")
        return turn

    def win(self, w: bool) -> None:
        """
        From specs: the player is informed whether it won or not
        :param w: boolean value to be used to inform the player whether they won
        """
        self.s.send(PlayerFuncs.WIN, [w])

    def newTiles(self, st: List[Tile]):
        """
        From specs: The player is handed a new set of tiles
        :param st: set of tiles to be handed to the player
        """
        tiles = Util().convert_tiles_to_jtiles(st)
        self.s.send(PlayerFuncs.SETUP, [tiles])
