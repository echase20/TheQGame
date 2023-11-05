from typing import Set
from dataclasses import dataclass


@dataclass
class PairResults:
    """
    Represents a pair of names of the winning player(s) and the names those players that misbehaved - from specs webpage
    """
    winners: Set[str]
    misbehaved: Set[str]
