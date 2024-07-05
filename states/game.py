import pygame

from pygame import QUIT, KEYDOWN, MOUSEBUTTONDOWN

from states import State
from core.const import *
from core.entities import *
from core.utils import *
from core.errors import ExitGameError
from core.preset import blue_text_style, red_text_style


class Game(State):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        self.bg_music = pygame.mixer.Sound(BG_MUSIC_PATH)
        self.death_sound = pygame.mixer.Sound(DEATH_SFX_PATH)
        self.eat_sound = pygame.mixer.Sound(EAT_SFX_PATH)

        self.score_text = Text(
            self.window, blue_text_style, 100, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10)
        )
        self.highscore_text = Text(
            self.window, blue_text_style, 50, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1)
        )
        self.death_text = Text(
            self.window, red_text_style, 30, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        )
        self.restart_text = Text(
            self.window, red_text_style, 30, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.8)
        )

    def run(self) -> None:

        snake = Snake()
        apple = Apple.spawn(snake=snake)
        self.bg_music.set_volume(self.volume.bg_vol)
        self.death_sound.set_volume(self.volume.sfx_vol)
        self.eat_sound.set_volume(self.volume.sfx_vol)
        self.bg_music.play(-1)

        death_play = False
        move = False  # For handling rapid key strokes; allows only a single keystroke every frame.
        fps = BASE_FPS
        highscore = load_highscore(HIGHSCORE_PATH)

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

                if event.type == KEYDOWN:
                    if not move:
                        if snake.x_dir != 1 and (event.key in KEY_LEFT):
                            snake.x_dir = snake.x_dir or -1
                            snake.y_dir = 0
                            move = True
                        elif snake.x_dir != -1 and (event.key in KEY_RIGHT):
                            snake.x_dir = snake.x_dir or 1
                            snake.y_dir = 0
                            move = True
                        elif snake.y_dir != -1 and (event.key in KEY_UP):
                            snake.x_dir = 0
                            snake.y_dir = snake.y_dir or -1
                            move = True
                        elif snake.y_dir != 1 and (event.key in KEY_DOWN):
                            snake.x_dir = 0
                            snake.y_dir = snake.y_dir or 1
                            move = True

                if event.type == MOUSEBUTTONDOWN and snake.dead:
                    self.manager.change_state("Menu")
                    self.manager.exit_current_state()
                    # snake = Snake()
                    # apple = Apple.spawn(snake=snake)
                    # fps = BASE_FPS
                    # self.bg_music.play(-1)
                    # death_play = False

            if snake.head.x == apple.x and snake.head.y == apple.y:
                self.eat_sound.play()
                last_body = snake.body[-1]
                snake.body.append(
                    pygame.Rect(last_body.x, last_body.y, BLOCK_SIZE, BLOCK_SIZE)
                )
                apple = Apple.spawn(snake=snake)
                if len(snake.body) % 5 == 0:
                    fps += 2

            apple.update(self.window)
            snake.update()
            draw_grid(self.window)

            pygame.draw.rect(self.window, SNAKE_COLOUR, snake.head, BLOCK_SIZE)
            move = False
            for body in snake.body:
                pygame.draw.rect(self.window, SNAKE_COLOUR, body, BLOCK_SIZE)

            self.score_text.render(f"{len(snake.body)}")
            self.highscore_text.render(f"HIGHSCORE: {highscore}")

            if snake.dead:
                self.bg_music.stop()
                if not death_play:
                    self.death_sound.play()
                    death_play = True

                self.death_text.render("You have died!")
                self.restart_text.render("Click anywhere on the screen to restart.")

                if len(snake.body) > highscore:
                    highscore = len(snake.body)
                    save_highscore(HIGHSCORE_PATH, highscore)
                    self.highscore_text.render(f"HIGHSCORE: {highscore}")

            pygame.display.update()
            self.clock.tick(fps)
