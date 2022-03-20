from termcolor import colored
from acceptable_words import words
import os
import random


class WordleBrain:
    def __init__(self):
        os.system('color')
        self.WORD = random.choice(words)
        print(f"The length of the word is: {len(self.WORD)}")
        self.alphabet = list("abcdefghijklmnopqrstuvwxyz")

    def processGuess(self, guessWord):
        clue = ""
        for i in range(len(self.WORD)):
            if self.WORD[i] == guessWord[i]:
                clue += "g"
            elif guessWord[i] in self.WORD:
                flag = True
                for j in range(len(guessWord)):
                    if j == i:
                        continue
                    if guessWord[j] == guessWord[i]:
                        flag = False
                if flag:
                    clue += 'y'
                else:
                    clue += 'w'
            else:
                clue += "w"
        return clue

    def decodeColors(self, code, guessed_word):
        colored_str = ''
        for i in range(len(guessed_word)):
            if code[i] == 'g':
                colored_str += colored(guessed_word[i], 'green', )
                try:
                    self.alphabet[self.alphabet.index(guessed_word[i])] = colored(guessed_word[i], 'green', )
                except ValueError:
                    try:
                        self.alphabet[self.alphabet.index(colored(guessed_word[i], "yellow"))] = colored(
                            guessed_word[i], 'green')
                    except ValueError:
                        pass
            elif code[i] == 'y':
                colored_str += colored(guessed_word[i], 'yellow')
                try:
                    self.alphabet[self.alphabet.index(guessed_word[i])] = colored(guessed_word[i], 'yellow', )
                except ValueError:
                    pass
            else:
                colored_str += guessed_word[i]
                try:
                    self.alphabet[self.alphabet.index(guessed_word[i])] = colored(guessed_word[i], 'red', )
                except ValueError:
                    pass

        return colored_str

    def play_console(self):
        guesses = 0
        word_guessed = False
        while not word_guessed:
            guess = input("Guess a five letter word: ").lower()
            guesses += 1
            if guess == self.WORD:
                print(f"You Won. You got it in {guesses} guesses")
                word_guessed = True
            elif len(guess) != 5:
                print("Please enter a five letter word")
                guesses -= 1
            else:
                code = self.processGuess(guess)
                print(self.decodeColors(code, guess))
                print(''.join(self.alphabet))
