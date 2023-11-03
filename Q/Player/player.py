import sys
import strategy as s
sys.path.insert(1,'../Common')
from map import Map, Tile
import game_state as g

"""
This module defines the Player_API class which represents a player in a game. 
The player is initialized with a name and a strategy. The player can get setup with the initial map and tiles, 
take a turn by passing, replacing tiles or extending the map with tile placements, receive a new set of tiles, 
and be informed whether it won or not.
"""
class Player_API():

    # Initializes the player with a name and optional exn
    def __init__(self, name: str, strat: str, exn = None):
        self.name = name
        self.strat = strat
        self.DAG = 'dag'
        self.LDASG = 'ldasg'
        self.exn = exn

    """
    // the player is handed the inital map, which is visible to all,

    // plus an initial set of tiles

    """
    # Setup the player with the initial map and tiles
    def setup(self, m: Map, bag_of_tiles: list, score: int):
        if self.exn == "setup":
            raise Exception()
        else:
            self.map = m
            self.bag_of_tiles = bag_of_tiles
            self.score = score
        
    """
    // after receiving the public part of state, a player

    // - passes,

    // - asks the referee to replace its set of tiles, or

    // - requests the extension of the map in the given state with

    //   some tile placements
    """
    #PASS or REPLACE or EXTENSION 
    def takeTurn(self, game: g):
        if self.exn != "take-turn":
            new_map = game._map
            ref_tiles_left = game.ref_tiles_left()
            if self.strat == self.DAG:
                xdag = s.dag(self.bag_of_tiles,new_map,ref_tiles_left)
                next_move = xdag.iterate()
            elif self.strat == self.LDASG:
                xldasg = s.ldasg(self.bag_of_tiles,new_map,ref_tiles_left)
                next_move = xldasg.iterate()
            else:
                return TypeError("Invalid Strategy")
            return next_move
        else:
            raise Exception()

 
    """
    // the player is handed a new set of tiles
    """

    def newTiles(self, Tiles: list):
        if self.exn != "new-tiles":
            self.bag_of_tiles = Tiles
        else:
            raise Exception()

    """
    // the player is informed whether it won or not
    """
    def win(self, win: bool):
        if self.exn != "win":
            self.has_won = win
        else:
            raise Exception()
