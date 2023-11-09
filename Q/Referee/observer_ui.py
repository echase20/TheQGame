from tkinter import Tk, Label, Button

from PIL import ImageTk

from Q.Referee.next_states import nextState
from Q.Referee.observer_ui_callbacks import ObserverUICallback


class ObserverUI:

    def __init__(self, callback: ObserverUICallback):
        self.current_state = 0
        self.callback = callback

        self.root = Tk()
        self.root.geometry("800x600")
        img = ImageTk.PhotoImage(file="../../8/tmp/0.png")
        #imgTk = PhotoImage(img)
        self.board = Label(self.root, image=img)
        self.board.photo = img
        self.board.grid(row=1)
        self.next_button = Button(text="Next", command=self.switch_next)
        self.next_button.grid(row=0, column=0)
        self.previous_button = Button(text="Previous", command=self.switch_prev)
        self.previous_button.grid(row=0, column=1)
        self.save_button = Button(text="Save", command=callback.save_jstate).grid(row=0, column=2)



    def receive_new_image(self, filename: str):
        img = ImageTk.PhotoImage(file="../../8/tmp/" + filename)
        img.photo = img
        #imgTk = PhotoImage(img)
        self.board.configure(image=img)

    def switch_prev(self):
        prev_button_state = self.callback.isPrevious(self.current_state)
        if prev_button_state == nextState.END:
            self.previous_button.configure(state="disabled")
        if prev_button_state == nextState.AVAILABLE:
            self.current_state -= 1
            self.callback.switch(self.current_state)

    def switch_next(self):
        next_button_state = self.callback.isNext(self.current_state)
        if next_button_state == nextState.AVAILABLE:
            self.current_state += 1
            self.callback.switch(self.current_state)
        if next_button_state == nextState.END:
            self.next_button.configure(state="disabled")

    def runUI(self):
        self.root.mainloop()
