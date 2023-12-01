from dataclasses import dataclass


@dataclass
class RefereeStateConfig:
    q_score: int
    end_game_bonus: int