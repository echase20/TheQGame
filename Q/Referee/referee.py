import sys
sys.path.insert(1,'../Common')
import game_state as g
sys.path.insert(1,'../Player')
import player as p


"""
# Referee function
# Input: A list of players
# Output: List of names of the winners and List of names of the eliminated players

Abnormal Interactions Taken of Care:
- If a player tries to exchange with more tiles then the ref has left
- If a player tries to place a tile that it does not have
- If a player tries to place a tile out of bounds, on another tiles, or in an invalid spot, (ergo, any invalid move)
- If a player passes an to the referee something that is not one of pass, replace, or a list of actions
"""
def referee(players: list) -> (list, list):
    winners = []
    eliminated = []
    # Create a new game state
    game = g.game_state()
    game._players = players

    # Set up the Game with players
    for player in game._players:
        tiles = game.TileBag(6)
        game_map = game._map
        player.setup(game_map, tiles)

    game._active_player = game._players[0]

    all_tiles_placed = False
    player_placed_all_tiles = False
    # While there are still tiles in the bag
    while not (game._game_over() and all_tiles_placed and player_placed_all_tiles):
        pass_or_replace_count = 0
        for _ in range(len(game._players)):
            turn_action = game._active_player.takeTurn(game)
            if turn_action == "pass":
                game._rotate_players()
                pass_or_replace_count += 1
            if turn_action == "replace":
                #check that the ref has enough tiles to replace
                if len(game._active_player.bag_of_tiles) > game.ref_tiles_left():
                    eliminated.append(game._active_player.name)
                    game._players.remove(game._active_player)
                else:
                    game._active_player.newTiles(game._tile_bag(len(game._active_player.bag_of_tiles)))
                    game._rotate_players()          
                    pass_or_replace_count += 1
            if type(turn_action) == list:
                    hand_length = len(game._active_player.bag_of_tiles)
                    still_player = True
                    for tile in turn_action:
                        #check to see the player has the tiles it wishes to place
                        if tile[0] not in game._active_player.bag_of_tiles:
                            eliminated.append(game._active_player.name)
                            game._players.remove(game._active_player)
                            still_player = False
                            break
                        try:
                            # try to place the tile and removes that tile from the players hand if successful
                            game.place_tile(tile[1][0], tile[1][1], tile[0])
                            if len(game._active_player.bag_of_tiles) != 0:
                                game._active_player.bag_of_tiles.remove(tile[0])
                            else:
                                all_tiles_placed = True
                        except(TypeError):
                            eliminated.append(game._active_player.name)
                            game._players.remove(game._active_player)
                            still_player = False
                            break
                        # if the player completed a legal move, give them tiles back and score the action
                    if still_player:
                        if len(game._active_player.bag_of_tiles) == 0:
                            player_placed_all_tiles = True
                            break
                        if len(game._ref_tiles) < len(turn_action):
                            all_tiles_placed = True
                        else:
                            game._active_player.bag_of_tiles.extend(game.TileBag(len(turn_action)))
                            row_list = []
                            col_list = []
                            tile_list = []
                            for action in turn_action:
                                row_list.append(action[1][0])
                                col_list.append(action[1][1])
                                tile_list.append(action[0])
                            points = game._score_point(row_list,col_list,tile_list,hand_length)
                            game._active_player.score += points
                            game._rotate_players()
            else:
                raise TypeError("The given input is not of type: String.")
            if pass_or_replace_count == len(game._players):
                break
    score_list = []
    # find the winner at the end of the game based on score
    for player in game._players:
        score_list.append(player.score)
        winning_player_index = score_list.index(max(score_list))
    for i in range(len(players)):
        if i == winning_player_index:
            player.win(True)
            winners.append(players[i])
        else:
            player.win(False)
    return winners, eliminated
            





# Referee function
# Input: A list of players
# Output: List of names of the winners and List of names of the eliminated players

# The only diference with this function is that is takes in a premade game state for testing purposes

