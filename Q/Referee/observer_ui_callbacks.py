

class ObserverUICallback():

    def switch(self, state: int):
        pass

    def save_jstate(self, current_state: int, filepath: str):
        pass

    def isNext(self, current_state: int):
        pass

    def isPrevious(self, current_state: int):
        pass