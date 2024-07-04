import pygame

from pygame import QUIT

from states import State
from core.utils import Button, ButtonStyle, draw_grid
from core.const import SCREEN_WIDTH, SCREEN_HEIGHT


class Settings(State):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.fps = 60

    def run(self) -> None:
        while True:
            self.window.fill(
                (
                    0,
                    0,
                    0,
                )
            )

            for event in pygame.event.get():
                if event.type == QUIT:
                    raise

            draw_grid(self.window)

            pygame.display.update()
            self.clock.tick(self.fps)
