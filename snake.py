import pygame

from pygame import QUIT, KEYDOWN, MOUSEBUTTONDOWN
from pygame.locals import DOUBLEBUF

from const import *
from entities import *
from utils import *


icon = pygame.image.load("assets/icon.ico")
pygame.display.set_icon(icon)
pygame.mixer.init()
pygame.init()
pygame.display.init()
pygame.display.set_caption("Snake Game", "Snake Game")
pygame.event.set_allowed((QUIT, KEYDOWN, MOUSEBUTTONDOWN))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF)
screen.set_alpha(None)

score_font = pygame.font.SysFont(None, 100, True)
highscore_font = pygame.font.SysFont(None, 50, True)
death_font = pygame.font.SysFont(None, 30, True)
ui_font = pygame.font.SysFont(None, 50, True)

bg_music = pygame.mixer.Sound("assets/bg_music.mp3")
death_sound = pygame.mixer.Sound("assets/death_sound.mp3")
eat_sound = pygame.mixer.Sound("assets/eat_sound.mp3")

clock = pygame.time.Clock()

def main():
    snake = Snake()
    apple = Apple.spawn(snake=snake)
    bg_music.play(-1)
    death_play = False
    score_text = score_font.render("1", True, SCORE_TEXT_COLOUR)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10))
    move = False  # For handling rapid key strokes; allows only a single keystroke every frame.

    highscore = load_highscore(HIGHSCORE_PATH)
    highscore_text = highscore_font.render(
        f"HIGHSCORE: {highscore}", True, SCORE_TEXT_COLOUR
    )
    highscore_rect = highscore_text.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1)
    )

    death_text = death_font.render("YOU DIED", True, DEATH_TEXT_COLOUR)
    death_rect = death_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    restart = death_font.render(
        "Click anywhere on the screen to restart.", True, DEATH_TEXT_COLOUR
    )
    restart_rect = restart.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.8))
    fps = BASE_FPS

    while True:
        screen.fill(
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
                if not move:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        move = True
                        snake.x_dir = snake.x_dir or -1
                        snake.y_dir = 0
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        move = True
                        snake.x_dir = snake.x_dir or 1
                        snake.y_dir = 0
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        move = True
                        snake.x_dir = 0
                        snake.y_dir = snake.y_dir or -1
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        move = True
                        snake.x_dir = 0
                        snake.y_dir = snake.y_dir or 1

            if event.type == MOUSEBUTTONDOWN and snake.dead:
                snake = Snake()
                apple = Apple.spawn(snake=snake)
                fps = BASE_FPS
                bg_music.play(-1)
                death_play = False

        if snake.head.x == apple.x and snake.head.y == apple.y:
            eat_sound.play()
            apple = Apple.spawn(snake=snake)
            last_body = snake.body[-1]
            snake.body.append(
                pygame.Rect(last_body.x, last_body.y, BLOCK_SIZE, BLOCK_SIZE)
            )
            if len(snake.body) % 3 == 0:
                fps += 1

        draw_grid(screen)
        apple.update(screen)
        snake.update()

        pygame.draw.rect(screen, SNAKE_COLOUR, snake.head, BLOCK_SIZE)
        move = False
        for body in snake.body:
            pygame.draw.rect(screen, SNAKE_COLOUR, body, BLOCK_SIZE)

        score_text = score_font.render(f"{len(snake.body)}", True, SCORE_TEXT_COLOUR)
        screen.blit(score_text, score_rect)
        screen.blit(highscore_text, highscore_rect)

        if snake.dead:
            bg_music.stop()
            if not death_play:
                death_sound.play()
                death_play = True
            screen.blit(death_text, death_rect)
            screen.blit(restart, restart_rect)

            if len(snake.body) > highscore:
                highscore = len(snake.body)
                save_highscore(HIGHSCORE_PATH, highscore)
                highscore_text = highscore_font.render(
                    f"HIGHSCORE: {highscore}", True, SCORE_TEXT_COLOUR
                )

        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError:
        pygame.quit()
