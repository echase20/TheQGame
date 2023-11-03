import unittest
import sys
from referee import referee

sys.path.insert(1,'../Common')
import game_state as g

sys.path.insert(1,'../Player')
from player import Player_API



# Tests a referee function with mock players by going through a whole Q game
class TestReferee(unittest.TestCase):
    def test_referee(self):
        # Set up mock player attributes
        player1 = Player_API('Alice','dag')
        player2 = Player_API('Bob','dag')
        player3 = Player_API('Charlie','dag')
        players = [player1, player2, player3]


        game = g.game_state()
        game.init_ref_tile_bag_testing()

        

        # Call referee function with mock players
        winners, eliminated = referee(players, game)

        # Check that the returned winners and eliminated lists are correct
        self.assertEqual(winners, [player2])
        self.assertEqual(eliminated, [])

if __name__ == '__main__':
    unittest.main()