import tkinter as tk

class Rectangles(tk.Canvas):
    def __init__(self):
        super().__init__()

        self.create_rectangle(0,0,100,100,outline="black")
        self.pack()
        
class MainUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title("PyWordle")
        self.geometry('500x500')
        self.rectangles = Rectangles()

        self.mainloop()
