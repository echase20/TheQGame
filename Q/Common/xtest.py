import unittest
import map as m
import ShapeRenderer as u


# List of possible cshape colors 
colors = ["red", "green", "blue", "yellow", "orange", "purple"]
# List of possible shapes
shapes = ["star", "8star", "square", "circle", "diamond", "clover"]


class TestMap(unittest.TestCase):

    # Creating test tiles
    t1 = m.Tile("8star", "blue")
    t2 = m.Tile("circle", "yellow")
    t3 = m.Tile("diamond", "green")
    t4 = m.Tile("square", "orange")
    t5 = m.Tile("star", "purple")
    t6 = m.Tile("clover", "red")

        
    # Setting up the Map
    # Setting up the Map automatically creates a red star for the ref tile for testing purposes.
    def setUp(self):
        self.map = m.Map()


    # Testing if the generate ref tile creates a random tile in the center of the board. 
    # (for testing purposes we made the generate ref create a red star)
    def test_generate_ref(self):
        self.setUp()
        ref_tile = self.map.map[1][1]
        self.assertIsNotNone(ref_tile)
        self.assertIn(ref_tile.shape, shapes)
        self.assertIn(ref_tile.color, colors)


    # Testing that placing a tile only works if the tile is adjacent to other tiles
    # The cordinates do change due to map expansion when a tile is placed on the edge of the map
    def test_place_tile_valid(self):
        self.setUp()
        t1 = m.Tile("8star", "red")
        t2 = m.Tile("star", "yellow")
        t3 = m.Tile("circle", "yellow")

        # Test 1
        self.map._place_tile_given(1, 0, t1)
        # Coordinates becomes (1,1) due to map expansion
        self.assertIsNotNone(self.map._get_tile(1, 0))
    
        # Test 2
        self.map._place_tile_given(2, 1, t2)
        # Coordinates becomes (2, 1) due to map expansion
        self.assertIsNotNone(self.map._get_tile(2, 1))

        # Test 3
        self.map._place_tile_given(2, 2, t3)
        # Coordinates becomes (2, 2) due to map expansion
        self.assertIsNotNone(self.map._get_tile(2, 2))

        self.map._place_tile_given(1, -1, t1)
        self.assertIsNotNone(self.map._get_tile(1, -1))


    # Tests that if a tile is placed not adjacent to other tiles, the spot will remain (None) and 
    # The message "Cannot place tile at the given index" will be given
    def test_place_tile_invalid(self):
        self.setUp()
        t1 = m.Tile("8star", "red")
        with self.assertRaises(ValueError):
            self.map._place_tile_given(0, 0, t1)

    
    # Testing to see the valid places where a tile of specific shape or color can be placed
    def test_valid_pos_valid(self):
        self.setUp()
        t1 = m.Tile("8star", "red")
        self.map._place_tile_given(1, 0, t1)
        self.assertEqual(self.map._valid_pos(t1), [(0,0),(0, 1),(1,-1),(1,2),(2,0),(2, 1)])


    
# Running the tests in the console
if __name__ == '__main__':
    unittest.main()
