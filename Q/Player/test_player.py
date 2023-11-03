import unittest
import sys
sys.path.insert(1,'../Common')
from map import Map, Tile
from strategy import Strategy, dag, ldasg
from player import Player_API
import game_state as g

class TestPlayerAPI(unittest.TestCase):
    def setUp(self):
        self.player = Player_API("Test Player", 'dag')

    def test_setup(self):
        m = Map()
        bag_of_tiles = [Tile('star', 'red'), Tile('diamond', 'red'), Tile('circle', 'red')]
        self.player.setup(m, bag_of_tiles)
        self.assertEqual(self.player.map, m)
        self.assertEqual(self.player.bag_of_tiles, bag_of_tiles)
        self.assertEqual(self.player.score, 0)

    def test_takeTurn(self):
        game = g.game_state()
        self.player.bag_of_tiles = [Tile('star', 'red'), Tile('diamond', 'red'), Tile('circle', 'red')]
        self.assertEqual(self.player.takeTurn(game), [(self.player.bag_of_tiles[0], (0, 1))])

    def test_newTiles(self):
        new_tiles = [Tile('star', 'red'), Tile('diamond', 'red'), Tile('circle', 'red')]
        self.player.newTiles(new_tiles)
        self.assertEqual(self.player.bag_of_tiles, new_tiles)

    def test_win(self):
        self.player.win(True)
        self.assertTrue(self.player.has_won)
        self.player.win(False)
        self.assertFalse(self.player.has_won)

if __name__ == '__main__':
    unittest.main()