import os

import pygame
import menu
import score_db
from src.config import SIZE, WIDTH, HEIGHT, FPS, DB_NAME
from utils import Button, load_image, terminate


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SIZE)
buttons = pygame.sprite.Group()
clock = pygame.time.Clock()


def check_db_existing():
    if not os.path.exists(DB_NAME):
        with open(DB_NAME, 'a') as db_file:
            pass
        score_db.create_table_and_add_row(DB_NAME)


def start_screen():
    fon = pygame.transform.scale(load_image("bg.png"), (WIDTH, HEIGHT))
    button_play = Button((700, 300), "play.png", (300, 200), buttons)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.click(event.pos):
                    menu.menu2(screen)
                    return

        screen.blit(fon, (0, 0))
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    check_db_existing()
    start_screen()
