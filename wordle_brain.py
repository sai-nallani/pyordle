from constants.acceptable_words import VALID_GUESSES
from constants.word_list import WORDS
import os
import random

try:
    from termcolor import colored
except ModuleNotFoundError:
    pass

clearConsole = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")


class WordleBrain:
    def __init__(self):
        # create random word

        self.WORD = random.choice(WORDS)
        self.alphabet = list("abcdefghijklmnopqrstuvwxyz")
        self.dict_alphabet = {i: 'w' for i in self.alphabet}
        self.guesses = 0

    # processes guess and sees if it is same as the word
    def processGuess(self, guessWord):
        clue = ""  # clue to see what letters are green, yellow, and red
        self.guesses += 1
        for i in range(len(self.WORD)):
            # if letters match up, add green to clue
            if self.WORD[i] == guessWord[i]:
                clue += "g"

            # if letter is in word, but don't match up
            elif guessWord[i] in self.WORD:
                should_add_yellow = True
                # check if another instance of the letter is found
                for j in range(i, len(guessWord)):
                    if guessWord.count(guessWord[i]) > self.WORD.count(guessWord[i]):

                        if j == i:
                            continue
                        if guessWord[j] == guessWord[i]:

                            should_add_yellow = False
                # add yellow or white to clue
                if should_add_yellow:
                    clue += "y"
                else:
                    clue += "z"
            # add white to clue
            else:
                clue += "z"

        return clue

    def updateAlphabet(self, guess, color_code):
        """
        used "upgrade" mechanic!
        upgrade mechanic is when the alphabet's color can only be upgraded, not downgraded.
        for example: yellow can only go to green, green can't be changed after in the dict
        :param guess: user guess
        :param color_code: color code with g y or z
        :return:
        """
        for i in range(len(guess)):
            letter = guess[i]
            color = color_code[i]
            current_color = self.dict_alphabet[letter]
            if current_color == 'g':
                continue
            elif current_color == 'y' and color == 'g':
                self.dict_alphabet[letter] = color
            else:
                self.dict_alphabet[letter] = color


        pass
    
    # return a colored string and make sure the current alphabet is updated with the clues
    def decodeColors(self, code, guessed_word):
        colored_str = ""

        # iterate through the guessed word
        for i in range(len(guessed_word)):
            # if the letter is g
            if code[i] == "g":
                # add g to the colored string clue
                colored_str += colored(
                    guessed_word[i],
                    "green",
                )
                # try to update the alphabet
                try:
                    # replace regular alphabet with green
                    self.alphabet[self.alphabet.index(guessed_word[i])] = colored(
                        guessed_word[i],
                        "green",
                    )
                except ValueError:
                    # try to replace yellow with green
                    try:
                        self.alphabet[
                            self.alphabet.index(colored(guessed_word[i], "yellow"))
                        ] = colored(guessed_word[i], "green")
                    except ValueError:
                        pass
            # if the letter is yellow
            elif code[i] == "y":
                colored_str += colored(
                    guessed_word[i], "yellow"
                )  # add yellow to clue string
                # update alphabet
                try:
                    self.alphabet[self.alphabet.index(guessed_word[i])] = colored(
                        guessed_word[i],
                        "yellow",
                    )
                except ValueError:
                    pass
            else:
                colored_str += guessed_word[i]  # add the letter with no colors
                # update alphabet
                try:
                    self.alphabet[self.alphabet.index(guessed_word[i])] = colored(
                        guessed_word[i],
                        "red",
                    )
                except ValueError:
                    pass

        return colored_str

    def is_input_valid(self, guess):
        if len(guess) != len(self.WORD):
            return -1
        elif guess not in VALID_GUESSES:
            return 0
        return 1

    def play_console(self):
        word_guessed = False
        print(f"The length of the word is: {len(self.WORD)}")
        while not word_guessed:
            guess = input("Guess a five letter word: ").lower()
            if self.is_input_valid(guess) == 0:
                print("not acceptable word")
            elif guess == self.WORD:
                print(f"You Won. You got it in {self.guesses} guesses")
                word_guessed = True
            elif self.is_input_valid(guess) == -1:
                print("Please enter a five letter word")
            else:
                code = self.processGuess(guess)
                print(self.decodeColors(code, guess))
                print("".join(self.alphabet))
