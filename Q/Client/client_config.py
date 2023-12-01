from typing import List

from Q.Player.player import Player


class ClientConfig:
    port: int
    host: str
    wait: int
    quiet: bool
    players: List[Player]