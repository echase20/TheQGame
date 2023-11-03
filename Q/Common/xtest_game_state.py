import unittest
import map as Map
import game_state as g
import player_obs as Player


class TestGameState(unittest.TestCase):
    """
    This class contains unit tests for the game_state module.
    """

    def setUp(self):
        """
        This method is called before each test method.
        It creates a new instance of the game_state class.
        """
        self.game = g.game_state(6,6)

    def test_add_player(self):
        """
        This method tests the add_player method of the game_state class.
        It creates two player objects and adds them to the game.
        It then checks if the number of players in the game is equal to 2.
        """
        player1 = Player.Player(1, 25)
        player2 = Player.Player(2, 30)
        self.game.add_player(player1)
        self.game.add_player(player2)
        self.assertEqual(len(self.game.get_players()), 2)

    def test_add_duplicate_player(self):
        """
        This method tests the check_dup_id method of the game_state class.
        It creates two player objects with the same ID and adds them to the game.
        It then checks if the check_dup_id method returns True for the second player.
        """
        player1 = Player.Player(1, 25)
        player2 = Player.Player(1, 30)
        self.game.add_player(player1)
        self.game.check_dup_id(player2.get_id())
        self.assertTrue(self.game.check_dup_id(player2.get_id()))

    def test_sort_by_age(self):
        """
        This method tests the __sort_by_age method of the game_state class.
        It creates three player objects with different ages and adds them to the game.
        It then sorts the players by age and checks if the first player's ID is equal to 2.
        """
        player1 = Player.Player(1, 25)
        player2 = Player.Player(2, 30)
        player3 = Player.Player(3, 20)
        self.game.add_player(player1)
        self.game.add_player(player2)
        self.game.add_player(player3)
        self.game._sort_by_age()
        self.assertEqual(self.game.get_players()[0].get_id(), 2)

    
    def test_rotate_players(self):
        """
        This method tests the __rotate_players method of the game_state class.
        It creates three player objects and adds them to the game.
        It then rotates the players and checks if the active player's ID is equal to 2.
        """
        game1 = g.game_state(6, 6)
        player1 = Player.Player(1, 25)
        player2 = Player.Player(2, 30)
        player3 = Player.Player(3, 20)
        game1.add_player(player1)
        game1.add_player(player2)
        game1.add_player(player3)
        game1._active_player = player2
        game1._rotate_players()
        self.assertEqual(game1._active_player.get_id(), 2)
        

    def test_get_game_info(self):
        """
        This method tests the get_game_info method of the game_state class.
        It creates two player objects with different ages and adds them to the game.
        It then sorts the players by age and sets the active player to the second player.
        It then gets the game info and checks if the current turn player ID is equal to 2,
        the player scores are equal to {"1": 0, "2": 0}, and the tiles remaining is equal to 0.
        """
        player1 = Player.Player(1, 25)
        player2 = Player.Player(2, 30)
        self.game.add_player(player1)
        self.game.add_player(player2)
        self.game._sort_by_age()
        self.game._active_player = player2
        info = self.game.get_game_info()
        self.assertEqual(info["Gameplay Order"], [2, 1])
        self.assertEqual(info["Current Turn Player ID"], 2)
        self.assertEqual(info["Player Scores"], {"1": 0, "2": 0})
        self.assertEqual(info["Tiles remaining:"], 1080)

    def test_check_placement_validity(self):
        """
        This method tests the check_placement_validity method of the game_state class.
        It creates four tile objects with different colors and adds them to the game.
        It then checks if the placement of each tile is valid or not.
        """
        tile1 = Map.Tile("circle","red")
        tile2 = Map.Tile("circle","blue")
        tile3 = Map.Tile("circle","green")
        tile4 = Map.Tile("circle","yellow")      
        self.assertFalse(self.game.check_placement_validity(0, 0, tile1))
        self.assertTrue(self.game.check_placement_validity(0, 1, tile1))
        self.assertFalse(self.game.check_placement_validity(1, 0, tile3))
        self.assertFalse(self.game.check_placement_validity(1, 1, tile4))

    def test_score(self):
        tile1 = Map.Tile("red","clover")
        tile2 = Map.Tile("red","diamond")
        tile3 = Map.Tile("red","circle")
        tile4 = Map.Tile("blue","circle")
        tile5 = Map.Tile("red","square")
        tile6 = Map.Tile("blue","square")
        tile7 = Map.Tile("purple","square")
        """
        self.game.get_map().replace_tile(1, 1, tile1)
        self.game.get_map().place_tile_given(2,1, tile2)
        self.game.get_map().place_tile_given(3,1, tile3)
        self.game.get_map().place_tile_given(4,1, tile5)
        self.game.get_map().place_tile_given(4,2, tile6)
        self.game.get_map().place_tile_given(4,3, tile7)
        self.game.get_map().print_map()
        
        self.assertEqual(self.game.score_point([3],[2],[tile4],0), 5)
        """

        t1 = Map.Tile("green","8star")
        t2 = Map.Tile("green","clover")
        t3 = Map.Tile("red","clover")
        t4 = Map.Tile("green","diamond")
        t5 = Map.Tile("red","diamond")
        t6 = Map.Tile("green","circle")
        t7 = Map.Tile("red","circle")
        t9 = Map.Tile("red","square")
        t10 = Map.Tile("blue","square")
        t11 = Map.Tile("purple","square")
        t12 = Map.Tile("blue","circle")

        self.game.get_map()._replace_tile(1, 1, t3)
        self.game.get_map()._place_tile_given(1, 0, t2)
        self.game.get_map()._place_tile_given(2, 1, t5)
        self.game.get_map()._place_tile_given(2, 0, t4)
        self.game.get_map()._place_tile_given(3, 1, t7)
        self.game.get_map()._place_tile_given(3, 2, t12)
        self.game.get_map()._place_tile_given(4, 1, t9)
        self.game.get_map()._place_tile_given(4, 2, t10)
        self.game.get_map()._place_tile_given(4, 3, t11)
        self.game.get_map()._place_tile_given(0,0,t1)
        self.game.get_map()._place_tile_given(3,0,t6)

        self.game.get_map().print_map()

        self.assertEquals(self.game._score_point([0, 3],[0, 0],[t1,t6],0), 9)




if __name__ == '__main__':
    unittest.main()