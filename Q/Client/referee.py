import json

from Q.Client.client import ClientFactory
from Q.Player.player import Player
from Q.Player.player_funcs import PlayerFuncs
from Q.Util.util import Util


class ProxyRef:
    """
    Represents the proxy ref
    """
    def __init__(self, factory: ClientFactory, player: Player):
        self.fac = factory
        self.c = factory.protocol
        self.player = player
        #self.listen()

    def listen(self):
        while True:
            data = self.c.get_data()
            #print(data)
            if data is None:
                pass
            else:
                print(data)
                func = data[0]
                args = data[1]
                if func == PlayerFuncs.WIN.value:
                    self.call_win(args)
                    self.c.send_data('void')
                if func == PlayerFuncs.SETUP.value:
                    self.call_setup(args)
                    self.c.send_data('void')
                if func == PlayerFuncs.TAKE_TURN.value:
                    val = self.call_take_turn(args)
                    self.c.send_data(val)
                if func == PlayerFuncs.NEW_TILES.value:
                    self.call_new_tiles(args)
                    self.c.send_data('void')

    def call_take_turn(self, args) :
        ps = json.loads(args[0])
        return self.player.take_turn(ps)

    def call_new_tiles(self, args):
        tiles = json.loads(args[0])
        converted_tiles = Util().convert_jtiles_to_tiles(tiles)
        self.player.newTiles(converted_tiles)


    def call_setup(self, args):
        ps = json.loads(args[0])
        tiles = json.loads(args[1])
        Util().convert_jpub_json_to_game_state(ps)
        Util().convert_jtiles_to_tiles(tiles)
        self.player.setup(ps, tiles)

    def call_win(self, args):
        b = args[0]
        self.player.win(b)

