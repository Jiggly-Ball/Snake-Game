import os
import pickle
import pygame

from dataclasses import dataclass
from typing import Optional, Union, Sequence, Tuple

from core.const import SCREEN_HEIGHT, SCREEN_WIDTH, BLOCK_SIZE


@dataclass
class ButtonStyle:
    button_width: int
    button_height: int
    text_size: int
    text_colour: Union[str, int]


class Text:
    __slots__ = ("window", "center", "colour", "font", "rect")

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


class Button:
    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        button_style: ButtonStyle,
        window: pygame.Surface,
    ) -> None:
        self.text = text
        self.x = x
        self.y = y
        self.button_style = button_style
        self.window = window

    def run(self) -> bool:
        button_text = Text(
            self.window,
            self.button_style.text_size,
            (self.x, self.y + self.button_style.button_height // 2),
            self.button_style.text_colour,
        )
        button_rect = pygame.rect.Rect(
            self.x - self.button_style.button_width // 2,
            self.y,
            self.button_style.button_width,
            self.button_style.button_height,
        )
        pygame.draw.rect(self.window, "black", button_rect, 0, 5)
        pygame.draw.rect(self.window, "green", button_rect, 2, 5)
        button_text.render(self.text)

        pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
            return False
        return False


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
