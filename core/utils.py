import os
import pickle
import pygame

from dataclasses import dataclass
from typing import Optional, Union, Sequence, Tuple

from core.const import SCREEN_HEIGHT, SCREEN_WIDTH, BLOCK_SIZE


@dataclass
class TextStyle:
    text_colour: Union[int, str, Sequence[int]]
    text_bg_colour: Optional[Union[int, str, Sequence[int]]] = None
    bold: bool = False
    italic: bool = False
    font_name: Optional[Union[str, bytes]] = None


@dataclass
class ButtonStyle:
    button_width: int
    button_height: int
    text_style: TextStyle


@dataclass
class MusicVol:
    bg_vol: float = 0.5
    sfx_vol: float = 0.5


class Text:
    __slots__ = ("window", "center", "text_style", "text_size", "font", "rect")

    def __init__(
        self,
        window: pygame.Surface,
        text_style: TextStyle,
        text_size: int,
        center: Tuple[int, int],
    ) -> None:
        self.window = window
        self.center = center
        self.text_style = text_style
        self.text_size = text_size
        self.font = pygame.font.SysFont(
            self.text_style.font_name,
            text_size,
            self.text_style.bold,
            self.text_style.italic,
        )
        self.rect: Optional[pygame.Rect] = None

    def render(
        self,
        text: str,
        colour: Optional[Union[int, str, Sequence[int]]] = None,
        text_bg_colour: Optional[Union[int, str, Sequence[int]]] = None,
        antialias: bool = True,
        wrap_length: int = 0,
    ) -> None:
        rendered_text = self.font.render(
            text=text,
            antialias=antialias,
            color=colour or self.text_style.text_colour,
            bgcolor=text_bg_colour or self.text_style.text_bg_colour,
            wraplength=wrap_length,
        )
        if self.rect is None:
            self.rect = rendered_text.get_rect(center=self.center)
        self.window.blit(rendered_text, self.rect)


class Button:
    __slots__ = (
        "text",
        "x",
        "y",
        "text_size",
        "button_style",
        "window",
        "__clicked",
        "button_text",
        "button_rect",
    )

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        text_size: int,
        button_style: ButtonStyle,
        window: pygame.Surface,
    ) -> None:
        self.text = text
        self.x = x
        self.y = y
        self.text_size = text_size
        self.button_style = button_style
        self.window = window
        self.__clicked = False
        self.button_text = Text(
            self.window,
            self.button_style.text_style,
            self.text_size,
            (self.x, self.y + self.button_style.button_height // 2),
        )
        self.button_rect = pygame.rect.Rect(
            self.x - self.button_style.button_width // 2,
            self.y,
            self.button_style.button_width,
            self.button_style.button_height,
        )

    def render(self) -> None:
        """Manually render the buttons."""

        pygame.draw.rect(self.window, "black", self.button_rect, 0, 5)
        pygame.draw.rect(self.window, "green", self.button_rect, 2, 5)
        self.button_text.render(self.text)

    def click(self) -> bool:
        """Should manually be called when pygame.MOUSEBUTTONDOWN event has been dispatched."""

        pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(pos):
            return True
        return False

    def run(self) -> bool:
        """Handles rendering & click events automatically (buggy)."""

        self.render()
        pos = pygame.mouse.get_pos()

        if self.button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.__clicked:
                self.__clicked = True
                return True
        if pygame.mouse.get_pressed()[0] == 0:
            self.__clicked = False

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


def load_settings(path: str) -> MusicVol:
    if not os.path.isfile(path=path):
        save_settings(path=path, settings=MusicVol())
        return MusicVol()

    with open(path, "rb") as f:
        try:
            return pickle.load(f)
        except EOFError:
            return MusicVol()


def save_settings(path: str, settings: MusicVol) -> None:
    with open(path, "wb") as f:
        pickle.dump(settings, f)
