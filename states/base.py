from __future__ import annotations

import pygame
from typing import Dict, Optional


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
            ), f"Expected {State} instead got {type(state)}"

        self.__states: Dict[str, State] = {
            class_.__name__: class_(window=window, manager=self) for class_ in states
        }
        self.current_state: Optional[State] = None

    def change_state(self, state_name: str) -> None:
        assert (
            state_name in self.__states
        ), f"State: {state_name} isn't present from the available states: {self.__states.keys()}"
        self.current_state = self.__states[state_name]

    def get_state(self) -> Optional[State]:
        return self.current_state

    def run_current_state(self) -> None:
        self.current_state.run()
