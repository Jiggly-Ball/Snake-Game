import pygame

from pygame import QUIT, MOUSEBUTTONDOWN

from states import State
from core.utils import Button, ButtonStyle, draw_grid
from core.const import SCREEN_WIDTH, SCREEN_HEIGHT
from core.errors import ExitGameError
from core.preset import menu_button_style


class Menu(State):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.fps = 60

    def run(self) -> None:
        play_button = Button(
            "Play",
            SCREEN_WIDTH // 2,
            (SCREEN_HEIGHT // 2) - 75,
            25,
            menu_button_style,
            self.window,
        )
        settings_button = Button(
            "Settings",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            25,
            menu_button_style,
            self.window,
        )
        quit_button = Button(
            "Quit",
            SCREEN_WIDTH // 2,
            (SCREEN_HEIGHT // 2) + 75,
            25,
            menu_button_style,
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
                    raise ExitGameError()

                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if play_button.click():
                        self.manager.change_state("Game")
                        self.manager.exit_current_state()

                    elif settings_button.click():
                        self.manager.change_state("Settings")
                        self.manager.exit_current_state()

                    elif quit_button.click():
                        raise ExitGameError()

            draw_grid(self.window)
            play_button.render()
            settings_button.render()
            quit_button.render()

            pygame.display.update()
            self.clock.tick(self.fps)
