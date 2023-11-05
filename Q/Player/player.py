from copy import deepcopy
from typing import List, Dict
from Q.Common.map import Map
from Q.Common.Board.pos import Pos
from Q.Common.Board.tile import Tile
from Q.Common.rulebook import Rulebook
from Q.Player.dag import Dag
from Q.Player.turn import Turn
from Q.Player.turn_outcome import TurnOutcome

from Q.Player.strategy import PlayerStrategy
from Q.Player.public_player_data import PublicPlayerData


class Player:
    """
    # represents a Player of a game
    """

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

    def setup(self, given_map: Map, tiles: List[Tile]):
        """
        Sets up the game by giving the player their tiles. We do not need to use the given_map but are keeping the
        parameter as this is a public API.
        """
        self.hand = tiles

    def take_turn(self, s: PublicPlayerData) -> Turn:
        """
        takes a turn for a player
        :param s: the public state
        :return: the turn the player does
        """
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

    def choose_move_type(self, pub_data: PublicPlayerData) -> TurnOutcome:
        """
        Returns the move type depending on the strategy and public data.
        :param pub_data: the public data about the game that player knows to determine the move type
        """
        if len(self.rulebook.get_legal_hand(pub_data.current_map, self.hand, [])):
            return TurnOutcome.PLACED
        if pub_data.num_ref_tiles < len(self.hand):
            return TurnOutcome.PASSED
        return TurnOutcome.REPLACED

    def get_tile_placement_choices(self, pub_data: PublicPlayerData) -> Turn:
        """
        Gets the placements of the given tiles in the players hand on the given map
        :param pub_data: the public data about the game that player knows to determine the move
        :return a dictionary of position to tile
        """
        tiles_to_place = {}
        turn_outcome = self.choose_move_type(pub_data)
        copy_hand = deepcopy(self.hand)
        legal_hand = self.rulebook.get_legal_hand(pub_data.current_map, copy_hand, list(tiles_to_place.keys()))
        if turn_outcome == TurnOutcome.PASSED or turn_outcome == TurnOutcome.REPLACED:
            return Turn(turn_outcome, tiles_to_place)

        while len(legal_hand):
            tile_placement = self.get_placement(pub_data, self.strategy, legal_hand, list(tiles_to_place.keys()))
            if not tile_placement:
                break
            copy_hand.remove(next(iter(tile_placement.values())))
            pub_data.current_map.add_tile_to_board_dict(placement=tile_placement)
            tiles_to_place.update(tile_placement)
            legal_hand = self.rulebook.get_legal_hand(pub_data.current_map, copy_hand, list(tiles_to_place.keys()))
        return Turn(turn_outcome, tiles_to_place)

    def get_placement(self, pub_data: PublicPlayerData, strategy: PlayerStrategy, hand: List[Tile], tiles_placed: List[Pos]) -> Dict[Pos, Tile]:
        """
        Determines a single placement for the given public data state with some given strategy
        :param tiles_placed: the tiles that have already been placed in this move
        :param pub_data: the public data for the player to make the move
        :param strategy: the given strategy to make the move
        :param hand: the legal hand of tiles that can be placed.
        """
        tile = strategy.choose_tile_to_play(hand, pub_data.current_map, self.rulebook)
        positions = self.rulebook.get_legal_positions(pub_data.current_map, tile, [])
        position_to_place_tile = strategy.choose_placement(list(positions), pub_data.current_map)
        if position_to_place_tile not in self.rulebook.get_legal_positions(pub_data.current_map, tile, tiles_placed):
            return {}

        return {position_to_place_tile: tile}
