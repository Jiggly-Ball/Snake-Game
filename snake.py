__version__ = "2.2"

import pygame

from pygame import QUIT, KEYDOWN, MOUSEBUTTONDOWN
from pygame.locals import DOUBLEBUF

from core.const import *
from core.entities import *
from core.utils import *

from states import StateManager
from states.game import Game
from states.menu import Menu

icon = pygame.image.load("assets/icon.ico")
pygame.display.set_icon(icon)
pygame.mixer.init()
pygame.init()
pygame.display.init()
pygame.display.set_caption("Snake Game v" + __version__)
pygame.event.set_allowed((QUIT, KEYDOWN, MOUSEBUTTONDOWN))

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF)
# screen.set_alpha(None)


class SnakeGame:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF)
        self.screen.set_alpha(None)
        self.state_manager = StateManager(self.screen, Game, Menu)

    def run(self) -> None:
        self.state_manager.change_state("Game")
        self.state_manager.run_current_state()


if __name__ == "__main__":
    try:
        sanke_game = SnakeGame()
        sanke_game.run()
    except RuntimeError:
        pygame.quit()
