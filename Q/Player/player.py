from abc import ABC, abstractmethod
from typing import List

from Q.Common.Board.tile import Tile
from Q.Common.map import Map
from Q.Common.rulebook import Rulebook
from Q.Player.dag import Dag
from Q.Player.public_player_data import PublicPlayerData
from Q.Player.strategy import PlayerStrategy
from Q.Player.turn import Turn


class Player(ABC):


    @abstractmethod
    def __init__(self, name, strategy: PlayerStrategy = Dag(), hand: List[Tile] = [], rulebook: Rulebook = Rulebook()):
        """
        # initializes a player with a given name, strategy and hand for the Q Game
        """
        self.strategy = strategy
        self._name = name
        self.hand = hand
        self.rulebook = rulebook

    def name(self) -> str:
        """
        Returns the player's name
        """
        return self._name

    @abstractmethod
    def setup(self, given_map: Map, tiles: List[Tile]):
        """
        Sets up the game by giving the player their tiles. We do not need to use the given_map but are keeping the
        parameter as this is a public API.
        """
        self.hand = tiles

    @abstractmethod
    def take_turn(self, s: PublicPlayerData) -> Turn:
        """
        takes a turn for a player
        :param s: the public state
        :return: the turn the player does
        """
        pass

    @abstractmethod
    def win(self, w: bool) -> None:
        """
        From specs: the player is informed whether it won or not
        :param w: boolean value to be used to inform the player whether they won
        """
        pass

    @abstractmethod
    def newTiles(self, st: List[Tile]):
        """
        From specs: The player is handed a new set of tiles
        :param st: set of tiles to be handed to the player
        """
        self.hand = st
