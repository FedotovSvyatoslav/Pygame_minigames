import pygame
import sys
import os
import dice
import menu2

pygame.init()
FPS = 50
SIZE = WIDTH, HEIGHT = 1120, 630
screen = pygame.display.set_mode(SIZE)
buttons = pygame.sprite.Group()
clock = pygame.time.Clock()


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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image("bg.png"), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    button_play = Button((700, 300), "play.png", (300, 200))
    button_info = Button((950, 500), "info.png", (100, 100))
    
    while True:
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
                    
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)



start_screen()
