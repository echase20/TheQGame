import json
from collections import defaultdict
from typing import Set, Dict, List, Union

from Q.Common.player_game_state import PlayerGameState
from Q.Common.rulebook import Rulebook
from Q.Common.game_state import GameState
from Q.Common.Board.pos import Pos
from Q.Common.map import Map
from Q.Common.Board.tile import Tile
from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Player.cheat_player import CheatPlayer
from Q.Player.dag import Dag
from Q.Player.ldasg import LDasg
from Q.Player.strategy import PlayerStrategy
from Q.Player.player import Player
from Q.Player.public_player_data import PublicPlayerData
from Q.Player.turn_outcome import TurnOutcome
from Q.Player.mock_player import MockPlayer
from Q.Referee.pair_results import PairResults


class Util:
    """
    # Represents a utility class used mainly for json parsing
    """
    def pair_results_to_jresults(self, pair_results: PairResults):
        jwinners = sorted(list(pair_results.winners))
        jmisbehaved = sorted(list(pair_results.misbehaved))
        jresults = [jwinners, jmisbehaved]
        return jresults

    def jactors_to_players(self, jactors) -> List[Player]:
        players = []
        for jactorspec in jactors:
            jname = jactorspec[0]
            strategy = self.convert_jstrategy_to_strategy(jactorspec[1])
            if len(jactorspec) == 4:
                jcheat = jactorspec[3]
                players.append(CheatPlayer(name=jname, strategy=strategy, cheat=jcheat))
            if len(jactorspec) == 3:
                jexn = jactorspec[2]
                players.append(MockPlayer(name=jname, strategy=strategy, exn=jexn))
            else:
                players.append(Player(jname, strategy))
        return players

    def convert_jstate_to_gamestate(self, jstate):
        """
         { "map"      : JMap,

        "tile*"    : [JTile, ..., JTile],

        "players"  : [JPlayer, ..., JPlayer] }

        :param jstate:
        :return:
        """
        map = self.convert_json_to_map(jstate["map"])
        tiles = [self.json_to_tile(t) for t in jstate["tile*"]]
        game_state = GameState(given_map=map, tiles=tiles)
        return game_state

    def convert_jplayers_to_playergamestates(self, jplayers) -> List[PlayerGameState]:
        players = []
        for player in jplayers:
            score = player["score"]
            hand = [self.json_to_tile(t) for t in player["tile*"]]
            players.append(PlayerGameState(hand, score, False, None))
        return players


    def convert_single_turn_to_j_action(self, outcome: TurnOutcome, placement: Dict[Pos, Tile]):
        """
        converts a single turn to a jaction with the given outcome and given placement
        :param outcome the outcome of the turn
        :param placement: the placement
        :return: A j_action which is either pass, replace, or a 1Placement
        """
        if outcome == TurnOutcome.PASSED:
            return "pass"
        if outcome == TurnOutcome.REPLACED:
            return "replace"
        if outcome == TurnOutcome.PLACED:
            return self.convert_placement_to_jplacement(placement)

    def convert_placement_to_jplacement(self, placement: Dict[Pos, Tile]) -> dict:
        """
        convert placement to a jplacement of the given placement
        :param placement: the given placements to be converted to a jplacement
        :return the j_placement
        """
        if len(placement) != 1:
            raise Exception("Placements must be of length 1")
        pos = list(placement.keys())[0]
        tile = list(placement.values())[0]
        jpos = self.__create_json_pos(pos)
        jtile = self.convert_tile_to_json(tile)
        return {"coordinate": jpos, "1tile": jtile}

    def convert_jplacements_to_tiles(self, python_json) -> Dict[Pos, Tile]:
        """
        Converts jplacements to dict from pos to tile
        JPlacements is an array of the following shape:
        [{"coordinate": JCoordinate, "1tile": JTile}, ...]
        """
        pos_to_tile = {}
        for placement in python_json:
            pos = self.convert_coorindate_to_pos(placement["coordinate"])
            tile = self.json_to_tile(placement["1tile"])
            pos_to_tile[pos] = tile
        return pos_to_tile

    def convert_coorindate_to_pos(self, python_json) -> Pos:
        return Pos(python_json["column"], python_json["row"])

    def convert_jstrategy_to_strategy(self, strat_string: str) -> PlayerStrategy:
        """
        converts a string representation of a strategy to a player strategy
        :param strat_string the given strategy to be converted to a playerstrategy
        """
        if strat_string == "dag":
            return Dag()
        if strat_string == "ldasg":
            return LDasg()


    def convert_json_to_map(self, python_json: List[Union[int, List[Union[int, Dict[str, str]]]]]) -> Map:

        """
        Converts python_json from a list of json
        :param python_json: json that will be parsed into
        :return: a default dict from positions to their corresponding tiles
        """
        map_rep = defaultdict()
        for row in python_json:
            for i in range(1, len(row)):
                ci, tile = row[i]
                map_tile = Util.json_to_tile(tile)
                pos = Pos(x=ci, y=row[0])
                map_rep[pos] = map_tile
        return Map(config=map_rep)

    def convert_jpub_json_to_game_state(self, python_json) -> GameState:
        """
        JPub is an object with three fields:
        {
            "map": JMap,
            "tile*": Natural,
            "players": [JPlayer, Natural, ..., Natural]
        }
        We take this information and return a GameState object with it.
        """
        names = self.create_names(len(python_json["players"]))
        player_public_data = self.convert_player_json_to_player_public_data(python_json, names)
        game_state = GameState(config=player_public_data)
        return game_state

    def convert_game_state_to_false_or_j_map(self, game_state: GameState, tiles: [Pos, Tile]) -> str:
        """
        Returns expected output:
        The expected output is either false or the newly constructed JMap if the placement is legal.
        """
        try:
            game_state.place_tiles(tiles)
        except:
            return json.dumps(False)
        j_map = self.convert_map_to_jmap(game_state.map)
        return json.dumps(j_map)

    def convert_map_to_jmap(self, given_map: Map):
        """
        Converts map object into json readable JMap such as:
        [[row, [col, {"color":  color, "shape":  shape}], [col, {...}], ...], [row, [col, {...}, ...]]]
        """
        j_map_dict: [int, List[Dict[str, str]]] = defaultdict(list)
        for pos, tile in sorted(given_map.tiles.items(), key=lambda item: item[0].x):
            json_tile = self.convert_tile_to_json(tile)
            if pos.y not in j_map_dict:
                j_map_dict[pos.y] = []
            j_cells = j_map_dict.get(pos.y)
            j_cells.append([pos.x, json_tile])

        j_map = []
        for y, jcell in sorted(j_map_dict.items()):
            jcell.insert(0, y)
            j_map.append(jcell)

        return j_map

    def convert_player_json_to_player_public_data(self, python_json, names) -> PublicPlayerData:
        """
        converts player json to the public player data representation
        :param python_json: JSON representation of Q players
        :param names: All player names
        :return: Public information that the player can know about the game
        """
        map_board = self.convert_json_to_map(python_json["map"])
        referee_deck_length = python_json["tile*"]
        score = python_json["players"][0]["score"]
        other_points = python_json["players"][1:]
        other_points.insert(0, score)
        points = dict(zip(names, other_points))

        ppd = PublicPlayerData(referee_deck_length, map_board, points)
        return ppd

    def create_names(self, num_of_players: int):
        """
        Automatically creates player names
        :param num_of_players: Number of players to create names for
        """
        return [i for i in range(num_of_players)]

    @staticmethod
    def convert_jplayer_to_player(python_json, strategy: PlayerStrategy, name: str) -> Player:
        """
        Converts JSON representation of a player into an actual Q player
        :param python_json: JSON representation of a player
        :param strategy: Strategy to create player with
        :param name: Name of player to be created
        """
        player_tiles = [Util.json_to_tile(tile) for tile in python_json["tile*"]]
        return Player(name=name, strategy=strategy, hand=player_tiles)

    @staticmethod
    def write_legal_json_coordinates(given_map: Map, tile: Tile) -> str:
        """
        Determines legal moves for a tile and outputs the data as json formatted JCoordinates
        :param given_map: the map for where valid positions are to be searched
        :param tile: the tile which will be placed on the map
        :return: json of the valid JCoordinates
        """
        positions = Rulebook.get_legal_positions(given_map, tile)
        dict_positions = Util.__convert_positions_to_sorted_dicts(positions)
        return json.dumps(dict_positions)

    @staticmethod
    def json_to_tile(python_json_tile: Dict[str, str]) -> Tile:
        """
        Converts a json tile to an internal representation of a tile
        :param python_json_tile: the tile to be converted
        :return: Tile conversion result
        """
        color = TileColor.get_color_by_name(python_json_tile["color"])
        shape = TileShape.get_shape_by_name(python_json_tile["shape"])
        return Tile(shape, color)

    def convert_tile_to_json(self, tile: Tile) -> Dict[str, str]:
        """
        Converts internal representation of a tile to JSON representation
        """
        return {"color": tile.color.get_name(), "shape": tile.shape.get_name()}

    @staticmethod
    def __convert_positions_to_sorted_dicts(positions: Set[Pos]) -> List[Dict[str, int]]:
        """
        Converts given positions into row-column json coordinates
        :param positions: positions to be converted
        :return: the converted positions in json coordinate form
        """
        row_col_positions = sorted(positions, key=lambda pos: (pos.y, pos.x))
        positions = [Util.__create_json_pos(pos) for pos in row_col_positions]
        return positions

    @staticmethod
    def __create_json_pos(pos: Pos) -> Dict[str, int]:
        """
        Converts a pos into a dictionary pos
        :param pos: the pos that will be converted
        :return: the converted pos
        """
        return {"row": pos.y, "column": pos.x}
