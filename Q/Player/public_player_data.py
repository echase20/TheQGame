from dataclasses import dataclass
from typing import Dict

from Q.Common.map import Map

@dataclass
class PublicPlayerData:
    """
    Represents public information that the player can know about the game.
    num_ref_tiles: is the number of tiles the ref currently had
    current_map: the current map of this game
    score: is a mapping from name to number of player points
    """
    num_ref_tiles: int
    current_map: Map
    scores: Dict[str, int]

