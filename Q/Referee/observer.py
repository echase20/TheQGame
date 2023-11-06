from typing import List, Deque

from Q.Common.game_state import GameState
from Q.Common.render import Render
from collections import deque
from Q.Player.public_player_data import PublicPlayerData
from Q.Util.util import Util


class Observer:
    """
    Represents a game observer of the Q Game
    """

    def __init__(self):
        self.states: Deque["GameState"] = deque()
        self.is_game_over = False
        self.image_name_counter = 0

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

    def next(self):
        """
        goes to the next state
        """
        state = self.states.popleft()
        self.states.append(state)

    def previous(self):
        """
        goes to the previous state
        """
        state = self.states.pop()
        self.states.append(state)

    def save_jstate(self):
        state = self.states.popleft()
        self.states.appendleft(state)
        Util.convert_state_to_jstate(state)



