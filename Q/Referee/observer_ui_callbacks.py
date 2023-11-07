

class ObserverUICallback():

    def next(self, next_state: int):
        pass

    def previous(self, prev_state: int):
        pass

    def save_jstate(self, current_state: int):
        pass

    def isNext(self, current_state: int):
        pass

    def isPrevious(self, current_state: int):
        pass