from typing import List, Set, Dict

from Q.Common.Board.pos import Pos
from Q.Common.Board.tile import Tile
from Q.Common.map import Map
from Q.Common.rulebook import Rulebook


class RulebookConfig(Rulebook):
    """
        Represents the game rules which the referee and players may consult
        Source of truth of all dynamically changeable items of the game
        """
    def __init__(self, q_bonus: int, finish_bonus: int):
        self.q_bonus = q_bonus
        self.finish_bonus = finish_bonus
    def get_legal_positions(self, given_map: Map, given_tile: Tile, placed_positions: List[Pos],
                            break_early: bool = False) -> Set[Pos]:
        """
        Computes all of the legal positions to place the given tile onto the given map
        :param placed_positions: the positions that have already been placed
        :param given_map: the map searched for valid positions
        :param given_tile: the tile that is placed
        :return: a set of valid positions
        """
        return super().get_legal_positions(given_map,given_tile,placed_positions,break_early)

    def get_legal_hand(self, given_map: Map, hand: List[Tile], already_placed: List[Pos]) -> List[Tile]:
        """
        Gets the legal hand based on some rulebook
        """
        return super().get_legal_hand(given_map,hand,already_placed)

    def filter_adjacent_positions(self, neighbors: Dict[Pos, Tile], given_tile: Tile, map: Map) -> Set[Pos]:
        """
        Filters out the neighbors of a specific tile which the given tile can be placed
        :param neighbors: potential tile placements
        :param given_tile: the tile being placed
        :param map: the map at which we inspect for valid placements
        :return: the set of valid positions
        """
        return super().filter_adjacent_positions(neighbors,given_tile,map)

    def is_valid_space(self, given_map: Map, pos: Pos, given_tile: Tile) -> bool:
        """
        Is this given tile allowed to be placed at the given position on the given map according to the rulebook?
        :param given_map: the map at which we insect for a valid placement
        :param pos: the position of the potentially valid space
        :param given_tile: the tile we are trying to place
        :return: true if the tile can be placed
        """
        return super().is_valid_space(given_map,pos,given_tile)


    def valid_replacement(self, num_of_ref_tiles: int, player_hand: List[Tile]):
        """
        is this a valid replacement move
        :param num_of_ref_tiles: the number of ref tiles
        :param player_hand: the players current hand
        :return: true if a replacement is possible
        """
        return super().valid_replacement(num_of_ref_tiles,player_hand)

    def valid_placements(self, given_map: Map, placements: Dict[Pos, Tile]):
        return super().valid_placements(given_map,placements)

    def valid_placement(self, given_map: Map, pos: Pos, tile: Tile, tiles_placed: Dict[Pos, Tile]) -> bool:
        """
        if the given tiles can be placed according to the rules of the Q game
        :param given_map: the given map we are placing tiles at
        :param tiles_placed: the tiles attempting to be placed
        returns true if the tiles can be placed
        """
        return super().valid_placement(given_map,pos,tile,tiles_placed)

    def compatible_shapes(self, tile1: Tile, tile2: Tile):
        return super().compatible_shapes(tile1,tile2)

    def compatible_colors(self, tile1: Tile, tile2: Tile):
        return super().compatible_colors(tile1,tile2)

    # SCORING

    def score_turn(self, tiles: Dict[Pos, Tile], curr_map: Map, player_hand: List[Tile], end_game=False) -> int:
        """
        Calculates the points scored on a given turn
        Note: Everything has already been placed before scoring. So it's fine if the player hand is empty.
        :param tiles: the tiles placed which is a mapping from position to tile
        :param end_game: is the game over which add the end bonus points
        :param player_hand: Player's current hand
        :param curr_map: Current map to score turn
        :return: the points scored on a turn
        """
        return super().score_turn(tiles,curr_map,player_hand,end_game)

    def score_place_tiles(self, tiles: Dict[Pos, Tile]) -> int:
        """
        calculates the score for placing tiles
        :param tiles: the tiles that are placed to be scored
        :return the points valued to be scored
        """
        return len(tiles)

    def score_end_bonus_points(self, player_hand: List[Tile]) -> int:
        """
        calculates the score for the end bonus points if the player places all their tiles
        :param player_hand: the tiles that are placed on the board to be scored
        :return the points to be scored
        """
        if not len(player_hand):
            return self.finish_bonus
        else:
            return 0

    def get_contiguous_sequence_points(self, curr_map: Map, positions: List[Pos]) -> int:
        """
        From instructions: A Player receives one point per tile in a contiguous sequence of tiles (in a row or column)
        that contains at least one of its newly placed tiles.
        :param positions: List of positions played in a given turn
        :return: number of points to be added for this rule
        """
        return super().get_contiguous_sequence_points(curr_map,positions)

    def __get_seen_components_points(self, curr_map: Map, contiguous_positions: Set[Pos]) -> int:
        """
        Gets points for seen components for a list of positions contiguous rows/cols
        :param contiguous_positions: list of contiguous positions
        :return: points to be added
        """
        points = 0
        seen_component_shape = set()
        seen_component_color = set()
        for position in contiguous_positions:
            seen_component_shape.add(curr_map.tiles.get(position).shape)
            seen_component_color.add(curr_map.tiles.get(position).color)
            if (len(seen_component_shape) == 6 and len(seen_component_color) == 1) or \
                    (len(seen_component_color) == 6 and len(seen_component_shape) == 1):
                points += self.q_bonus
        return points

    def get_completing_q_points(self, curr_map: Map, positions: List[Pos]) -> int:
        """
        :param positions: determines the points for completing some number of q's
        :return: the points for completing q's
        """
        return super().get_completing_q_points(curr_map,positions)

    def all_same_row_or_col(self, tiles: List[Pos]) -> bool:
        """
        are all the tiles in the same row xor the same col?
        param: tiles: a list of pos which are checked if they are same row or col
        return: true if tiles are same row or col, else false
        """
        return super().all_same_row_or_col(tiles)
