import sys
import copy
sys.path.insert(1,'../Common')
from map import Map, Tile

class Strategy():
    """
    The Strategy class is an abstract class that defines the interface for all concrete strategy classes.
    """
    def __init__(self, hand: list, Map: Map, ref_tiles_left: int):
        """
        Initializes a new instance of the DAG strategy.

        Args:
        hand (list): The list of tiles in the player's hand.
        Map (Map): The game map.
        """
        self.hand = hand
        self.map = Map
        self.ref_tiles_left = ref_tiles_left
        self.Jpass = "pass"
        self.Jreplace = "replace"

    def iterate(self) -> list | str:
        """
        This method is responsible for iterating through the strategy.

        Returns:
        list: The list of tiles to place and where.
        str: Either "pass" or "replace".
        """

        # Uses a copy of the map in order to not modify the original map
        map_copy = []
        for row in self.map.map:
            row_list = []
            for col in row:
                row_list.append(col)
            map_copy.append(row_list)
        new_map = Map()
        new_map.map = map_copy
        new_map.rows_expanded = self.map.rows_expanded
        new_map.cols_expanded = self.map.cols_expanded
        player_hand = []
        # Adding the tiles to player hand
        for tile in self.hand:
            player_hand.append(tile)
        move_list = []
        for _ in range(6):
            next_move = self.next_move(player_hand,new_map)
            if type(next_move) == tuple:
                move_list.append(next_move)
                new_map._place_tile_given(next_move[1][0],next_move[1][1], next_move[0])
                player_hand.remove(next_move[0])
            else:
                #This if statement enforces that a list of moves is returned if possible, otherwise a string is returned
                if len(move_list) == 0:
                    return next_move
                else:
                    return move_list
        return move_list

    def next_move(self, hand: list, new_map) -> tuple | str:
        """
        This method is responsible for finding the tile(s) that should be placed and where.

        Returns:
        Tile: The tile that should be placed.
        """
        tile_to_place = self.find_tile_placement(hand,new_map)
        if tile_to_place:
            return tile_to_place
        else:
            return self.pass_or_replace()

    def find_tile_placement(self, new_map) -> tuple | bool:
        """
        This method is responsible for finding the tile(s) that should be placed and where.

        Returns:
        Tile: The tile that should be placed.
        """
        pass
    
    def pass_or_replace(self):
        """
        This method is responsible for deciding whether the player should pass or replace its tiles if placing at least one is impossible.
        """
        if self.ref_tiles_left < len(self.hand):
            return "pass"
        else:
            return "replace"

    def find_smallest_tile(self, hand: list) -> Tile:
        """
        This method is responsible for finding the smallest tile in the hand lexographically.

        Args:
        hand (list): The list of tiles to search through.

        Returns:
        Tile: The smallest tile in the hand.
        """
        smallest_so_far = []
        for tile in hand:
            if len(smallest_so_far) == 0:
                smallest_so_far.append(tile)
            elif self.compare_shapes(tile, smallest_so_far[-1]):
                smallest_so_far.append(tile)
        return smallest_so_far[-1]
    
    def compare_shapes(self, tile1: Tile, tile2: Tile) -> bool:
        """
        This method is responsible for comparing two tiles and returning True if tile1 is smaller lexographically than tile2, otherwise False.

        Args:
        tile1 (Tile): The first tile to compare.
        tile2 (Tile): The second tile to compare.

        Returns:
        bool: True if tile1 is smaller lexographically than tile2, otherwise False.
        """
        shapes = ['star', '8star', 'square', 'circle', 'clover', 'diamond']
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']
        if tile1.get_shape() == tile2.get_shape():
            color1 = tile1.get_color()
            color2 = tile2.get_color()
            return colors.index(color1) < colors.index(color2)
        else:
            shape1 = tile1.get_shape()
            shape2 = tile2.get_shape()
            return shapes.index(shape1) < shapes.index(shape2)  

