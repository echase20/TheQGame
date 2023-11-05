from abc import ABC, abstractmethod
from typing import List
from Q.Common.Board.pos import Pos
from Q.Common.Board.tile import Tile
from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.map import Map
from Q.Common.rulebook import Rulebook


class PlayerStrategy(ABC):
    """
    The abstract class (ABC) for automated player strategies.
    """
    @abstractmethod
    def choose_placement(self, possible_positions: List[Pos], given_map: Map) -> Pos:
        """
        Calls get_smallest_placement by default
        """
        return self.get_smallest_placement(possible_positions)

    @abstractmethod
    def choose_tile_to_play(self, filtered_hand: List[Tile], given_map: Map, rulebook: Rulebook) -> Tile:
        """
        Defaults to choosing the smallest tile
        :returns: smallest tile in hand
        """
        smallest_shape_rank = min([tile.shape.value for tile in filtered_hand])
        tiles_with_smallest_shape_rank = [tile for tile in filtered_hand if tile.shape.value == smallest_shape_rank]

        smallest_color_rank = min([tile.color.value for tile in tiles_with_smallest_shape_rank])
        # If we have multiple of the same smallest tile, we just return the first one.
        smallest_tile = [tile for tile in tiles_with_smallest_shape_rank if tile.color.value == smallest_color_rank][0]
        return smallest_tile


    def get_smallest_placement(self, possible_positions: List[Pos]) -> Pos:
        """
        Chooses smallest placement by row-column order
        """
        smallest_row = min([position.y for position in possible_positions])
        positions_with_smallest_row = [position for position in possible_positions if position.y == smallest_row]

        return min(positions_with_smallest_row, key=lambda position: position.x)
