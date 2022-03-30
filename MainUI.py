import tkinter as tk
from tkinter import ttk
from wordle_brain import WordleBrain


class Alphabet(tk.Canvas):
    def __init__(self, master):
        super().__init__(master=master)
        self.configure(width=350, height=400)
        self.alphabet_squares = {}
        keyboard = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']

        def create_squares(number_of_squares: int, keyboard_row_index: int, y1, y2):
            """creates squares and alphabet on the right of wordle squares

            :param number_of_squares: how many squares in a row to be constructed
            :param keyboard_row_index: which keyboard row to use
            :param y1: height coordinate
            :param y2: height coordinate #2
            :return: None
            """
            a = 0
            for i in range(0, 30 * number_of_squares, 30):
                key_of_keyboard = keyboard[keyboard_row_index][a]
                x1_cor = 20 + i
                x2_cor = 50 + i
                x = self.create_rectangle(x1_cor, y1, x2_cor, y2)

                z = self.create_text(((x1_cor + x2_cor) // 2, (y1 + y2) // 2), text=key_of_keyboard,
                                     font=('Georgia 20'))
                # print(x1_cor, x2_cor, self.coords(z))
                self.alphabet_squares[key_of_keyboard] = x
                a += 1

        create_squares(10, 0, 100, 150)
        create_squares(9, 1, 170, 220)
        create_squares(7, 2, 240, 290)
        self.grid(column=13, row=1, rowspan=3)



    def update_squares(self, text_version_alphabet: dict):
        print(text_version_alphabet)
        for char, color in text_version_alphabet.items():
            square_number: int = self.alphabet_squares[char]
            match color:

                case 'g':
                    self.itemconfig(square_number, fill='#669bbc')
                case 'y':
                    self.itemconfig(square_number, fill='#fdf0d5')
                case 'r':
                    self.itemconfig(square_number, fill='#780000')


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

        self.grid(column=1, row=1, rowspan=3, columnspan=11)

    def update_rectangles(self, guess: str, row_index: int, color_code: str):
        """Takes guess argument and changes rectangles in a row's text and colors;

        Args:
            guess (str): user guess input
            row_index (int): which row to modify? depends on guess-1
            color_code (str): from processGuess in WordleBrain class and is a string consisting of 'g' for green,
            'w' for white, 'y' yellow
        """
        print(color_code)
        for i, char in enumerate(guess):
            # calculation of where text should be
            rect_coords = self.coords(self.rectangle_list[row_index][i])
            x_coordinate_of_text = (rect_coords[0] + rect_coords[2]) // 2
            y_coordinate_of_text = (rect_coords[1] + rect_coords[3]) // 2

            # create text and set fill color of rectangles
            self.create_text((x_coordinate_of_text, y_coordinate_of_text), text=char, font=('Georgia 20'))
        for (j, chare) in enumerate(color_code):
            match chare:
                case "g":
                    self.itemconfig(self.rectangle_list[row_index][j], fill="#669bbc")
                case "y":
                    self.itemconfig(
                        self.rectangle_list[row_index][j], fill="#fdf0d5"
                    )
                case "r":
                    self.itemconfig(self.rectangle_list[row_index][j], fill="#780000")


# debug tool to get coordinates on event
def motion(event):
    x, y = event.x, event.y
    print("{}, {}".format(x, y))


class MainUI(tk.Tk):
    def __init__(self, debug=False, word=None):
        super().__init__()
        self.wb = WordleBrain()
        self.PLAYING = True
        self.PLAY_AGAIN = False
        self._row_index = 0  # can be replaced with self.wb.guesses-1
        if debug:
            self.wb.WORD=word
            print(self.wb.WORD)
        # configure the root window
        self.title("PyWordle")
        self.geometry("800x600")
        self.attributes("-fullscreen", False)
        # self.bind('<Button-1>', motion)

        label = ttk.Label(
            self,
            text='Red: letter not in word\nYellow: letter in word but wrong position\nBlue: letter in correct position',
            font=("Helvetica", 14))
        label.grid(column=13, row=4)
        # create wordle boxes
        self.rectangles = Rectangles(self)
        self.alphabet = Alphabet(self)
        # gather guess input
        self.word_input = tk.Entry(self)
        self.word_input.config(width=4, font='Georgia 40')
        self.word_input.focus_set()
        self.guess_submit = tk.Button(
            self, text="Submit guess", command=self.process_input
        )
        self.bind("<Return>", self.process_input)
        self.word_input.grid(column=5, row=4)
        self.guess_submit.grid(column=5, row=5)

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

        yes = tk.Button(pop_up_game_over, text="Yes", command=_yes)
        no = tk.Button(pop_up_game_over, text="No", command=_no)
        yes.grid(column=2, row=4)
        no.grid(column=2, row=5)

    def process_input(self, _=None):
        guess: str = self.word_input.get().lower()

        if len(guess) > 0:
            self.word_input.delete(0, tk.END)
            # print(guess)
            # print(self.wb.guesses)
            validity = self.wb.is_input_valid(guess)
            # print(self.wb.WORD)

            if validity == 1:
                color_code = self.wb.processGuess(guess)
                self.wb.updateAlphabet(guess, color_code)
                # print(color_code)
                self.rectangles.update_rectangles(
                    guess=guess, row_index=self._row_index, color_code=color_code
                )
                self.alphabet.update_squares(self.wb.dict_alphabet)
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
