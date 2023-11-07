from typing import List, Deque

from Q.Common.game_state import GameState
from Q.Common.render import Render
from collections import deque
from Q.Player.public_player_data import PublicPlayerData
from Q.Referee.next_states import nextState
from Q.Referee.observer_ui import ObserverUI
from Q.Referee.observer_ui_callbacks import ObserverUICallback
from Q.Util.util import Util


class Observer(ObserverUICallback):
    """
    Represents a game observer of the Q Game
    """

    def __init__(self):
        self.states: List["GameState"] = []
        self.is_game_over = False
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
        img.save("tmp/" + str(self.image_name_counter))
        self.image_name_counter += 1

    def receive_a_state(self, state: GameState):
        """
        receives a particular state
        :param state: the given state to be saved
        """
        self.states.append(state)
        self.save_states(state)
    def receive_a_game_over_func(self, game_over: bool):
        """
        receives a notification that the game is over
        :param game_over: true if the game is over false otherwise
        """
        self.is_game_over = game_over

    def state_to_img(self, state: GameState):
        public_data = state.extract_public_player_data()
        img = Render(public_data)
        return img

    def next(self, next_state: int):
        """
        goes to the next state
        """
        img = self.state_to_img(self.states[next_state])
        self.observer_ui.receive_new_image(img)
    def previous(self, prev_state: int):
        """
        goes to the previous state
        """
        img = self.state_to_img(self.states[prev_state])
        self.observer_ui.receive_new_image(img)
    def save_jstate(self, current_state: int):
        Util.convert_state_to_jstate(self.states[current_state])

    def isNext(self, current_state: int) -> nextState:
        if (current_state == len(self.states) - 1) and self.is_game_over:
            return nextState.END
        if current_state == len(self.states) - 1:
            return nextState.WAITING
        return nextState.AVAILABLE
    def isPrevious(self, current_state: int) -> nextState:
        return nextState.AVAILABLE if current_state != 0 else nextState.END


