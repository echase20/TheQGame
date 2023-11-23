import json
import time
from typing import List


from Q.Common.Board.tile import Tile
from Q.Player.player import Player
from Q.Player.player_funcs import PlayerFuncs
from Q.Player.player_state import PlayerState
from Q.Player.turn import Turn
from Q.Util.util import Util


class ProxyPlayer(Player):
    def __init__(self, name: str, s):
        super().__init__(name)
        self._name = name
        self.s = s

    def listen(self):
        sent_time = time.time()
        while time.time() - sent_time < 6:
            msg = self.s.get_latest_message()
            if msg:
                return msg
        return None

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

        self.s.write_method(PlayerFuncs.SETUP.value, [jstate, jtiles])
        response = self.listen()
        if response != "void":
            raise Exception("no void return")

    def take_turn(self, s: PlayerState) -> Turn:
        """
        takes a turn for a player
        :param s: the public state
        :return: the turn the player does
        """
        jpub = Util().convert_player_state_to_jpub(s)
        self.s.write_method(PlayerFuncs.TAKE_TURN.value, [jpub])
        msg = self.listen()
        if msg:
            print("LMAO")
            try:
                print(msg)
                data = json.loads(msg)
                return Util().convert_jaction_to_turn(data)
            except Exception as e:
                print(e)
        else:
            raise Exception("Reply message was not valid")

    def win(self, w: bool) -> None:
        """
        From specs: the player is informed whether it won or not
        :param w: boolean value to be used to inform the player whether they won
        """
        self.s.write_method(PlayerFuncs.WIN.value, [w])
        response = self.listen()
        if response != "void":
            raise Exception("no void return")

    def newTiles(self, st: List[Tile]):
        """
        From specs: The player is handed a new set of tiles
        :param st: set of tiles to be handed to the player
        """
        tiles = Util().convert_tiles_to_jtiles(st)
        self.s.write_method(PlayerFuncs.NEW_TILES.value, tiles)
        response = self.listen()
        if response != "void":
            raise Exception("no void return")
