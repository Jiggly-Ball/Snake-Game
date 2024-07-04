import pygame

from pygame import QUIT

from states import State
from core.utils import Button, ButtonStyle, draw_grid
from core.const import SCREEN_WIDTH, SCREEN_HEIGHT


class Menu(State):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.menu_button = ButtonStyle(150, 40, 25, 0xFFFF14)
        self.fps = 60

    def run(self) -> None:
        play_button = Button(
            "Play",
            SCREEN_WIDTH // 2,
            (SCREEN_HEIGHT // 2) - 75,
            self.menu_button,
            self.window,
        )
        settings_button = Button(
            "Settings",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            self.menu_button,
            self.window,
        )
        quit_button = Button(
            "Quit",
            SCREEN_WIDTH // 2,
            (SCREEN_HEIGHT // 2) + 75,
            self.menu_button,
            self.window,
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
                    raise

            draw_grid(self.window)
            if play_button.run():
                self.manager.change_state("Game")
                self.manager.run_current_state()

            elif settings_button.run():
                self.manager.change_state("Settings")
                self.manager.run_current_state()

            elif quit_button.run():
                raise

            pygame.display.update()
            self.clock.tick(self.fps)
