import pygame

from src.config import WIDTH, HEIGHT, FPS
from src.games import dice, pong, space_invaders
from src.games.chess import chess_loop
from src.main import clock
from utils import Button, terminate, load_image

buttons = pygame.sprite.Group()


def menu2(screen):
    fon = pygame.transform.scale(load_image("bg2.jpg"), (WIDTH, HEIGHT))
    font = pygame.font.Font(None, 70)
    text = font.render("Выберите игру", True, (153, 153, 102))
    intro_rect = text.get_rect(x=400, top=20)

    dice_icon = Button((610, 70), "dice.png", (440, 315), buttons)
    chess_icon = Button((140, 70), "chess.png", (420, 315), buttons)
    pong_icon = Button((120, 340), "pong.png", (330, 185), buttons)
    space_icon = Button((520, 260), "space.png", (560, 360), buttons)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # Возврат в start_screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if dice_icon.click(pos):
                    dice.start_game(screen)
                elif chess_icon.click(pos):
                    chess_loop(screen)
                elif pong_icon.click(pos):
                    pong.start_game(screen)
                elif space_icon.click(pos):
                    space_invaders.space_invaders_loop(screen)

        screen.blit(fon, (0, 0))
        screen.blit(text, intro_rect)
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
