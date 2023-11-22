from abc import ABC, abstractmethod
from typing import Dict


class Callback(ABC):
    @abstractmethod
    def start_game(self,names: Dict):
        pass