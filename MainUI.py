import tkinter as tk

class Rectangles(tk.Canvas):
    def __init__(self):
        super().__init__()
        for i in range(0, 45*5, 45):
        
          self.create_rectangle(40+i,40+i,100+i,100+it,outline="black")
          self.pack()
        
class MainUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title("PyWordle")
        self.geometry('500x500')
        self.rectangles = Rectangles()

        self.mainloop()
