import map as m
from game_state import game_state

"""
The inputs of xmap consist of two JSON values: a JMap object followed by a JTile.
The expected outputs is an array of JCoordinates, sorted in row-column order, 
listing all JCoordinates where this tile could be added to the given JMap.
"""
class map_converter():
    
    def __init__(self, input):
        self.input = input
        self.map = self._parse_map(self.input)

    # Parses the input json tile representation as a tile object
    def _parse_tile(self, tile_data):
        return m.Tile(tile_data['shape'], tile_data['color'])
    
    # Expands the map to fit the given JMap
    def expandMap(self,JMap) -> m.Map:
        new_map = m.Map()
        min_row = 0
        max_row = 0
        min_col = 0
        max_col = 0
        for jrow in JMap:
            if jrow[0] < min_row:
                min_row = jrow[0]
            if jrow[0] > max_row:
                max_row = jrow[0]
            list_of_jcell = jrow[1:]
            for jcell in list_of_jcell:
                if jcell[0] < min_col:
                    min_col = jcell[0]
                if jcell[0] > max_col:
                    max_col = jcell[0]
        new_map._expand(min_row,min_col)
        new_map._expand(max_row,max_col)
        #new_map.print_map()
        return new_map
    # Parses the input json map representation as a map object
    def _parse_map(self, map_data) -> m.Map:

        new_map = self.expandMap(map_data)
        #new_map.print_map()
        coord_traversed = []


        # Parse the json array string representing a map
        for jrow in map_data:
            row = jrow[0] + 1    # Adding 1 to both row and col to fit the coordinate system of our map data representation
            list_of_jcell = jrow[1: ]

            for jcell in list_of_jcell:
                col = jcell[0] + 1
                coord_traversed.append((row, col))
                tile = self._parse_tile(jcell[1])
                try:
                    new_map._place_tile_given(row, col, tile)
                    #print(row+new_map.rows_expanded,col + new_map.cols_expanded, (tile.get_shape(), tile.get_color()))
                # If there is already a tile (e.g. the init tile of the map)
                # place_tile_given throws a value error when a tile object already exists
                # at the given position
                except ValueError:
                    # Replace the tile with the current tile
                    new_map._replace_tile(row , col , tile)
        
        # If the coordinates of the map's initial tile isn't traversed 
        if (1,1) not in coord_traversed:
            # Remove the init tile
            new_map._replace_tile(1, 1, None)

        return new_map