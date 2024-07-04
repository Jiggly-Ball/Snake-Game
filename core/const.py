import pygame
from typing import Tuple


BASE_FPS: int = 6
SCREEN_WIDTH: int = 750
SCREEN_HEIGHT: int = 750
BLOCK_SIZE: int = 50  # 25 | 50 | 150 | 250
SNAKE_COLOUR: str = "green"
APPLE_COLOUR: str = "red"
SCORE_TEXT_COLOUR: int = 0xFFFF14
DEATH_TEXT_COLOUR: str = "red"
HIGHSCORE_PATH: str = "data.bin"
KEY_LEFT: Tuple[int, int] = (pygame.K_a, pygame.K_LEFT)
KEY_RIGHT: Tuple[int, int] = (pygame.K_d, pygame.K_RIGHT)
KEY_UP: Tuple[int, int] = (pygame.K_w, pygame.K_UP)
KEY_DOWN: Tuple[int, int] = (pygame.K_s, pygame.K_DOWN)
KEY_ALL: Tuple[int, ...] = KEY_LEFT + KEY_RIGHT + KEY_UP + KEY_DOWN
