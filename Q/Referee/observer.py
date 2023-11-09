import json
from typing import List

from Q.Common.game_state import GameState
from Q.Common.render import Render
from Q.Referee.observer_ui import ObserverUI
from Q.Referee.observer_ui_callbacks import ObserverUICallback
from Q.Util.util import Util
import pathlib


class Observer(ObserverUICallback):
    """
    Represents a game observer of the Q Game
    """

    def __init__(self):
        self.states: List[GameState] = []
        self.image_name_counter = 0
        self.observer_ui = ObserverUI(self)

    def save_states(self, state):
        """
        saves multiple states to the directory tmp/x.png where x is a sequential number starting at 0.
        :param states: the states that we will save
        :EFFECT updates the image name counter
        """
        public_data = state.extract_public_player_data()
        img = Render(public_data)
        curr_dir = pathlib.Path(__file__).parent.resolve()
        img.save(str(curr_dir) + "/../../8/tmp/" + str(self.image_name_counter) + ".png")
        self.image_name_counter += 1

    def receive_a_state(self, state: GameState):
        """
        receives a particular state
        :param state: the given state to be saved
        """
        self.states.append(state)
        self.save_states(state)

    def receive_a_game_over(self):
        """
        receives a notification that the game is over
        """
        self.start_ui()

    def switch(self, state: int):
        """
        goes to the previous state
        """
        self.observer_ui.receive_new_image(f"{str(state)}.png")

    def save_jstate(self, current_state: int, filepath: str):
        out_file = open(filepath, "w")
        jstate = Util().convert_gamestate_to_jstate(self.states[current_state])
        json.dump(jstate, out_file)
        out_file.close()

    def hasState(self, current_state: int) -> bool:
        return 0 <= current_state < len(self.states)

    def start_ui(self):
        self.observer_ui.runUI()
