import sys
import time

from jsonstream import loads
from Q.Client.client import Client
from Q.Client.referee import ProxyRef
from Q.Util.util import Util


def main():
    stream = loads(sys.stdin.read())
    config = Util().convert_j_client_config_to_client_config(next(stream))
    for player in config.players:
        c = Client(player.name, config.host, get_port())
        ProxyRef(c, player)
        time.sleep(config.wait)


def get_port() -> int:
    try:
        return int(sys.argv[1])
    except Exception:
        raise Exception("no port number provided")


if __name__ == "__main__":
    main()
