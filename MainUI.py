import tkinter as tk
from wordle_brain import WordleBrain



class Rectangles(tk.Canvas):
    def __init__(self, master):
        super().__init__(master=master)
        self.configure(width=400, height=400)

        horizontal_gap = 5
        self.rectangle_list = []
        for j in range(0, 50 * 6, 50):
            current_row = []
            for i in range(0, 45 * 5, 45 + horizontal_gap):
                current_row.append(self.create_rectangle(45 + i, 45 + j, 90 + i, 90 + j))
            self.rectangle_list.append(current_row)
        self.place(relx=0.5, rely=0.35, anchor="center")

    def update_rectangles(self, guess: str, row_index: int, color_code: str):
        for i, char in enumerate(guess):
            rect_coords = self.coords(self.rectangle_list[row_index][i])
            x_coordinate_of_text = (rect_coords[0] + rect_coords[2]) // 2
            y_coordinate_of_text = (rect_coords[1] + rect_coords[3]) // 2

            self.create_text((x_coordinate_of_text, y_coordinate_of_text), text=char)
            for i, char, in enumerate(color_code):
                match char:
                    case 'g':
                        self.itemconfig(self.rectangle_list[row_index][i], fill='green')
                    case 'y':
                        self.itemconfig(self.rectangle_list[row_index][i], fill='yellow')
                    case 'w':
                        self.itemconfig(self.rectangle_list[row_index][i], fill='white')


def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))


class MainUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wb = WordleBrain()
        self.PLAYING = True
        self.PLAY_AGAIN = False
        self._row_index = 0

        self.guesses_arr = []
        # configure the root window
        self.title("PyWordle")
        self.geometry('1000x600')
        self.attributes('-fullscreen', False)
        # self.bind('<Button-1>', motion)

        # create wordle boxes
        self.rectangles = Rectangles(self)

        # gather guess input
        self.word_input = tk.Entry(self)
        self.guess_submit = tk.Button(self, text="Submit guess", command=self.process_input)
        self.bind('<Return>', self.process_input)
        self.word_input.pack()
        self.guess_submit.pack()
        self.mainloop()

    def pop_up(self, error_message):
        message = tk.Toplevel(self)
        message.geometry('200x200')
        message.title("Invalid Input")
        tk.Label(message, text=error_message, ).pack()
        message.after(1000, lambda: message.destroy())

    def game_over(self, user_won: bool):
        pop_up_game_over = tk.Toplevel(self)
        pop_up_game_over.geometry('300x300')
        pop_up_game_over.title('Game Over!')
        if user_won:
            tk.Label(pop_up_game_over, text=f'Game over! You got the word in {self.wb.guesses} guesses!').pack()
        else:
            tk.Label(pop_up_game_over, text=f"You absolute dumbass loser. The word was {self.wb.WORD}").pack()

        tk.Label(pop_up_game_over,
                 text="y = play again. n = stop").pack()
        play_again = tk.Entry(pop_up_game_over)
        play_again.pack()

        def play_again_thing(e=None):
            yorn = play_again.get()
            match yorn:
                case 'y':
                    # print('hehheheha')
                    self.PLAY_AGAIN = True
                    self.destroy()
                case 'n':
                    # print('nononono')
                    self.PLAYING = False
                    self.destroy()

        pop_up_game_over.bind("<Return>", play_again_thing)

        pass

    def process_input(self, _=None):
        guess: str = self.word_input.get()
        self.word_input.delete(0, tk.END)
        # print(guess)
        # print(self.wb.guesses)
        validity = self.wb.is_input_valid(guess)
        # print(self.wb.WORD)

        if validity == 1:
            self.guesses_arr.append([char for char in guess])
            color_code = self.wb.processGuess(guess)
            # print(color_code)
            self.rectangles.update_rectangles(guess=guess, row_index=self._row_index, color_code=color_code)
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
