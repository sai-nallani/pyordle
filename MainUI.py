from ast import Pass
import tkinter as tk
from wordle_brain import WordleBrain


class Alphabet(tk.Canvas):
    def __init__(self, master):
        super().__init__(master=master)
        self.configure(width=350, height=400)
        print('initialized alphabet')
        self.alphabet_squares = []
        keyboard = ['qwertyuiop','asdfghjkl','zxcvbnm']
        a=0

        for i in range(0, 30*10,30):
            row = []
            print(i)
            x1_cor = 20+i
            x2_cor = 50+1
            y1_cor = 100
            y2_cor = 150
            x = self.create_rectangle(x1_cor,y1_cor,x2_cor,y2_cor)
            
            self.create_text(((x1_cor+x2_cor)//2,(y1_cor+y2_cor)//2), text=keyboard[0][a])
            a+=1
            row.append(x)
        self.alphabet_squares.append(row)
        a=0
        for i in range(0, 30*9,30):
            row = []
            x1_cor = 20+i
            x2_cor = 50+1
            y1_cor = 160
            y2_cor = 210
            x = self.create_rectangle(x1_cor,y1_cor,x2_cor,y2_cor)
            
            txt = self.create_text(((x1_cor+x2_cor)//2,(y1_cor+y2_cor)//2), text=keyboard[1][a])
            a+=1
            row.append(x)
        self.alphabet_squares.append(row)
        a=0
        for i in range(0, 30*7,30):
            row = []
            x1_cor = 20+i
            x2_cor = 50+1
            y1_cor = 220
            y2_cor = 270
            x = self.create_rectangle(x1_cor,y1_cor,x2_cor,y2_cor)
            
            txt = self.create_text(((x1_cor+x2_cor)//2,(y1_cor+y2_cor)//2), text=keyboard[2][a])
            a+=1
            row.append(x)
        self.alphabet_squares.append(row)
        self.grid(column=1, row=2)

class Rectangles(tk.Canvas):
    """initializes and updates the wordle boxes!

    Args:
        tk (Canvas): master
    """

    def __init__(self, master):
        super().__init__(master=master)
        self.configure(width=400, height=400)

        horizontal_gap = 5
        self.rectangle_list = []

        # creates rectangles, and appends to rectangle list so it is accessible
        for j in range(0, 50 * 6, 50):
            current_row = []
            for i in range(0, 45 * 5, 45 + horizontal_gap):
                current_row.append(
                    self.create_rectangle(45 + i, 45 + j, 90 + i, 90 + j)
                )
            self.rectangle_list.append(current_row)

        self.grid(column=3, row=2)
        
    def update_rectangles(self, guess: str, row_index: int, color_code: str):
        """Takes guess argument and changes rectangles in a row's text and colors;

        Args:
            guess (str): user guess input
            row_index (int): which row to modify? depends on guess-1
            color_code (str): from processGuess in WordleBrain class and is a string consisting of 'g' for green,
            'w' for white, 'y' yellow
        """
        for i, char in enumerate(guess):
            # calculation of where text should be
            rect_coords = self.coords(self.rectangle_list[row_index][i])
            x_coordinate_of_text = (rect_coords[0] + rect_coords[2]) // 2
            y_coordinate_of_text = (rect_coords[1] + rect_coords[3]) // 2

            # create text and set fill color of rectangles
            self.create_text((x_coordinate_of_text, y_coordinate_of_text), text=char)
            for (
                i,
                char,
            ) in enumerate(color_code):
                match char:
                    case "g":
                        self.itemconfig(self.rectangle_list[row_index][i], fill="green")
                    case "y":
                        self.itemconfig(
                            self.rectangle_list[row_index][i], fill="yellow"
                        )
                    case "w":
                        self.itemconfig(self.rectangle_list[row_index][i], fill="white")


# debug tool to get coordinates on event
def motion(event):
    x, y = event.x, event.y
    print("{}, {}".format(x, y))


class MainUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wb = WordleBrain()
        self.PLAYING = True
        self.PLAY_AGAIN = False
        self._row_index = 0  # can be replaced with self.wb.guesses-1

        # configure the root window
        self.title("PyWordle")
        self.geometry("1000x600")
        self.attributes("-fullscreen", False)
        self.bind('<Button-1>', motion)

        # create wordle boxes
        self.rectangles = Rectangles(self)
        self.alphabet = Alphabet(self)
        # gather guess input
        self.word_input = tk.Entry(self)
        self.guess_submit = tk.Button(
            self, text="Submit guess", command=self.process_input
        )
        self.bind("<Return>", self.process_input)
        self.word_input.grid(column=3, row=4)
        self.guess_submit.grid(column=3, row=5)

        self.mainloop()

    def pop_up(self, error_message: str):
        """pop up when an invalid guess has occured

        Args:
            error_message (str): error message to show on pop up
        """
        message = tk.Toplevel(self)
        message.geometry("200x200")
        message.title("Invalid Input")
        
        tk.Label(
            message,
            text=error_message,
        ).grid(column=1, row=2)
        message.after(1000, lambda: message.destroy())

    def game_over(self, user_won: bool):
        """shows results when game is over and asks if user wants to play again

        Args:
            user_won (bool): did user win?
        """
        # quick setup of popup
        pop_up_game_over = tk.Toplevel(self)
        pop_up_game_over.geometry("300x300")
        pop_up_game_over.title("Game Over!")
        pop_up_game_over.focus_set()
        if user_won:
            tk.Label(
                pop_up_game_over,
                text=f"Game over! You got the word in {self.wb.guesses} guesses!",
            ).grid(column=1, row=2)
        else:
            tk.Label(
                pop_up_game_over,
                text=f"You absolute dumbass loser. The word was {self.wb.WORD}",
            ).grid(column=1, row=2)

        # ask user if they want to play again
        tk.Label(pop_up_game_over, text="y = play again. n = stop").grid(column=1, row=4)

        def _yes(e=None):
            self.PLAY_AGAIN = True
            self.destroy()
        def _no(e=None):
            self.PLAY_AGAIN = False
            self.destroy()
            
        yes = tk.Button(pop_up_game_over,text="Yes", command=_yes)
        no = tk.Button(pop_up_game_over, text="No", command=_no)
        yes.grid(column=2,row=4)
        no.grid(column=2,row=5)

    def process_input(self, _=None):
        guess: str = self.word_input.get()
        self.word_input.delete(0, tk.END)
        # print(guess)
        # print(self.wb.guesses)
        validity = self.wb.is_input_valid(guess)
        # print(self.wb.WORD)

        if validity == 1:
            color_code = self.wb.processGuess(guess)
            # print(color_code)
            self.rectangles.update_rectangles(
                guess=guess, row_index=self._row_index, color_code=color_code
            )
            self._row_index += 1
            if guess == self.wb.WORD:
                self.game_over(True)

        else:
            match validity:
                case 0:
                    self.pop_up("Guess not in word list")
                case -1:
                    self.pop_up(f"Guess not {len(self.wb.WORD)} letters")
        if self.wb.guesses > 6:
            self.game_over(False)
