from __future__ import annotations

import pygame
from typing import Dict, Optional, Generator

from core.utils import Text
from core.const import MENU_COLOUR, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_TEXT_SIZE


class State:
    def __init__(self, *, window: pygame.Surface, manager: StateManager) -> None:
        self.window = window
        self.manager = manager
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        """The method to be executed by the StateManager when called."""


class StateManager:
    __slots__ = ("__states", "current_state")

    def __init__(self, window: pygame.Surface, *states: State) -> None:
        for state in states:
            assert issubclass(
                state, State
            ), f"Expected subclass of `{State}` instead got `{state.__mro__[-2]}`"

        self.__states: Dict[str, State] = {
            class_.__name__: class_(window=window, manager=self) for class_ in states
        }
        self.current_state: Optional[State] = None

    def change_state(self, state_name: str) -> None:
        assert (
            state_name in self.__states
        ), f"State `{state_name}` isn't present from the available states: `{', '.join(self.get_all_states())}`"
        self.current_state = self.__states[state_name]

    def get_state(self) -> Optional[State]:
        return self.current_state

    def get_all_states(self) -> Generator[str]:
        return (state for state in self.__states.keys())

    def run_current_state(self) -> None:
        self.current_state.run()
