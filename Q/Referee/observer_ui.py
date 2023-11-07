from tkinter import Tk, ttk
from PIL import ImageTk, Image

from Q.Referee.next_states import nextState
from Q.Referee.observer_ui_callbacks import ObserverUICallback


class ObserverUI:

    def __init__(self, callback: ObserverUICallback):
        self.current_state = 0
        self.callback = callback
        root = Tk()
        root.geometry("800x600")
        self.map = ttk.Label()
        self.map.grid(row=0)
        self.next_button = ttk.Button(text="Next", action=self.switch_next)
        self.next_button.grid(row=1, column=0)
        self.previous_button = ttk.Button(text="Previous", action=callback.previous).grid(row=1, column=1)
        self.save_button = ttk.Button(text="Save", action=callback.save_jstate).grid(row=1, column=2)
    def receive_new_image(self, img: Image):
        imgTk = ImageTk.PhotoImage(img)
        self.map = ttk.Label(imgTk)

    def switch_next(self):
        if self.callback.isNext(self.current_state) == nextState.AVAILABLE:
            self.current_state += 1
            self.callback.next(self.current_state)
        elif self.callback.isNext(self.current_state) == nextState.END:
            self.next_button.configure(state="disabled")

