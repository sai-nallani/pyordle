from valid_guesses import VALID_GUESSES
from word_list import WORDS
import os
import random
from termcolor import colored

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


class WordleBrain:
    def __init__(self):
        # create random word

        self.WORD = random.choice(WORDS)
        self.alphabet = list("abcdefghijklmnopqrstuvwxyz")
        self.guesses = 1

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
                for j in range(len(guessWord)):
                    if j == i:
                        continue
                    if guessWord[j] == guessWord[i]:
                        should_add_yellow = False
                # add yellow or white to clue
                if should_add_yellow:
                    clue += 'y'
                else:
                    clue += 'w'
            # add white to clue
            else:
                clue += "w"

        return clue

    # return a colored string and make sure the current alphabet is updated with the clues
    def decodeColors(self, code, guessed_word):
        colored_str = ''

        # iterate through the guessed word
        for i in range(len(guessed_word)):
            # if the letter is g
            if code[i] == 'g':
                # add g to the colored string clue
                colored_str += colored(guessed_word[i], 'green', )
                # try to update the alphabet
                try:
                    # replace regular alphabet with green
                    self.alphabet[self.alphabet.index(guessed_word[i])] = colored(guessed_word[i], 'green', )
                except ValueError:
                    # try to replace yellow with green
                    try:
                        self.alphabet[self.alphabet.index(colored(guessed_word[i], "yellow"))] = colored(
                            guessed_word[i], 'green')
                    except ValueError:
                        pass
            # if the letter is yellow
            elif code[i] == 'y':
                colored_str += colored(guessed_word[i], 'yellow')  # add yellow to clue string
                # update alphabet
                try:
                    self.alphabet[self.alphabet.index(guessed_word[i])] = colored(guessed_word[i], 'yellow', )
                except ValueError:
                    pass
            else:
                colored_str += guessed_word[i]  # add the letter with no colors
                # update alphabet
                try:
                    self.alphabet[self.alphabet.index(guessed_word[i])] = colored(guessed_word[i], 'red', )
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
        guesses = 0
        word_guessed = False
        print(f"The length of the word is: {len(self.WORD)}")
        while not word_guessed:
            guess = input("Guess a five letter word: ").lower()
            if self.is_input_valid(guess):
                print("not acceptable word")
            elif guess == self.WORD:
                print(f"You Won. You got it in {guesses} guesses")
                word_guessed = True
            elif self.is_input_valid(guess):
                print("Please enter a five letter word")
            else:
                code = self.processGuess(guess)
                print(self.decodeColors(code, guess))
                print(''.join(self.alphabet))
