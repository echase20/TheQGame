from typing import List

from Q.Common.Board.tile import Tile
from Q.Common.game_state import GameState
from Q.Common.map import Map
from Q.Common.player_game_state import PlayerGameState
from Q.Common.rulebook import Rulebook
from Q.Player.in_housep_player import InHousePlayer
from Q.Player.player import Player
from Q.Player.turn import Turn
from Q.Referee.referee import Referee


class RefereeConfig(Referee):
    def __init__(self, state: GameState, turn_time: int, observer=None):
        self.state = state
        self.turn_time = turn_time
        super.__init__(observer)

    def main(self, player_list: List[Player]) -> List[List[str]]:
        return self.start_from_state(player_list, self.state)

    def player_action(self, func, args, current_player: Player, game_state: GameState, player_list: List[Player]):
        return super().player_action(func,args,current_player,game_state,player_list)

    def player_func(self, func, args, current_player: Player, game_state: GameState, player_list: List[Player]):
        return super().player_action(func,args,current_player,game_state,player_list)

    def run_game(self, game_state: GameState, player_list: List[Player]) -> List[List[str]]:
        pass

    def pair_results(self, game_state: GameState) -> List[List[str]]:
        return super().pair_results(game_state)

    def is_game_over(self, game_state: GameState, players: List[Player]):
        return super().is_game_over(game_state,players)

    def send_results(self, players_left: List[Player], game_state):
        pass

    def send_player_tiles(self, new_tiles: List[Tile], player: Player, game_state: GameState, player_list: [InHousePlayer]):
        pass

    def is_valid_move(self, turn: Turn, rulebook: Rulebook, given_map: Map, current_player: PlayerGameState,
                      num_of_ref_tiles: int):
        return super().is_valid_move(turn, rulebook, given_map, current_player, num_of_ref_tiles)

    def start_from_state(self, player_list: List[Player], game_state: GameState) -> List[List[str]]:
        return super().start_from_state(player_list, game_state)

    def signup_players(self, player_list: List[Player], game_state: GameState):
        super().signup_players(player_list,game_state)

    def setup_players(self, player_list: List[Player], game_state: GameState):
        pass

    def remove_current_player(self, game_state: GameState, current_player: Player, player_list: [Player]):
        super().remove_current_player(game_state,current_player,player_list)