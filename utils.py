import pickle
import os
import pygame

from const import SCREEN_HEIGHT, SCREEN_WIDTH, BLOCK_SIZE


def draw_grid(window: pygame.Surface):
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            line = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(window, (255, 255, 255), line, 1)


def load_highscore(path: str) -> int:
    if not os.path.isfile(path=path):
        save_highscore(path=path, score=1)
        return 1

    with open(path, "rb") as f:
        try:
            return pickle.load(f)
        except EOFError:
            return 1


def save_highscore(path: str, score: int) -> None:
    with open(path, "wb") as f:
        pickle.dump(score, f)