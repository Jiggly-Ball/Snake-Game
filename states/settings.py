import pygame

from pygame import QUIT

from states import State
from core.utils import Box, Text, draw_grid
from core.errors import ExitGameError
from core.const import SCREEN_WIDTH, SCREEN_HEIGHT
from core.preset import blue_text_style


class Settings(State):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.fps = 60

    def run(self) -> None:
        box_width = SCREEN_WIDTH // 1.5
        box_height = SCREEN_HEIGHT // 1.2
        box = Box(
            self.window,
            (SCREEN_WIDTH - box_width) // 2,
            (SCREEN_HEIGHT - box_height) // 2,
            box_width,
            box_height,
        )
        bg_vol_text = Text(
            self.window,
            blue_text_style,
            25,
            (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4),
        )

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
                    raise ExitGameError()

            draw_grid(self.window)
            box.render()
            bg_vol_text.render("Music Volume")

            pygame.display.update()
            self.clock.tick(self.fps)
