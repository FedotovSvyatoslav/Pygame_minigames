import pygame

from games import space_invaders
from games import dice
import games
from games import pong
from useful import Button, terminate, load_image

SIZE = WIDTH, HEIGHT = 1120, 630
buttons = pygame.sprite.Group()
clock = pygame.time.Clock()
FPS = 50


def menu2(screen):
    screen.fill((255, 255, 255))

    fon = pygame.transform.scale(load_image("bg2.jpg"), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    text = "Выберите игру"
    font = pygame.font.Font(None, 70)
    string_render = font.render(text, True, (153, 153, 102))
    intro_rect = string_render.get_rect()
    intro_rect.x = 400
    intro_rect.top = 20
    screen.blit(string_render, intro_rect)

    dice_icon = Button((610, 70), "dice.png", (440, 315), buttons)
    chess_icon = Button((140, 70), "chess.png", (420, 315), buttons)
    pong_icon = Button((120, 340), "pong.png", (330, 185), buttons)
    space_icon = Button((520, 260), "space.png", (560, 360), buttons)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dice_icon.click(event.pos):
                    games.dice.start_game(screen)
                if chess_icon.click(event.pos):
                    games.chess_loop(screen)
                if pong_icon.click(event.pos):
                    pong.start_game(screen)
                if space_icon.click(event.pos):
                    space_invaders.space_invaders_loop(screen)

        screen.blit(fon, (0, 0))
        screen.blit(string_render, intro_rect)
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def info():
    pass
