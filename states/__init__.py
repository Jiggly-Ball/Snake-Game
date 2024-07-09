from states.base import State, StateManager
from states.game import Game
from states.menu import Menu
from states.settings import Settings
from typing import Tuple

__all__ = ("State", "StateManager")
GAME_STATES: Tuple[State, ...] = (Game, Menu, Settings)
