import os

import pygame
import menu2
import sqls
import useful
from useful import Button, load_image, terminate

DB_NAME = "score.db"

pygame.init()
pygame.mixer.init()
FPS = 50
SIZE = WIDTH, HEIGHT = 1120, 630
screen = pygame.display.set_mode(SIZE)
buttons = pygame.sprite.Group()
clock = pygame.time.Clock()

if not os.path.exists(DB_NAME):
    with open(DB_NAME, 'a') as db_file:
        pass
    sqls.create_table_and_add_row(DB_NAME)


def start_screen():
    fon = pygame.transform.scale(load_image("bg.png"), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    button_play = Button((700, 300), "play.png", (300, 200), buttons)
    button_info = Button((950, 500), "info.png", (100, 100), buttons)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.click(event.pos):
                    menu2.menu2(screen)
                    return
                if button_info.click(event.pos):
                    menu2.info()
                    return
        screen.blit(fon, (0, 0))
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
