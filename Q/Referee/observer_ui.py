from tkinter import Tk, ttk
from PIL import ImageTk, Image
from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from Q.Referee.next_states import nextState
from Q.Referee.observer_ui_callbacks import ObserverUICallback


class ObserverUI:

    def __init__(self, callback: ObserverUICallback):
        self.current_state = 0
        self.callback = callback

        app = QApplication([])
        window = QWidget()
        window.setWindowTitle("QVBoxLayout")

        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Top"))
        layout.addWidget(QPushButton("Center"))
        layout.addWidget(QPushButton("Bottom"))
        window.setLayout(layout)
        window.show()
        app.exec()
        """
        root = Tk()
        root.geometry("800x600")
        self.map = ttk.Label()
        self.map.grid(row=0)
        self.next_button = ttk.Button(text="Next", command=self.switch_next)
        self.next_button.grid(row=1, column=0)
        self.previous_button = ttk.Button(text="Previous", command=self.switch_prev)
        self.previous_button.grid(row=1, column=1)
        self.save_button = ttk.Button(text="Save", command=callback.save_jstate).grid(row=1, column=2)
        while True:
            root.update_idletasks()
            root.update()
        """

    def receive_new_image(self, img: Image):
        imgTk = ImageTk.PhotoImage(img)
        self.map = ttk.Label(imgTk)

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
        if next_button_state == nextState.WAITING:
            print("MORE STATES INCOMING")


