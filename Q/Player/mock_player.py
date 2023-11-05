from typing import List, Dict
from Q.Common.map import Map
from Q.Common.Board.tile import Tile
from Q.Common.rulebook import Rulebook
from Q.Player.dag import Dag
from Q.Player.player import Player
from Q.Player.turn import Turn

from Q.Player.strategy import PlayerStrategy
from Q.Player.public_player_data import PublicPlayerData


class MockPlayer(Player):
    """
    Represents a player that is mocked to have some certain kind of errors
    """
    def __init__(self, name, strategy: PlayerStrategy = Dag(), hand: List[Tile] = [], rulebook: Rulebook = Rulebook(), exn: str = ""):
        """
        # initializes a player with a given name, strategy and hand for the Q Game
        """
        self.exn = exn
        super().__init__(name, strategy, hand, rulebook)

    def win(self, w: bool):
        """
        Raises an exception if called for. Otherwise runs the desired parents win method.
        """
        if self.exn == "win":
            raise Exception("Name method in player errored out")
        return super().win(w)

    def setup(self, given_map: Map, tiles: List[Tile]):
        """
        Raises an exception if called for. Otherwise runs the desired parents setup method.
        """
        if self.exn == "setup":
            raise Exception("Setup method in player errored out")
        super().setup(given_map, tiles)

    def take_turn(self, s: PublicPlayerData) -> Turn:
        """
        Raises an exception if called for. Otherwise runs the desired parents take turn method.
        """
        if self.exn == "take-turn":
            raise Exception("take turn method in player errored out")
        return super().take_turn(s)

    def newTiles(self, st: List[Tile]):
        """
        Raises an exception if called for. Otherwise runs the desired parents newTiles method.
        """
        if self.exn  == "new-tiles":
            raise Exception("new tiles method in player errored out")
        super().newTiles(st)