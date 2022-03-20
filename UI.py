import tkinter as tk


class UI(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title("PyWordle")
        self.geometry('500x500')

