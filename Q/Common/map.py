from ShapeRenderer import ShapeRenderer as sp
import random

# List of possible cshape colors 
colors = ["red", "green", "blue", "yellow", "orange", "purple"]
# List of possible shapes
shapes = ["star", "8star", "square", "circle", "diamond", "clover"]

"""
- Explainations on reading the coordinates
- place_tile_given throw exception
- valid_pos should be factored into multiple function 

- Explain coordinates of the map
"""

# Represents a Tile object that has two attributes: shape and color
class Tile:
    color = 0
    shape = 0

    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
    def get_color(self) -> str:
        return self.color
    def get_shape(self) -> str:
        return self.shape
# Represents the game map and handles generation, placement, and restriction of tile placement
class Map:

    # 3 x 3 beginning tile
    # Automatically genrates ref tile when the board is created
    def __init__(self) -> None:
        self.map = [[None,None,None],[None,None,None],[None,None,None]]
        self.rows_expanded = 0
        self.cols_expanded = 0
        self._generate_ref()

    # Returns a tile with randomly chosen color and shape
    def generate_tile(self) -> Tile:
        return Tile(shapes[random.randrange(0,len(shapes))], colors[random.randrange(0,len(colors))])

    # Generates the referee tile and places it in the middle of the map
    # It is currently a red star for testing purposes
    def _generate_ref(self):
        self.map[1][1] = Tile("star","red")#self.generate_tile()

    def _get_tile(self,row: int,col: int) -> Tile:
        return self.map[row+self.rows_expanded][col+self.cols_expanded]
    # Expand the map array in the given "up"
    def _expand(self, new_row, new_col):
        curr_rows = len(self.map)
        curr_cols = len(self.map[0])
        # Expand rows below
        if new_row >= curr_rows - self.rows_expanded - 1:
            for _ in range(new_row - curr_rows + self.rows_expanded + 1):
                self.map.append([None] * curr_cols)
        
        # Expand columns to the right
        if new_col >= curr_cols - self.cols_expanded - 1:
            for row in self.map:
                row.extend([None] * (new_col - curr_cols + self.cols_expanded + 1))

        # Expand rows upwards
        if new_row < (-1*self.rows_expanded):
            for _ in range(abs(new_row) - self.rows_expanded):
                self.rows_expanded += 1
                self.map.insert(0, [None] * len(self.map[0]))

        # Expand columns to the left
        if new_col < (-1*self.cols_expanded):
            self.cols_expanded -= new_col
            for row in self.map:
                row[:0] = [None] * abs(new_col)
    
    # Replace the current tile object, if any, at the given coordinates with the given tile.
    def _replace_tile(self, row, col, tile):
        row += self.rows_expanded
        col += self.cols_expanded
        if self._coordinates_in_bound(row-self.rows_expanded,col-self.cols_expanded):
            self.map[row][col] = tile
        else:
            raise IndexError("The given pair of coordinates is out of the bounds of the map.")
            
    def _delete_tile(self, row, col):
        self.map[row][col] = None
        
    # Takes in a tile and place it at row, col on the board; for testing
    def _place_tile_given(self, row, col, tile):
        real_row = row + self.rows_expanded
        real_col = col + self.cols_expanded
        if not self._coordinates_in_bound(row, col):
            raise IndexError("The given pair of coordinates is out of the bounds of the map.")
        elif not self._coordinates_have_neighbhors(row,col):
            raise ValueError("There is no tile neighboring the given pair of coordinates.")
        elif self.map[real_row][real_col] != None:
            raise ValueError("A tile already exist at the given pair of coordinates.")
        else:
            self.map[real_row][real_col] = tile
            # Expand toward all necessary directions
            self._expand(row + 1, col + 1)
            self._expand(row - 1, col - 1)

    # Generates a random tile and places it at row, col
    def _place_tile(self, row, col):
        self._place_tile_given(row, col, self.generate_tile())

    # Checks that a coordinate is within the bounds of the map's coordinates
    def _coordinates_in_bound(self, row : int, col : int) -> bool:
        row = row + self.rows_expanded
        col = col + self.cols_expanded
        return row > -1 and row < len(self.map) and col > -1 and col < len(self.map[0])

    # Checks that a given coordinate is valid and can hold a new tile
    def _coordinates_have_neighbhors(self, row : int, col : int) -> bool:
        # maximum indices of the coordinates within the current map
        row = row + self.rows_expanded
        col = col + self.cols_expanded
        max_row = len(self.map) - 1
        max_col = len(self.map[0]) - 1

        # Check if the tiles at the coordinates to the left, right, up, or down of the 
        # given coordinates has a tile
        left_valid = (col != 0) and self.map[row][col - 1] != None
        right_valid = (col != max_col) and self.map[row][col + 1] != None
        top_valid = (row != 0) and self.map[row - 1][col] != None
        bottom_valid = (row != max_row) and self.map[row + 1][col] != None

        return left_valid or right_valid or top_valid or bottom_valid
    
    # Checks how many neighbors a given coordinate has
    def _coordinates_count_neighbors(self, row : int, col : int) -> int:
        # maximum indices of the coordinates within the current map
        row = row + self.rows_expanded
        col = col + self.cols_expanded
        counter = 0
        # Check if the tiles at the coordinates to the left, right, up, or down of the 
        # given coordinates has a tile, if they do, it enumerates the counter by 1
        try:
            if self.map[row][col - 1] != None:
                counter += 1
            if self.map[row][col + 1] != None:
                counter += 1
            if self.map[row - 1][col] != None:
                counter += 1
            if self.map[row + 1][col] != None:
                counter += 1
        except IndexError:
            pass

        return counter
    
    # Return a list of valid indices to place a given tile based on shape and color
    def _valid_pos(self, tile : Tile) -> list:
        # A set of all possible indices to place the given tile
        all_pos_indices = set()
        # A set of invalid indices to place the given tile
        invalid_indices = set()
        # Traverse each item (Tile and None) in the map
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):

                # Set curr to be the current item in the map
                curr = self.map[row][col]

                # If a tile is present at the given coordinate
                if curr != None:
                    
                    # Create strings representing the x and y coordinates of the possible positions in the map
                    up = (row - 1, col)
                    down = (row + 1, col)
                    left = (row, col - 1)
                    right = (row, col + 1)

                    # Add the coordinate of the current Tile, as new Tiles cannot be placed on existing Tiles
                    invalid_indices.add((row-self.rows_expanded, col-self.cols_expanded))
                    # If the given Tile matches either the color or the shape of the current Tile
                    if (curr.get_color() == tile.color or curr.get_shape() == tile.shape):
                        
                        # Add the coordinate-strings of the surrounding Tiles to the set of all_pos_indices
                        all_pos_indices.add((up[0]-self.rows_expanded,up[1]-self.cols_expanded))
                        all_pos_indices.add((down[0]-self.rows_expanded,down[1]-self.cols_expanded))
                        all_pos_indices.add((left[0]-self.rows_expanded,left[1]-self.cols_expanded))
                        all_pos_indices.add((right[0]-self.rows_expanded,right[1]-self.cols_expanded))
                    # If the given Tile has no common attribute with the current Tile
                    else:

                        # Add all surrounding coordinate-strings to the set of invalid indices
                        invalid_indices.add((up[0]-self.rows_expanded,up[1]-self.cols_expanded))
                        invalid_indices.add((down[0]-self.rows_expanded,down[1]-self.cols_expanded))
                        invalid_indices.add((left[0]-self.rows_expanded,left[1]-self.cols_expanded))
                        invalid_indices.add((right[0]-self.rows_expanded,right[1]-self.cols_expanded))
        # Remove the intersection between all possible indices and the invalid indices
        all_pos_indices.difference_update(invalid_indices)

        # A list to include all valid locations to place the Tile
        valid_indices = list(all_pos_indices)
        valid_indices.sort()
        return valid_indices

    
    # Prints the current map
    def print_map(self):
    
        for row in self.map:
            r = ""
            for item in row:
                c = ""
                if item != None:
                    c += item.shape + "," + item.color
                else:
                    c += str(item) 
                
                r += c.ljust(20)
            print(r)
            
    # Saves the current map with the renderings of the shapes and colors using the utils file
    # The utils file handles the shape and color renderings    
    def show_map(self):

        s = sp(len(self.map[0]))

        for row in self.map:
            for item in row:
                if item == None:
                    s.make_shape("","",)
                else:
                    s.make_shape(item.get_shape(), item.get_color())

        s.save_images("map.png")

"""
def main():
    m = Map()
    pass

if __name__ == "__main__":
    main()
"""