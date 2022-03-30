from MainUI import MainUI
from wordle_brain import WordleBrain

def console(word):
    wb = WordleBrain()
    wb.WORD = 'stalk'
    wb.play_console()

def gui(debug, word=None):
    ui = MainUI(debug=False, word=word)
    while ui.PLAYING:
        if ui.PLAY_AGAIN:
            ui = MainUI(debug=False, word=word)
    
    


if __name__ == "__main__":
    gui('pupil')
