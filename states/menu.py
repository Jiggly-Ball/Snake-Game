import pygame

from pygame import QUIT, KEYDOWN, MOUSEBUTTONDOWN

from states import State
from core.const import *
from core.entities import *
from core.utils import *


class Menu(State):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.fps = 60

    def run(self) -> None:
        while True:
            self.window.fill(
                (
                    255,
                    255,
                    255,
                )
            )

            for event in pygame.event.get():
                if event.type == QUIT:
                    raise
        
            pygame.display.update()
            self.clock.tick(self.fps)