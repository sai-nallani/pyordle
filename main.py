from MainUI import MainUI
from wordle_brain import WordleBrain

def main():
    # wb = WordleBrain()
    # wb.WORD = 'stalk'
    # wb.play_console()
    ui = MainUI(debug=False, word='stalk')
    while ui.PLAYING:
        if ui.PLAY_AGAIN:
            ui = MainUI(debug=False, word='purer')


if __name__ == "__main__":
    main()
