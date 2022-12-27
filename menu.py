import pygame
import sys
import os

pygame.init()
FPS = 50
screen = pygame.display.set_mode((500, 600))
buttons = pygame.sprite.Group
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
    def __init__(self, pos, img):
        super.__init__(buttons)
        self.image = load_image(img)
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


def start_screen()

