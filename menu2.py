import pygame
import sys
import os
import dice


buttons = pygame.sprite.Group()
clock = pygame.time.Clock()
FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, img, size):
        super().__init__(buttons)
        self.image = pygame.transform.scale(load_image(img), size)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    
    def click(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            return True
        return  False


def menu2(screen):
    screen.fill((0, 0, 0))
    text = "Выберете игру"
    font = pygame.font.Font(None, 70)
    string_render = font.render(text, 1, pygame.Color("White"))
    intro_rect = string_render.get_rect()
    intro_rect.x = 400
    intro_rect.top = 20
    screen.blit(string_render, intro_rect)
    dice_icon = Button((0, 315), "dice.png", (560, 315))
    chess_icon = Button((560, 50), "chess.png", (560, 315))
    voll_icon = Button((0, 30), "voleyball.png", (560, 315))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dice_icon.click(event.pos):
                    pass
                    #dice.start_game(screen)
                if chess_icon.click(event.pos):
                    pass  # сюда впиши функцию активации игры
                if voll_icon.click(event.pos):
                    pass
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def info():
    pass
