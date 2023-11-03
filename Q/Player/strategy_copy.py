import sys
sys.path.insert(1,'../Common')
from map import Map, Tile

 #This is an old implementation that is being retired. Still holding on to it if we find bugs with new 
 # code in the future
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
        player_hand = []
        posn_list = []
        for tile in self.hand:
            player_hand.append(tile)
        move_list = []
        for _ in range(len(player_hand)):
            next_move = self.next_move(player_hand,posn_list)
            if type(next_move) == str:
                #This if statement enforces that a list of moves is returned if possible, otherwise a string is returned
                if len(move_list) == 0:
                    return self.pass_or_replace()
                else:
                    return move_list
            else:
                tile_to_place= next_move
                move_list.append(tile_to_place)
                posn_list.append(tile_to_place[1])
                player_hand.remove(tile_to_place[0])
        return move_list

    def next_move(self, hand: list, posn_list) -> tuple | str:
        """
        This method is responsible for finding the tile(s) that should be placed and where.

        Returns:
        Tile: The tile that should be placed.
        """
        tile_to_place = self.find_tile_placement(hand,posn_list)
        if tile_to_place:
            return tile_to_place
        else:
            return self.pass_or_replace()

    def find_tile_placement(self) -> tuple | bool:
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
            return self.Jpass
        else:
            return self.Jreplace

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
    
    def next_move(self, hand, posn_list) -> tuple | str:
        """
        This method is responsible for finding the tile(s) that should be placed and where using the DAG strategy.

        Returns:
        Tile: The tile that should be placed.
        """
        return super().next_move(hand, posn_list)

    def find_tile_placement(self, hand: list, posn_list) -> tuple | bool:
        """
        This method is responsible for finding the tile(s) that should be placed and where using the DAG strategy.

        Returns:
        Tile: The tile that should be placed.
        Posn_list: The list of positions that have already been placed on.
        """
        player_hand = hand
        for _ in range(len(player_hand)):
            tile_to_place = self.find_smallest_tile(player_hand)
            valid_positions = self.map._valid_pos(tile_to_place)
            if len(valid_positions) == 0:
                player_hand.remove(tile_to_place)
            else:
                for i in range(len(valid_positions)):
                    if valid_positions[i] not in posn_list:
                        return (tile_to_place, valid_positions[i])
                    else:
                        continue
                # valid_pos returns possible placements in order
                return False
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
    
    def next_move(self, hand, posn_list) -> tuple | str:
        """
        This method is responsible for finding the tile(s) that should be placed and where using the LDASG strategy.

        Returns:
        Tile: The tile that should be placed.
        """
        return super().next_move(hand, posn_list)

    def find_tile_placement(self, hand: list, posn_list) -> tuple | bool:
        """
        This method is responsible for finding the tile(s) that should be placed and where using the LDASG strategy.
        """
        player_hand = hand
        for i in range(len(player_hand)):
            tile_to_place = self.find_smallest_tile(player_hand)
            if len(self.map._valid_pos(tile_to_place)) == 0:
                player_hand.remove(tile_to_place)
            elif len(self.map._valid_pos(tile_to_place)) > 1:
                 # position with most neighbors
                pos = self.most_neighbors(self.map._valid_pos(tile_to_place), posn_list)

                return (tile_to_place, pos)
                
            else:
                if self.map._valid_pos(tile_to_place)[0] not in posn_list:
                    return (tile_to_place, self.map._valid_pos(tile_to_place)[0]) 
                else:
                    return False
        return False

    def most_neighbors(self, pos: list, posn_list) -> tuple:
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
            if position in posn_list:
                continue
            if self.map._coordinates_count_neighbors(position[0], position[1]) > max_neighbors:
                max_neighbors = self.map._coordinates_count_neighbors(position[0], position[1])
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

    
def main():
    tile1 = Tile('star', 'red')
    tile2 = Tile('diamond', 'purple')
    hand = [tile1,tile2]
    test = dag(hand, 1)
    print(test.find_smallest_tile(hand).get_color())
    #print(test.find_tile_placement)

if __name__ == "__main__":
    main()


