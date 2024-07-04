import pygame

from pygame import QUIT, KEYDOWN, MOUSEBUTTONDOWN

from states import State
from core.const import *
from core.entities import *
from core.utils import *


class Game(State):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.death_play = False
        self.move = False  # For handling rapid key strokes; allows only a single keystroke every frame.
        self.fps = BASE_FPS
        self.highscore = load_highscore(HIGHSCORE_PATH)

        self.bg_music = pygame.mixer.Sound("assets/bg_music.mp3")
        self.death_sound = pygame.mixer.Sound("assets/death_sound.mp3")
        self.eat_sound = pygame.mixer.Sound("assets/eat_sound.mp3")

        self.score_text = Text(
            self.window, 100, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10), SCORE_TEXT_COLOUR
        )
        self.highscore_text = Text(
            self.window, 50, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1), SCORE_TEXT_COLOUR
        )
        self.death_text = Text(
            self.window, 30, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), DEATH_TEXT_COLOUR
        )
        self.restart_text = Text(
            self.window, 30, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.8), DEATH_TEXT_COLOUR
        )

    def run(self) -> None:
        snake = Snake()
        apple = Apple.spawn(snake=snake)
        self.bg_music.play(-1)

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

                if event.type == KEYDOWN:
                    if not self.move and event.key in KEY_ALL:
                        self.move = True
                        if snake.x_dir != 1 and (event.key in KEY_LEFT):
                            snake.x_dir = snake.x_dir or -1
                            snake.y_dir = 0
                        elif snake.x_dir != -1 and (event.key in KEY_RIGHT):
                            snake.x_dir = snake.x_dir or 1
                            snake.y_dir = 0
                        elif snake.y_dir != -1 and (event.key in KEY_UP):
                            snake.x_dir = 0
                            snake.y_dir = snake.y_dir or -1
                        elif snake.y_dir != 1 and (event.key in KEY_DOWN):
                            snake.x_dir = 0
                            snake.y_dir = snake.y_dir or 1

                if event.type == MOUSEBUTTONDOWN and snake.dead:
                    snake = Snake()
                    apple = Apple.spawn(snake=snake)
                    self.fps = BASE_FPS
                    self.bg_music.play(-1)
                    self.death_play = False

            if snake.head.x == apple.x and snake.head.y == apple.y:
                self.eat_sound.play()
                last_body = snake.body[-1]
                snake.body.append(
                    pygame.Rect(last_body.x, last_body.y, BLOCK_SIZE, BLOCK_SIZE)
                )
                apple = Apple.spawn(snake=snake)
                if len(snake.body) % 4 == 0:
                    self.fps += 1

            draw_grid(self.window)
            apple.update(self.window)
            snake.update()

            pygame.draw.rect(self.window, SNAKE_COLOUR, snake.head, BLOCK_SIZE)
            self.move = False
            for body in snake.body:
                pygame.draw.rect(self.window, SNAKE_COLOUR, body, BLOCK_SIZE)

            self.score_text.render(f"{len(snake.body)}")
            self.highscore_text.render(f"HIGHSCORE: {self.highscore}")

            if snake.dead:
                self.bg_music.stop()
                if not self.death_play:
                    self.death_sound.play()
                    self.death_play = True

                self.death_text.render("You have died!")
                self.restart_text.render("Click anywhere on the screen to restart.")

                if len(snake.body) > self.highscore:
                    self.highscore = len(snake.body)
                    save_highscore(HIGHSCORE_PATH, self.highscore)
                    self.highscore_text.render(f"HIGHSCORE: {self.highscore}")

            pygame.display.update()
            self.clock.tick(self.fps)
