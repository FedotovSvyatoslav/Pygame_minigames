import pygame
import os
import sys


def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, img, size, spritegroup):
        super().__init__(spritegroup)
        img = load_image(img)
        self.image = pygame.transform.scale(img, size)
        self.rect = self.image.get_rect()
        self.killed = False
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def click(self, pos):
        if self.killed:
            return
        if self.rect.collidepoint(pos[0], pos[1]):
            return True
        return False


class Text:
    def __init__(self, screen):
        self.texts = {}
        self.screen = screen

    def add_text(self, text, color, font, x, y, name):
        font = pygame.font.Font(None, font)
        string_render = font.render(text, True, color)
        intro_rect = string_render.get_rect()
        intro_rect.x = x
        intro_rect.y = y
        self.texts[name] = (string_render, intro_rect)
        self.screen.blit(string_render, intro_rect)

    def update(self):
        for i in self.texts.items():
            self.screen.blit(i[1][0], i[1][1])

    def remove_text(self, name):
        try:
            del self.texts[name]
        except KeyError:
            pass


class Text_Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text, pos, font, screen, bg=(0, 0, 0), feedback=""):
        self.screen = screen
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        self.screen.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            return True


def terminate():
    pygame.quit()
    sys.exit()
