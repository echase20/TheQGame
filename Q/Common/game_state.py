import map as Map
import player_obs as Player
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from map import Tile
import ShapeRenderer as ShapeRenderer
from collections import deque 
import random
"""
- GAME STATE DATA REPRESENTATION -
The class game_state represents a game state of the Q Game. 
In accord with the functionalities of a game state, the game_state class keeps track of the following data as fields:
    1. self._map  --> The map representation of the game from map.py
    2. self._players --> a list representing the players (2 to 4) that are currently in the game
    3. self._active_player --> the Player object to make the current turn.
    4. self._active_player_index --> the index of the active Player object within the list self._players
    5. self._ref_tiles --> The list (stack) of tiles that the referee currently has. 
    _ref_tiles will be set to a list including all 1080 possible tiles.
"""

class game_state:
    def __init__(self, end_game_bonus, q_score_bonus):
        """
        Initializes a game state object with a map, players, active player, referee tiles, end game bonus and q score bonus.

        Parameters:
        end_game_bonus (int): Bonus points for the player with the most completed features at the end of the game.
        q_score_bonus (int): Bonus points for the player with the highest q score at the end of the game.
        """
        self._map = Map.Map()
        self._players = []            
        self._active_player = None
        self._active_player_index = 0
        self._ref_tiles = deque()          
        self.init_ref_tile_bag()
        self.end_game_bonus = end_game_bonus
        self.q_score_bonus = q_score_bonus

    def set_map(self, map : Map.Map):
        """
        Set the map of the game to the given map.

        Parameters:
        map (Map.Map): A Map object to be saved as the map of the game state.
        """
        self._map = map

    def set_ref_tiles(self, tiles: deque):
        self._ref_tiles = tiles

    def get_map(self):
        """
        Returns the map of the game.
        """
        return self._map

    def get_players(self):
        """
        Returns the list of players.
        """
        return self._players
    
    def init_ref_tile_bag(self) -> None:
        """
        Creates the ref tile bag.
        """
        shapes = ['star', '8star', 'square', 'circle', 'clover', 'diamond']
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']
        for shape in shapes:
            for color in colors:
                for _ in range(30):
                    self._ref_tiles.append(Tile(shape, color))
        random.shuffle(self._ref_tiles)
        
    def init_ref_tile_bag_testing(self) -> None:
        """
        Creates the ref tile bag for testing.
        """
        self._ref_tiles.clear()
        shapes = ['star', '8star', 'square', 'circle', 'clover', 'diamond']
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']
        for shape in shapes:
            for color in colors:
                for _ in range(1):
                    self._ref_tiles.append(Tile(shape, color))


        
    def TileBag(self,number_of_tiles) -> list:
        """
        Creates the player tile bag with the number of tiles.

        Parameters:
        number_of_tiles (int): The number of tiles to be added to the player tile bag.

        Returns:
        list: A list of tiles.
        """
        new_bag = []
        for _ in range(number_of_tiles):
            new_tile = self._ref_tiles.popleft()
            new_bag.append(new_tile)

        return new_bag
    
    def _game_over(self) -> bool:
        """
        Checks if the game is over.

        Returns:
        bool: True if the game is over, False otherwise.
        """
        #Checking that there are a correct amount of players
        if len(self._players) < 2:
            return True
        elif len(self._players) > 4:
            return True
        elif self.ref_tiles_left == 0:
            return True
        return False
    
    def check_dup_id(self, id : int) -> bool:
        """
        Checks that a player of the given id already exist in the list.

        Parameters:
        id (int): An unique integer that identifies the Player object.

        Returns:
        bool: True if a player of the same id exists, False otherwise.
        """
        for player in self._players:
            if player.get_id() == id:
                return True
        return False
    
    def ref_tiles_left(self):
        """
        Returns the number of tiles left in the referee's stack.
        """
        return len(self._ref_tiles)

    def add_player(self, player : Player.Player):
        """
        Adds the given player to the list.

        Parameters:
        player (Player.Player): The Player object to be added to the game state's list of players.
        """
        if type(player) is Player.Player:
            # If a player with the same id does not already exist in the game
            if not self.check_dup_id(player.get_id()):
                self._players.append(player)
            else:
                raise ValueError("A player with the given ID already exists in this game.")
        else:
            raise TypeError("The input is not of type Player.")
    
    def _sort_by_age(self):
        """
        Sorts the list of players in the order of their ages.
        """
        self._players.sort(key=(lambda player : player.get_info()['age']), reverse=True)

    def _rotate_players(self):
        """
        Moves the active player's index to the next player.
        """
        # Calculate the next player's index (order) within the list
        self._active_player_index = (len(self._players) + self._active_player_index + 1) % len(self._players)
        # Set the active player to the player of the next index
        self._active_player = self._players[self._active_player_index]
    
    def _print_map(self):
        """
        Gets the current map state of the game.
        """
        return self._map.print_map()
    

    def get_game_info(self) -> dict:
        """
        Extracts the data to be sent to a player when it is its turn.

        Returns:
        dict: A dictionary that is a data representation for all the information the current player will receive.
        """
        # Order of gameplay
        order = self._get_order()
        # id of the current player
        active_player = self._active_player.get_id()
        # scores    
        scores = self._get_all_scores()
        # ref's tiles? 
        num_tiles = len(self._ref_tiles)

        return {"Gameplay Order" : order, 
                "Current Turn Player ID" : active_player, 
                "Player Scores" : scores, 
                "Tiles remaining:" : num_tiles}

    # Returns the list of strings (player ids) in the order of the gameplay
    def _get_order(self) -> list:
        ids_in_order = []
        
        for player in self._players:
            ids_in_order.append(player.get_id())
        
        return ids_in_order
    
    # Compile a dictionary where the each key is each player's id and each value is the player's 
    # according score
    def _get_all_scores(self) -> list:
        all_scores = dict()

        for player in self._players:
            all_scores[str(player.get_id())] = player.get_info()['score']

        return all_scores
    
    """
    Functionality #2: for completing a turn action.
    
    - The function takes in a string representing the current player's choice for its turn.
    - The choice can either be "pass", "exchange", or "place", according to the rules
      of the Q Game.
        1. If the input choice is neither of the above, throw an exception explaining the error.
        2. If the choice is "pass", the game state will move on to the next player in the game's order
           by invoking the function rotate_players.
        3. If the choice is "exchange", the game state will invoke exchange_tiles (place holder for 
           milestone #3).
        4. If the choice is "place", the tate will invoke place_tile (place holder for 
           milestone #3).
    - Not yet implemented - The method should eventually check to make sure that only the active player
      is allowed these choices during their turn.
    """


    """
    This method calculates points scored for a series of placements

    Args:
    row_list (list): The list of row coordinates for the placements to be scored
    col_list (list): The list of column coordinates for the placements to be scored
    tile_list (list): The list of tiles for the placements to be scored
    tiles_left (int): The number of tiles in the hand of the player who made the placements

    Returns:
    int: The points scored on the series of placements
    """
    def _score_point(self, row_list, col_list, tile_list, tiles_left):
        points = 0
        #checks if the player has placed all their tiles
        if len(tile_list) == tiles_left:
            points = points + self.end_game_bonus
        points = points + len(tile_list)
        row_visited = []
        col_visited = []
        for i in range(len(row_list)):
            continuous_points,row_visited,col_visited = self._continuous_sequence_points(row_list[i], col_list[i], row_visited, col_visited)
            points = points + continuous_points
            q_points_color = self._q_score_color(row_list[i], col_list[i],tile_list[i]) 
            q_points_shape = self._q_score_shape(row_list[i], col_list[i],tile_list[i])
            points += q_points_color + q_points_shape
        return points    
    
    # Returns the number of continuous sequence of tiles that the given tile is a part of
    
    def _continuous_sequence_points(self, row ,col,row_visited,col_visited):
            """
            Calculates the number of points in a continuous sequence of tiles starting from the given row and column.
            A sequence is considered continuous if it contains only non-None tiles and is either in a row or a column.
            The method returns the number of points in the sequence, as well as the updated row_visited and col_visited lists.
            
            Args:
            - row: int, the row index of the starting tile
            - col: int, the column index of the starting tile
            - row_visited: list of int, the list of row indices that have already been visited in the current sequence
            - col_visited: list of int, the list of column indices that have already been visited in the current sequence
            
            Returns:
            - final_total: int, the number of points in the continuous sequence
            - row_visited: list of int, the updated row_visited list
            - col_visited: list of int, the updated col_visited list
            """
            orig_row = row
            orig_col = col
            points = set()
            in_row = False
            in_column = False
            #left
            while (self._map._get_tile(row,col-1) != None):
                if row in row_visited:
                    break
                in_row = True
                points.add((row,col-1))
                col = col -1
            col = orig_col
            #right
            while (self._map._get_tile(row,col+1) != None):
                if row in row_visited:
                    break
                in_row = True
                points.add((row,col+1))
                col = col + 1
            col = orig_col
            #up
            while (self._map._get_tile(row-1,col) != None):
                if col in col_visited:
                    break
                in_column = True
                points.add((row-1,col))
                row = row - 1
            row = orig_row
            #down
            while (self._map._get_tile(row+1,col) != None):
                if col in col_visited:
                    break
                in_column = True
                points.add((row+1,col))
                row = row + 1
            row = orig_row

            #adds the original tile for score calculation
            points.add((row,col))
            final_total = len(points)
            if in_row and in_column:
                final_total = final_total + 1
            if in_row:
                row_visited.append(row)
            if in_column:
                col_visited.append(col)
            #returns the number of points
            return final_total, row_visited, col_visited
    
    # Returns the number of points a tile earns for being a part of a Q sequence based on color
    def _q_score_color(self, row, col, tile: Tile):
            """
            Calculates the Q score for a given tile based on the number of unique colors in its row and column.

            Args:
                row (int): The row index of the tile.
                col (int): The column index of the tile.
                tile (Tile): The tile for which to calculate the Q score.

            Returns:
                int: The Q score for the given tile.
            """
            orig_col = col
            orig_row = row
            color_buffer = []
            points = 0
            #left
            color_buffer.append(tile.get_color())
            while (self._map._get_tile(row,col-1) != None):
                tile1 = self._map._get_tile(row, col-1)
                if tile1.get_color() not in color_buffer:
                    color_buffer.append(tile1.get_color())
                    col = col - 1
                else:
                    break
            col = orig_col
            #right
            while (self._map._get_tile(row,col+1) != None):
                tile1 = self._map._get_tile(row, col+1)
                if tile1.get_color() not in color_buffer:
                    color_buffer.append(tile1.get_color())
                    col = col + 1
                else:
                    break
            col = orig_col
            if len(color_buffer) == 6:
                points = points + 6
            #up
            while (self._map._get_tile(row-1,col) != None):
                tile1 = self._map._get_tile(row-1, col)
                if tile1.get_color() not in color_buffer:
                    color_buffer.append(tile1.get_color())
                    row = row - 1
                else:
                    break
            row = orig_row
            #down
            while (self._map._get_tile(row+1,col) != None):
                tile1 = self._map._get_tile(row + 1, col)
                if tile1.get_color() not in color_buffer:
                    color_buffer.append(tile1.get_color())
                    row = row + 1
                else:
                    break
            row = orig_row
            if len(color_buffer) == 6:
                points = points + self.q_score_bonus
            return points
    
    # Returns the number of points a tile earns for being a part of a Q sequence based on shape
    def _q_score_shape(self, row, col, tile: Tile):
            """
            Calculates the Q score for a given tile based on the number of unique shapes in its row, column, and surrounding tiles.

            Args:
                row (int): The row index of the tile.
                col (int): The column index of the tile.
                tile (Tile): The tile for which to calculate the Q score.

            Returns:
                int: The Q score for the given tile.
            """
            shape_buffer = []
            points = 0
            orig_col = col
            orig_row = row
            #left
            shape_buffer.append(tile.get_shape())
            while (self._map._get_tile(row,col-1) != None):
                tile1 = self._map._get_tile(row, col-1)
                if tile1.get_shape() not in shape_buffer:
                    shape_buffer.append(tile1.get_shape())
                    col = col - 1
                else:
                    break
            col = orig_col
            #right
            while (self._map._get_tile(row,col+1) != None):
                tile1 = self._map._get_tile(row, col+1)
                if tile1.get_shape() not in shape_buffer:
                    shape_buffer.append(tile1.get_shape())
                    col = col + 1
                else:
                    break
            col = orig_col
            if len(shape_buffer) == 6:
                points = points + 6
            #up
            while (self._map._get_tile(row-1,col) != None):
                tile1 = self._map._get_tile(row-1, col)
                if tile1.get_shape() not in shape_buffer:
                    shape_buffer.append(tile1.get_shape())
                    row -= 1
                else:
                    break
            row = orig_row
            #down
            while (self._map._get_tile(row+1,col) != None):
                tile1 = self._map._get_tile(row + 1, col)
                if tile1.get_shape() not in shape_buffer:
                    shape_buffer.append(tile1.get_shape())
                    row += 1
                else:
                    break
            row = orig_row
            if len(shape_buffer) == 6:
                points = points + self.q_score_bonus
            return points

  
    
    def check_placement_validity(self, row : int, col : int, tile : Map.Tile) -> bool:
        
        try: 
            valid_coord = self._map._valid_pos(tile)

            if (row, col) in valid_coord:
                return True
            else:
                return False
        except TypeError as e:
            raise TypeError("All inputs must be of correct type.") from e



    # Called when the active player wants to place a tile
    # the function checks the position of the tile that the player wants to place 
    # is a valid position and follows the rules of the Q game. If so, it places
    # the tile and if not, yet to implement(referee should end player turn and eliminate player) 
    def place_tile(self,x: int,y: int,tile):
        # while condition (allows the player to place multiple tiles until a stop signal): 
        # --- place holder values --- 


        # Checks the validity of the placement, assuming that the player gives a coordinate and a tile
        valid = self.check_placement_validity(x,y,tile)
        if valid:
            self._map._place_tile_given(x, y, tile)
            # Call a function that:
            # gives a random tile from the ref's stack to the current player
            # 0. Generate a random index within 0, len(self._ref_tile) 
            # 1. Add the tile to the player 
            #    e.g. self._active_player.add_tile(tile)
            # 2. Remove the tile from the referee's stack 
            #    e.g. [self._ref_tiles.remove(tile)]
        pass

    # Returns the tile at the given coordinate
    def _get_tile(self, row: int, col:int):
        return self._map._get_tile(row,col)


    # Renders the current state of the game
    def render_state(self):
        # Initialize Pygame
        pygame.init()
        # Set up the window
        window_size = (800, 600)
        screen = pygame.display.set_mode(window_size)
        screen.fill("white")
        pygame.display.set_caption("The Q Game")

        # Draw the player scores
        self._draw_scores(screen)

        # Draw the remaining tiles of the referee
        self._draw_referee_tiles(screen)

        # Draw the game map
        self._draw_map(screen)

        # Update the window
        pygame.display.flip()

        # Wait for the user to close the window
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

    # Draws the map of the game
    def _draw_map(self, screen):
        map_width = len(self._map.map[0])
        map_height = len(self._map.map)
        tile_size = 50
        window_width = 800
        window_height = 600
        map_x = (window_width - map_width * tile_size) / 2
        map_y = ((window_height - len(self._players) * 40) - map_height * tile_size) / 2 + len(self._players) * 40 # adjust the y position to leave space for scores and referee tiles
        for row in range(map_height):
            for col in range(map_width):
                tile = self._get_tile(row,col)
                if tile is not None:
                    tile_color = tile.get_color()
                    tile_shape = tile.get_shape()
                    ShapeRenderer.ShapeRenderer.return_file(tile_shape,tile_color)
                    tile_rect = pygame.image.load('file.png')
                    tile_x = map_x + col * tile_size
                    tile_y = map_y + row * tile_size
                    screen.blit(tile_rect, (tile_x, tile_y))

    # Draws the scores of the players
    def _draw_scores(self, screen):
        font = pygame.font.Font(None, 24)
        score_text = "Scores:"
        order_text = "Order:"
        order = font.render(order_text, True, (0, 0, 0))
        screen.blit(order, (10, 10))
        score = font.render(score_text, True, (0, 0, 0))
        screen.blit(score, (90, 10))
        for i, player in enumerate(self._players):
            score_text = f"Player {player.get_id()}:       {player.get_score()}"
            score_surface = font.render(score_text, True, (0, 0, 0))
            screen.blit(score_surface, (10, 10 + (i + 1) * 40))

    # Draws the remaining tiles of the referee
    def _draw_referee_tiles(self, screen):
        font = pygame.font.Font(None, 24)
        ref_tiles_text = f"Referee tiles: {len(self._ref_tiles)} tiles left"
        ref_tiles_surface = font.render(ref_tiles_text, True, (0, 0, 0))
        screen.blit(ref_tiles_surface, (600, 10 + len(self._players))) # adjust the y position to leave space for scores

"""
    def main():
        game_state1 = game_state()
        game_state1.add_player(Player.Player(1, 10))
        game_state1.add_player(Player.Player(2, 8))
        game_state1.add_player(Player.Player(3, 20))
        game_state1.add_player(Player.Player(4, 9))
        game_state1._sort_by_age()
        game_state1._active_player=game_state1.get_players()[0]
        tile1 = Tile("square","red")
        tile2 = Tile("square","blue")
        tile3 = Tile("square","green")
        tile4 = Tile("star","purple")
        game_state1._place_tile(2,1,tile1)
        game_state1._place_tile(3,1,tile2)
        game_state1._place_tile(3,2,tile3)
        game_state1._place_tile(1,0,tile4)
        game_state1._print_map()
        game_state1.render_state()



game_state.main()"""