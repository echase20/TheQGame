import threading
import time
from json import dumps
from typing import List, Optional

from twisted.internet import defer

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

    def listen(self):
        t = time.time()
        while time.time() - t < 6:
            #jrep = self.s.see_if_received()
            #if rep: return rep
            pass

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
        response = self.s.see_if_received(d)
        if response:
            print(response)
            raise Exception("no void return")

    def take_turn(self, s: PlayerState) -> Turn:
        """
        takes a turn for a player
        :param s: the public state
        :return: the turn the player does
        """
        jpub = Util().convert_player_state_to_jpub(s)
        test = self.s.send(PlayerFuncs.TAKE_TURN, [jpub])
        response = self.listen()
        if response != "void":
            raise Exception("no void return")

        print(test)
        return test

    def win(self, w: bool) -> None:
        """
        From specs: the player is informed whether it won or not
        :param w: boolean value to be used to inform the player whether they won
        """
        self.s.send(PlayerFuncs.WIN, [w])
        response = self.listen()
        if response != "void":
            raise Exception("no void return")

    def newTiles(self, st: List[Tile]):
        """
        From specs: The player is handed a new set of tiles
        :param st: set of tiles to be handed to the player
        """
        tiles = Util().convert_tiles_to_jtiles(st)
        self.s.send(PlayerFuncs.SETUP, [tiles])
        response = self.listen()
        if response != "void":
            raise Exception("no void return")
