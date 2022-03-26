import tkinter as tk
import time

class Rectangles(tk.Canvas):
    def __init__(self, master):
        super().__init__()
        self.configure(width=400, height=400)
        horizontal_gap = 5
        rectangle_list = []
        for j in range(0,50*6, 50):
          for i in range(0, 45*5, 45+horizontal_gap):
            self.create_rectangle(45+i, 45+j, 90+i, 90+j)

        self.place(relx=0.5, rely=0.35, anchor="center")
def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))


class MainUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # configure the root window
        self.title("PyWordle")
        self.geometry('1000x600')
        self.attributes('-fullscreen', False)
        self.bind('<Button-1>', motion)

        # create wordle boxes
        self.rectangles = Rectangles(self)


        self.mainloop()
