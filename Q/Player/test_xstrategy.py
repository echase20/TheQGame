import unittest
from unittest.mock import MagicMock
import sys
sys.path.insert(1,'../Common')
from map import Map, Tile
from strategy import dag, ldasg


# Testing the DAG Strategy class
class TestDAG(unittest.TestCase):
    def setUp(self) -> None:
        self.map = Map()
        self.ref_tiles_left = 1
        self.hand = [
            Tile('star', 'red'),
            Tile('diamond', 'red'),
            Tile('circle', 'red')
        ]
        self.dag = dag(self.hand, self.map, self.ref_tiles_left)

    # Find which tile and where it should be placed
    def test_find_tile_placement(self):
        
        self.assertEqual(self.dag.find_tile_placement(self.hand, self.map), (self.hand[0], (0, 1)))

    # Testing when to pass and when to replace
    def test_pass_or_replace(self):

        self.assertEqual(self.dag.pass_or_replace(), "pass")

        self.map = Map()
        self.ref_tiles_left = 4
        self.hand = [
            Tile('star', 'red'),
            Tile('diamond', 'red'),
            Tile('circle', 'red')
        ]
        strategy = dag(self.hand, self.map, self.ref_tiles_left)
        self.assertEqual(strategy.pass_or_replace(), "replace")

    def test_find_smallest_tile(self):
        tile1 = Tile('star', 'red')
        tile2 = Tile('diamond', 'purple')
        hand = [tile1, tile2]
        strategy = dag(hand, self.map, self.ref_tiles_left)
        self.assertEqual(strategy.find_smallest_tile(hand), tile1)

    def test_compare_shapes(self):
        tile1 = Tile('star', 'red')
        tile2 = Tile('diamond', 'purple')
        self.assertTrue(self.dag.compare_shapes(tile1, tile2))

    def test_iterate_hand(self):
        tile1 = Tile('star', 'red')
        tile2 = Tile('diamond', 'purple')
        tile3 = Tile('circle', 'red')
        tile4 = Tile('star', 'purple')
        tile5 = Tile('clover', 'red')
        hand = [tile1, tile2, tile3, tile4, tile5]
        strategy = dag(hand, self.map, self.ref_tiles_left)
        self.assertEqual(strategy.iterate(), [(tile1, (0, 1)),(tile4, (-1,1)), (tile3, (0,0)), (tile5, (0,-1)), (tile2, (-2,1))])



class TestLDASG(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    # Find which tile and where it should be placed
    def test_find_tile_placement(self):
        self.map = Map()
        self.ref_tiles_left = 1
        self.hand = [
            Tile('star', 'red'),
            Tile('diamond', 'red'),
            Tile('circle', 'red')
        ]
        self.strategy = ldasg(self.hand, self.map, self.ref_tiles_left)

        self.assertEqual(self.strategy.find_tile_placement(self.hand, self.map), (self.hand[0], (0, 1)))


    #Testing when to pass and when to replace
    def test_pass_or_replace(self):
        self.map = Map()
        self.ref_tiles_left = 1
        self.hand = [
            Tile('star', 'red'),
            Tile('diamond', 'red'),
            Tile('circle', 'red')
        ]
        self.strategy = ldasg(self.hand, self.map, self.ref_tiles_left)
        self.assertEqual(self.strategy.pass_or_replace(), "pass")

        self.map = Map()
        self.ref_tiles_left = 4
        self.hand = [
            Tile('star', 'red'),
            Tile('diamond', 'red'),
            Tile('circle', 'red')
        ]
        self.strategy = ldasg(self.hand, self.map, self.ref_tiles_left)
        self.assertEqual(self.strategy.pass_or_replace(), "replace")

    def test_iterate_hand(self):
        self.map = Map()
        self.ref_tiles_left = 1
        tile1 = Tile('star', 'red')
        tile2 = Tile('diamond', 'purple')
        tile3 = Tile('circle', 'red')
        tile4 = Tile('star', 'purple')
        tile5 = Tile('clover', 'red')
        hand = [tile1, tile2, tile3, tile4, tile5]
        strategy = ldasg(hand, self.map, self.ref_tiles_left)
        self.assertEqual(strategy.iterate(), [(tile1, (0, 1)),(tile4, (-1,1)), (tile3, (0,0)), (tile5, (1,0)), (tile2, (-2,1))])

if __name__ == '__main__':
    unittest.main()