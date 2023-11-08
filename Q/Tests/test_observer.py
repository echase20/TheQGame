import unittest

from Q.Common.Board.tile import Tile
from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Player.ldasg import LDasg
from Q.Player.player import Player
from Q.Referee.observer import Observer
from Q.Referee.referee import Referee


class TestObserver(unittest.TestCase):
    def setUp(self):
        self.tile1 = Tile(TileShape.CIRCLE, TileColor.BLUE)
        self.tile2 = Tile(TileShape.STAR, TileColor.BLUE)
        self.tile3 = Tile(TileShape.CLOVER, TileColor.BLUE)
        self.player1 = Player(strategy=LDasg(), name="bob1", hand=[self.tile2, self.tile3])
        self.player2 = Player(strategy=LDasg(), name="bob2", hand=[self.tile2, self.tile3])
        self.player3 = Player(strategy=LDasg(), name="bob3", hand=[self.tile2, self.tile3])
        pass

    def test_run_gui(self):
        ref = Referee(observer=Observer())
        ref.main([self.player1, self.player2, self.player3])

if __name__ == '__main__':
    unittest.main()