def referee(players: list, premade_game: g, tile_hands: list, player_scores: list) -> (list, list):
    winners = []
    eliminated = []
    # Create a new game state
    game = premade_game
    game._players = players
    # Set up the Game with players
    to_be_eliminated = []
    i = 0
    for player in game._players:
        game_map = game._map
        # If a bad player tries to set up, it will raise an exception
        try:
            player.setup(game_map, tile_hands[i], player_scores[i])
        except(Exception):
            eliminated.append(player.name)
            to_be_eliminated.append(player)
        i=i+1
    for player in to_be_eliminated:
        game._players.remove(player)
       
        

    game._active_player = game._players[0]
    all_tiles_placed = False
    player_placed_all_tiles = False
    # While there are still tiles in the bag
    while not (game._game_over() and all_tiles_placed and player_placed_all_tiles):
        pass_or_replace_count = 0
        for _ in range(len(game._players)):
            try:
                turn_action = game._active_player.takeTurn(game)
            except(Exception):
                eliminated.append(game._active_player.name)
                game._players.remove(game._active_player)
                game._rotate_players()
            if turn_action == "pass":
                game._rotate_players()
                pass_or_replace_count += 1
            elif turn_action == "replace":
                #check that the ref has enough tiles to replace
                if len(game._active_player.bag_of_tiles) > game.ref_tiles_left():
                    eliminated.append(game._active_player.name)
                    game._players.remove(game._active_player)
                    game._rotate_players()
                else:
                    try:
                        game._active_player.newTiles(game.TileBag(len(game._active_player.bag_of_tiles)))
                        game._rotate_players()          
                        pass_or_replace_count += 1
                    except(Exception):
                        eliminated.append(game._active_player.name)
                        game._players.remove(game._active_player)
                        game._rotate_players()
            elif type(turn_action) == list:
                    hand_length = len(game._active_player.bag_of_tiles)
                    still_player = True
                    for tile in turn_action:
                        #check to see the player has the tiles it wishes to place
                        if tile[0] not in game._active_player.bag_of_tiles:
                            eliminated.append(game._active_player.name)
                            game._players.remove(game._active_player)
                            game._rotate_players()
                            still_player = False
                            break
                        try:
                            # try to place the tile and removes that tile from the players hand if successful
                            game.place_tile(tile[1][0], tile[1][1], tile[0])
                            game._active_player.bag_of_tiles.remove(tile[0])
                            
                        except(TypeError):
                            eliminated.append(game._active_player.name)
                            game._players.remove(game._active_player)
                            game._rotate_players()
                            still_player = False
                            break
                        # if the player completed a legal move, give them tiles back and score the action
                    if still_player:
                        if len(game._active_player.bag_of_tiles) == 0:
                            player_placed_all_tiles = True
                        if len(game._ref_tiles) < len(turn_action):
                            game._active_player.bag_of_tiles.extend(game.TileBag(len(game._ref_tiles)))
                        else:
                            game._active_player.bag_of_tiles.extend(game.TileBag(len(turn_action)))
                        row_list = []
                        col_list = []
                        tile_list = []
                        for action in turn_action:
                            row_list.append(action[1][0])
                            col_list.append(action[1][1])
                            tile_list.append(action[0])
                        points = game._score_point(row_list,col_list,tile_list,hand_length)
                        game._active_player.score += points
                        game._rotate_players()
                        still_player = False
            else:
                raise TypeError("The given input is not of type: String.")
        if pass_or_replace_count == len(game._players):
            break
    score_list = []
    # find the winner at the end of the game based on score
    for player in game._players:
        score_list.append(player.score)
        winning_player_index = score_list.index(max(score_list))
    for i in range(len(players)):
        if i == winning_player_index:
            # If a bad player tries to win, it will raise an exception
            try:
                players[i].win(True)
                winners.append(players[i].name)
            except(Exception):
                eliminated.append(players[i].name)
                game._players.remove(game._players[i])
        else:
            try:
                players[i].win(False)
            except(Exception):
                eliminated.append(players[i].name)
                game._players.remove(game._players[i])
    return winners, eliminated