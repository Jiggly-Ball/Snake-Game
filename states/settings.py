import pygame

from pygame import QUIT

from states import State
from core.utils import Text, draw_grid
from core.const import SCREEN_WIDTH, SCREEN_HEIGHT
from core.errors import ExitGameError
from core.preset import blue_text_style


class Settings(State):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.fps = 60

    def run(self) -> None:
        layer_width = SCREEN_WIDTH // 1.5
        layer_height = SCREEN_HEIGHT // 1.2
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
            button_rect = pygame.rect.Rect(
                (SCREEN_WIDTH - layer_width) // 2,
                (SCREEN_HEIGHT - layer_height) // 2,
                layer_width,
                layer_height,
            )
            pygame.draw.rect(self.window, "black", button_rect, 0, 5)
            pygame.draw.rect(self.window, "green", button_rect, 2, 5)

            bg_vol_text.render("Music Volume")

            pygame.display.update()
            self.clock.tick(self.fps)
