import sys
import threading
import time

from jsonstream import loads
from Q.Client.client import Client
from Q.Client.referee import ProxyRef
from Q.Player.player import Player
from Q.Util.util import Util


def main():
    stream = loads(sys.stdin.read())
    config = Util().convert_j_client_config_to_client_config(next(stream))
    for player in config.players:
        if not config.quiet:
            print("Next Player")
        t = threading.Thread(target=create_player,args=[player, config.host])
        t.start()
        time.sleep(config.wait)


def create_player(player: Player, host: str):
    c = Client(player.name(), host, get_port())
    ProxyRef(c, player)


def get_port() -> int:
    try:
        return int(sys.argv[1])
    except Exception:
        raise Exception("no port number provided")


if __name__ == "__main__":
    main()
