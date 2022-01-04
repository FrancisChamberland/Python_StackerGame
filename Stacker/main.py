import sys
from pygame import *
from window import Window
from constants import *
from game import Game


def main():
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, CASE_SIZE, BACKGROUND_COLOR, PRIMARY_COLOR)
    game = Game(window)
    window.display()
    game.start()

    while True:
        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    game.stack()
            if e.type == QUIT:
                sys.exit(0)
        window.update()
        game.moveCases()

if __name__ == '__main__':
    main()