class dag(Strategy):
    """
    The DAG strategy is a concrete strategy class that implements the Strategy interface.
    """
    def __init__(self, hand: list, Map: Map, ref_tiles_left: int):
        """
        Initializes a new instance of the DAG strategy.

        Args:
        hand (list): The list of tiles in the player's hand.
        Map (Map): The game map.
        """
        super().__init__(hand, Map, ref_tiles_left)
        
    def iterate(self) -> list | str:
        """
        This method is responsible for iterating through the DAG strategy.

        Returns:
        list: The list of tiles to place and where.
        str: Either "pass" or "replace".

        """
        return super().iterate()
    
    def next_move(self, hand, map_copy) -> tuple | str:
        """
        This method is responsible for finding the tile(s) that should be placed and where using the DAG strategy.

        Returns:
        Tile: The tile that should be placed.
        """
        return super().next_move(hand, map_copy)

    def find_tile_placement(self, hand: list, new_map) -> tuple | bool:
        """
        This method is responsible for finding the tile(s) that should be placed and where using the DAG strategy.

        Returns:
        Tile: The tile that should be placed.
        Posn_list: The list of positions that have already been placed on.
        """
        player_hand = hand
        for _ in range(len(player_hand)):
            tile_to_place = self.find_smallest_tile(player_hand)
            valid_positions = new_map._valid_pos(tile_to_place)
            if len(valid_positions) == 0:
                player_hand.remove(tile_to_place)
            else:
                return (tile_to_place, valid_positions[0])

                # valid_pos returns possible placements in order
        return False
    

    def pass_or_replace(self) -> str:
        """
        This method is responsible for deciding whether the player should pass or replace its tiles if placing at least one is impossible using the DAG strategy.
        """
        return super().pass_or_replace()

    def find_smallest_tile(self, hand: list) -> Tile:
        """
        This method is responsible for finding the smallest tile in the hand lexographically.

        Args:
        hand (list): The list of tiles to search through.

        Returns:
        Tile: The smallest tile in the hand.
        """
        return super().find_smallest_tile(hand)
    
    def compare_shapes(self, tile1: Tile, tile2: Tile) -> bool:
        """
        This method is responsible for comparing two tiles and returning True if tile1 is smaller lexographically than tile2, otherwise False.

        Args:
        tile1 (Tile): The first tile to compare.
        tile2 (Tile): The second tile to compare.

        Returns:
        bool: True if tile1 is smaller lexographically than tile2, otherwise False.
        """
        return super().compare_shapes(tile1, tile2)

        

class ldasg(Strategy):
    """
    The LDASG strategy is a concrete strategy class that implements the Strategy interface.
    """
    def __init__(self, hand: list, Map: Map, ref_tiles_left: int):
        """
        Initializes a new instance of the LDASG strategy.

        Args:
        hand (list): The list of tiles in the player's hand.
        Map (Map): The game map.
        """
        super().__init__(hand, Map, ref_tiles_left)
        
    def iterate(self) -> list | str:
        """
        This method is responsible for iterating through the LDASG strategy.

        Returns:
        list: The list of tiles to place and where.
        str: Either "pass" or "replace".

        """
        return super().iterate()
    
    def next_move(self, hand, new_map) -> tuple | str:
        """
        This method is responsible for finding the tile(s) that should be placed and where using the LDASG strategy.

        Returns:
        Tile: The tile that should be placed.
        """
        return super().next_move(hand, new_map)

    def find_tile_placement(self, hand: list, new_map) -> tuple | bool:
        """
        This method is responsible for finding the tile(s) that should be placed and where using the LDASG strategy.
        """
        player_hand = hand
        for i in range(len(player_hand)):
            tile_to_place = self.find_smallest_tile(player_hand)
            if len(new_map._valid_pos(tile_to_place)) == 0:
                player_hand.remove(tile_to_place)
            elif len(new_map._valid_pos(tile_to_place)) > 1:
                 # position with most neighbors
                pos = self.most_neighbors(new_map._valid_pos(tile_to_place), new_map)

                return (tile_to_place, pos)
                
            else:
                return (tile_to_place, new_map._valid_pos(tile_to_place)[0]) 
        return False

    def most_neighbors(self, pos: list, new_map) -> tuple:
        """
        This method is responsible for finding the position with the most neighbors.
        The method assumes that the list of positions is valid.

        Args:
        pos (list): The list of positions to search through.

        Returns:
        tuple: The position with the most neighbors.
        """
        max_neighbors = 0
        max_pos = None
        for position in pos:
            if new_map._coordinates_count_neighbors(position[0], position[1]) > max_neighbors:
                max_neighbors = new_map._coordinates_count_neighbors(position[0], position[1])
                max_pos = position
        return max_pos

    def find_smallest_tile(self, hand: list) -> Tile:
        """
        This method is responsible for finding the smallest tile in the hand lexographically.

        Args:
        hand (list): The list of tiles to search through.

        Returns:
        Tile: The smallest tile in the hand.
        """
        return super().find_smallest_tile(hand)
    
    def compare_shapes(self, tile1: Tile, tile2: Tile) -> bool:
        """
        This method is responsible for comparing two tiles and returning True if tile1 is smaller lexographically than tile2, otherwise False.

        Args:
        tile1 (Tile): The first tile to compare.
        tile2 (Tile): The second tile to compare.

        Returns:
        bool: True if tile1 is smaller lexographically than tile2, otherwise False.
        """
        return super().compare_shapes(tile1, tile2)

"""  
def main():
    tile1 = Tile('star', 'red')
    tile2 = Tile('diamond', 'purple')
    hand = [tile1,tile2]
    test = dag(hand, 1)
    print(test.find_smallest_tile(hand).get_color())
    #print(test.find_tile_placement)

if __name__ == "__main__":
    main()
    """