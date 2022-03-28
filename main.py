from MainUI import MainUI


def main():
    # WordleBrain = WordleBrain()
    # WordleBrain.play_console()
    ui = MainUI()
    while ui.PLAYING:
        if ui.PLAY_AGAIN:
            ui = MainUI()


if __name__ == "__main__":
    main()
