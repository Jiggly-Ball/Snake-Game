import os
import pickle
import pygame

from typing import Optional, Union, Sequence, Tuple

from const import SCREEN_HEIGHT, SCREEN_WIDTH, BLOCK_SIZE


class Text:
    def __init__(
        self,
        window: pygame.Surface,
        size: int,
        center: Tuple[int, int],
        colour: Union[int, str, Sequence[int]],
        bold: bool = False,
        italic: bool = False,
        name: Optional[Union[str, bytes]] = None,
    ) -> None:
        self.window = window
        self.center = center
        self.colour = colour
        self.font = pygame.font.SysFont(name, size, bold, italic)
        self.rect: Optional[pygame.Rect] = None

    def render(
        self,
        text: str,
        colour: Optional[Union[int, str, Sequence[int]]] = None,
        bg_colour: Optional[Union[int, str, Sequence[int]]] = None,
        antialias: bool = True,
        wrap_length: int = 0,
    ) -> None:
        rendered_text = self.font.render(
            text=text,
            antialias=antialias,
            color=colour or self.colour,
            bgcolor=bg_colour,
            wraplength=wrap_length,
        )
        if self.rect is None:
            self.rect = rendered_text.get_rect(center=self.center)
        self.window.blit(rendered_text, self.rect)


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
