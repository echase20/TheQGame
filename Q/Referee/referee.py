from copy import deepcopy
from typing import List, Set, Dict

from Q.Common.Board.tile import Tile
from Q.Common.map import Map
from Q.Common.player_game_state import PlayerGameState
from Q.Common.rulebook import Rulebook
from Q.Player.player import Player
from Q.Player.turn import Turn
from Q.Player.turn_outcome import TurnOutcome
from Q.Referee.pair_results import Results
from Q.Player.in_housep_player import InHousePlayer
from Q.Common.game_state import GameState


class Referee:
    """
    Anytime a player API function, take-turn, win, setup, new-tiles, throws an error, we remove this player from the game.
    We plan to add implementation for timeouts when there is more clarity
    Represents a referee for the Q game
    """
    def __init__(self, observer = None):
        self.observer = observer

    def main(self, player_list: List[Player]) -> Results:
        """
        executes the Q game for a given list of players
        :param player_list: list of players that will play the game
        :return winners and kicked players
        """
        game_state = GameState()
        game_state.setup_state()
        Referee.signup_players(player_list, game_state)
        Referee.setup_players(player_list, game_state)

        return self.run_game(game_state, player_list)

    def run_game(self, game_state: GameState, player_list: List[Player]) -> Results:
        """
        Runs the given game state to completion
        :param player_list: the list of players of the game
        :param game_state: the given game state to run the game on
        :return: winners and kicked players
        """
        if self.observer: self.observer.receive_a_state(deepcopy(game_state))
        while not Referee.is_game_over(game_state, player_list):
            current_player = player_list.pop(0)
            player_list.append(current_player)
            player_name = current_player.name()
            pub_data = game_state.extract_player_state(player_name)
            try:
                turn = current_player.take_turn(pub_data)
            except Exception as E:
                Referee.remove_current_player(game_state, current_player, player_list)
                continue
            if not Referee.is_valid_move(turn, game_state.rulebook, deepcopy(game_state.map), game_state.players[player_name], pub_data.num_ref_tiles):
                Referee.remove_current_player(game_state, current_player, player_list)
            else:
                players_old_hand = len(game_state.players[player_name].hand)
                game_state.process_turn(turn, player_name)
                if players_old_hand == len(turn.placements):
                    break
                game_state.draw_tiles_for_player(player_name)
                new_tiles = game_state.players[player_name].hand
                Referee.send_player_tiles(new_tiles, current_player, game_state, player_list)
            if self.observer: self.observer.receive_a_state(deepcopy(game_state))
        if self.observer: self.observer.receive_a_game_over()
        Referee.send_results(player_list, game_state)
        return game_state.return_pair_of_results()

    @staticmethod
    def is_game_over(game_state: GameState, players: List[Player]):
        """
        is the game over according to the referee
        :param game_state: the game state of which may be over
        :param players: the players in the game
        :return: true if the game is over
        """
        return not players or game_state.played_all_tiles() or game_state.has_all_passed_or_exchanged_for_a_round()

    @staticmethod
    def send_results(players_left: List[Player], game_state):
        """
        sends the results of the game to the respective player who are winners and losers
        :param players_left: the players left in the game
        :param winner_names: the names of the winners of the game
        :param game_state: the current game state
        """
        results = game_state.return_pair_of_results()
        for name in results.winners:
            player = list(filter(lambda n: n.name() == name, players_left))[0]
            try:
                player.win(True)
            except:
                Referee.remove_current_player(game_state, player, players_left)
                Referee.send_results(players_left, game_state)
                return

        for name in results.losers:
            player = list(filter(lambda n: n.name() == name, players_left))[0]
            try:
                player.win(False)
            except:
                Referee.remove_current_player(game_state, player, players_left)

    @staticmethod
    def send_player_tiles(new_tiles: List[Tile], player: Player, game_state: GameState, player_list: [InHousePlayer]):
        """
        sends a player new tiles by calling the player new-tiles API function
        :param new_tiles: the new tiles the player will receive
        :param player: the player who you are sending the update to
        :param game_state: the current game state
        """
        if not new_tiles:
            return
        try:
            player.newTiles(new_tiles)
        except:
            Referee.remove_current_player(game_state, player, player_list)

    @staticmethod
    def is_valid_move(turn: Turn, rulebook: Rulebook, given_map: Map, current_player: PlayerGameState, num_of_ref_tiles: int):
        """
        is this a valid move according to the rulebook?
        :param turn: the turn the player wants to perform
        :param rulebook: the rules of the game
        :param given_map: the map tiles are placed on
        :param current_player: the player that is currently trying to place tiles
        :param num_of_ref_tiles: the num of ref tiles in the game
        :return: true if the turn is valid according to the rulebook else false
        """
        copy_hand = current_player.hand.copy()
        for tile in turn.placements.values():
            if tile not in copy_hand:
                return False
            copy_hand.remove(tile)

        if turn.turn_outcome == TurnOutcome.PLACED:
            return rulebook.valid_placements(given_map, turn.placements)
        if turn.turn_outcome == TurnOutcome.REPLACED:
            return rulebook.valid_replacement(num_of_ref_tiles, current_player.hand)
        return True

    def start_from_state(self, player_list: List[Player], game_state: GameState) -> Results:
        """
        Initializes players in at a particular given state
        :param player_list: the players in the game
        :param game_state: game state to copy the map from
        :return: winners and kicked players
        """
        Referee.setup_players(player_list, game_state)
        return self.run_game(game_state, player_list)

    @staticmethod
    def signup_players(player_list: List[Player], game_state: GameState):
        """
        Starts the game with the given players and some given game
        :param player_list: the players to be added to the game
        :param game_state: the game state where the players sign up to
        """
        copy_map = deepcopy(game_state.map)
        for player in player_list:
            hand = game_state.draw_tiles(6)
            player_game_state = PlayerGameState(hand, 0, False, TurnOutcome.PLACED)
            game_state.signup_player(player_game_state, player.name())
            try:
                player.setup(copy_map, hand)
            except:
                Referee.remove_current_player(game_state, player, player_list)

    @staticmethod
    def setup_players(player_list: List[Player], game_state: GameState):
        """
        setups the player by calling the setup API for each player
        :param player_list: the players to be setup
        :param game_state: the state of the game
        """
        for player in player_list:
            try:
                player.setup(game_state.map, game_state.players[player.name()].hand.copy())
            except:
                Referee.remove_current_player(game_state, player, player_list)

    @staticmethod
    def remove_current_player(game_state: GameState, current_player: Player, player_list: [Player]):
        """
        removes the current play from the gamestate
        NOTE: may need to call continue ofter this function to not add the player back to the queue
        :param current_player: the current player which is being removed
        :param player_list: the list of current players
        :param game_state: the game state of the game
        """
        current_player_game_state = game_state.players[current_player.name()]
        current_player_game_state.misbehaved = True

        hand = current_player_game_state.hand
        game_state.add_tiles_to_referee_deck(hand)
        player_list.remove(current_player)
