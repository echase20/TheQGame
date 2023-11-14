import json

from Q.Player.player import Player
from Q.Player.player_funcs import PlayerFuncs
from Q.Referee.referee import Referee
from Q.Util.util import Util


class ProxyRef():
    """
    Represents the proxy ref
    """
    def __init__(self, client, player: Player):
        self.c = client
        self.player = player

    def listen(self):
        data = self.c.recive()
        if "msg looks like json we want":
            func = data[0]
            args = data[1]
            if func == PlayerFuncs.WIN.value:
                self.call_win(args)
            if func == PlayerFuncs.SETUP.value:
                self.call_setup(args)
            if func == PlayerFuncs.TAKE_TURN.value:
                val = self.call_take_turn(args)
                self.c.send(val)
            if func == PlayerFuncs.NEW_TILES.value:
                self.call_new_tiles(args)

    def call_take_turn(self, args):
        ps = json.loads(args[0])

        self.player.take_turn(ps)

    def call_new_tiles(self, args):
        tiles = json.loads(args[0])
        converted_tiles = Util.convert_jtiles_to_tiles(tiles)
        self.player.newTiles(converted_tiles)


    def call_setup(self, args):
        ps = json.loads(args[0])
        tiles = json.loads(args[1])
        # wrong
        Util().convert_jpub_json_to_game_state(ps)
        Util().convert_jtiles_to_tiles(tiles)
        self.player.setup(ps, tiles)

    def call_win(self, args):
        b = args[0]
        self.player.win(b)
