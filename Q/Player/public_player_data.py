from dataclasses import dataclass
from typing import List

from Q.Common.Board.tile import Tile


@dataclass
class PublicPlayerData:
    score = int
    name = str
    tiles = List[Tile]