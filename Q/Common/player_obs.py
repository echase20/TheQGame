"""
PLAYER DATA REPRESENTATION

The player class represents an object storing the necessary data a game state keeps track of. It is not
a real player that interacts with the game itself.

The Player class keeps track of the following data, all accessible by the game state by get_info():
    1. id:      The unique player id, in integer, of a player.
    2. age:     The age of the player.
    3. score:   The current score of the player.
    4. tiles:   The current list of tiles (Tile object) owned by the player.

At initialization, the score of the player will be set to 0 and the list of tiles will be empty.

"""
class Player:
    def __init__(self, player_id : int, age : int):
        self._id = player_id
        self. _age = age
        self._score = 0
        self._tiles = []

    # Returns the player's information as a dictionary
    def get_info(self):
        player_info = {"id": self._id,
                       "age": self._age,
                       "score": self._score,
                       "tiles": self._tiles}
        return player_info
    #test
    # Return the id of the player
    def get_id(self):
        return self._id
    def get_score(self):
        return self._score
    # Add a tile to the player's list of tiles
    def add_tile(self, tile):
        self._tiles.append(tile)

    # Remove a tile from the player's list of tiles
    def remove_tile(self, tile):
        self._tiles.remove(tile)

    # Add points number of points to the player's current score
    def add_score(self, points):
        self._score += points