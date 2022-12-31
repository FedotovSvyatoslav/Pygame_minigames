import pygame
import dice
from useful import Button, load_image, terminate


buttons = pygame.sprite.Group()
clock = pygame.time.Clock()
FPS = 50


def menu2(screen):
    screen.fill((0, 0, 0))
    text = "Выберете игру"
    font = pygame.font.Font(None, 70)
    string_render = font.render(text, 1, pygame.Color("White"))
    intro_rect = string_render.get_rect()
    intro_rect.x = 400
    intro_rect.top = 20
    screen.blit(string_render, intro_rect)
    dice_icon = Button((0, 315), "dice.png", (560, 315), buttons)
    chess_icon = Button((560, 50), "chess.png", (560, 315), buttons)
    voll_icon = Button((0, 30), "voleyball.png", (560, 315), buttons)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dice_icon.click(event.pos):
                    dice.start_game(screen)
                if chess_icon.click(event.pos):
                    pass  # сюда впиши функцию активации игры
                if voll_icon.click(event.pos):
                    pass
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def info():
    pass
