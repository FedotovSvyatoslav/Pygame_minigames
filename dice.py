import pygame
import sys
import random

import useful
from useful import load_image, terminate, Button, Text


pygame.init()
FPS = 30
SIZE = WIDTH, HEIGHT = 1120, 630
screen = pygame.display.set_mode(SIZE)
dice_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
text_manager = Text(screen)
stop_rotate = pygame.USEREVENT + 1
point_frame = {1: 48, 2: 52, 3: -1, 4: 0, 5: 60, 6: 56}


class Dice(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__(dice_group)
        self.frames = []
        self.cut_sheet(load_image(sheet), columns, rows)
        self.cur_frame = 0
        self.point = 0
        self.image = self.frames[self.cur_frame]
        self.round_ended = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        del self.frames[1:17]
        del self.frames[113:]
    
    def update(self):
        if self.round_ended:
            self.image = pygame.transform.scale(self.frames[point_frame[self.point]], (70, 70))
            self.rect = self.image.get_rect()
            self.rect.x = 510
            self.rect.y = 210

        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (70, 70))
            self.rect = self.image.get_rect()
            self.rect.x = 510
            self.rect.y = 210


class Game:
    def __init__(self):
        self.point_1 = 0
        self.save_1 = 0
        self.point_2 = 0
        self.save_2 = 0
        self.turn = random.randint(0, 1)
    
    def play_round(self):
        if self.turn == 0:
            text = "Ход игрока 1"
        else:
            text = "Ход игрока 2"
        text_manager.add_text(text, (0, 0, 0), 30, 500, 10, "hod")
        point = random.randint(1, 6)
        pygame.time.set_timer(stop_rotate, random.randint(500, 1000))
        return point


def start_game(screen):
    screen.fill((255, 255, 255))
    play_btn = Button((490, 200), "play2.png", (170, 100), all_sprites)
    text_manager.add_text("Очки игрока 1", (0, 0, 0), 70, 30, 10, "txt")
    text_manager.add_text("Очки игрока 2", (0, 0, 0), 70, 720, 10, "txt2")
    text_manager.add_text("0", (0, 0, 0), 70, 140, 50, "score1")
    text_manager.add_text("0", (0, 0, 0), 70, 830, 50, "score2")
    global dice
    dice = Dice("dice_anim.png", 16, 9)
    clock = pygame.time.Clock()
    game = Game()
    round_is_play = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.click(event.pos):
                    round_is_play = True
                    dice.round_ended = False
                    point = game.play_round()
                    text_manager.remove_text("win")
                    play_btn.kill()
                    play_btn.killed = True
                try:
                    if cont.click(event.pos):
                        dice.round_ended = False
                        point = game.play_round()
                    elif save_btn.click(event.pos):
                        dice.round_ended = False
                        if game.turn == 0:
                            game.turn = 1
                            game.save_1 = game.point_1
                        else:
                            game.turn = 0
                            game.save_2 = game.point_2
                        point = game.play_round()
                except UnboundLocalError:
                    pass

            if event.type == stop_rotate:
                if dice.round_ended or not round_is_play:
                    continue
                if game.turn == 0:
                    text_manager.remove_text("score1")
                    if point == 1:
                        game.point_1 = game.save_1 - 1
                    text_manager.add_text(f"{game.point_1 + point}", (0, 0, 0), 70, 140, 50, "score1")
                    game.point_1 += point
                else:
                    if point == 1:
                        game.point_2 = game.save_2 - 1
                    text_manager.remove_text("score2")
                    text_manager.add_text(f"{game.point_2 + point}", (0, 0, 0), 70, 830, 50, "score2")
                    game.point_2 += point
                dice.round_ended = True
                dice.point = point
                cont = useful.Text_Button("Продолжить", (430, 300), 50, screen)
                save_btn = useful.Text_Button("Сохранить очки", (430, 400), 40, screen)
        text_manager.update()
        all_sprites.draw(screen)
        all_sprites.update()
        if game.point_1 >= 100:
            round_is_play = False
            text_manager.add_text("Игрок 1 победил", (0, 0, 0 ), 50, 430, 300, "win")
            play_btn = Button((510, 200), "play2.png", (170, 100), all_sprites)
            game.point_1 = 0
            game.point_2 = 0
            game.save_2 = 0
            game.save_1 = 0
            text_manager.remove_text("score1")
            text_manager.add_text(f"{0}", (0, 0, 0), 70, 140, 50, "score1")
            dice.round_ended = False
        elif game.point_2 >= 100:
            round_is_play = False
            text_manager.add_text("Игрок  победил", (0, 0, 0), 50, 430, 300, "win")
            play_btn = Button((490, 200), "play2.png", (170, 100), all_sprites)
            game.point_1 = 0
            game.point_2 = 0
            game.save_2 = 0
            game.save_1 = 0
            text_manager.remove_text("score2")
            text_manager.add_text(f"{0}", (0, 0, 0), 70, 830, 50, "score2")
            dice.round_ended = False
        elif dice.round_ended and round_is_play:
            cont.show()
            save_btn.show()
        if round_is_play:
            dice_group.draw(screen)
            dice_group.update()
        pygame.display.flip()
        screen.fill((255, 255, 255))
        clock.tick(FPS)
    




