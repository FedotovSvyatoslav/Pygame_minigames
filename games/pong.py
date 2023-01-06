import pygame
import useful
import menu2
import random
import time


pygame.init()
FPS = 60
SIZE = WIDTH, HEIGHT = 1120, 630
clock = pygame.time.Clock()
ball_group = pygame.sprite.Group()
border_sprites = pygame.sprite.Group()
ball_spawn = pygame.USEREVENT + 1

MOVE = 8


class Ball(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__(ball_group)
        if random.randint(0, 1) == 1:
            self.vx = random.randint(3, 5)
        else:
            self.vx = random.randint(3, 5) * -1
        self.vy = random.randint(-5, 5)
        if self.vy == 0:
            self.vy = -3
        self.image = pygame.Surface((40, 40),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (20, 20), 20)
        self.rect = pygame.Rect(WIDTH//2, HEIGHT//2, 40, 40)

    def update(self, *args):
        if not 0 < self.rect.y < HEIGHT - 40:
            self.vy = self.vy * -1
        if pygame.sprite.spritecollideany(self, border_sprites):
            offx = random.randint(1, 2) if self.vx < 0 else random.randint(1, 2) * -1
            self.vx = self.vx * -1 + offx
        self.rect = self.rect.move(self.vx, self.vy)


class Borders(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__(border_sprites)
        self.x, self.y = pos
        self.image = pygame.Surface((20, 140))
        self.image.fill(pygame.Color("grey"))
        self.rect = pygame.Rect(self.x, self.y, 20, 140)

    def set_pos(self):
        self.rect.y = HEIGHT // 2

    def move(self, y):
        self.rect = self.rect.move(0, y)


class Game:
    def __init__(self):
        self.round_ended = False
        self.point_1 = 0
        self.point_2 = 0

    def play_round(self, ball):
        if ball.rect.x < -40:
            self.score(0, 1)
            return False
        elif ball.rect.x > WIDTH + 20:
            self.score(1, 0)
            return False
        return True

    def score(self, p1, p2):
        self.round_ended = True
        self.point_1 += p1
        self.point_2 += p2
        text_manager.remove_text("p1")
        text_manager.remove_text("p2")
        text_manager.add_text(f"{self.point_1}", pygame.Color("white"), 40, 80, 40, "p1")
        text_manager.add_text(f"{self.point_2}", pygame.Color("white"), 40, 1000, 40, "p2")

    def end_game(self):
        self.point_1 = 0
        self.point_2 = 0
        text_manager.remove_text("p1")
        text_manager.remove_text("p2")
        text_manager.add_text("0", pygame.Color("white"), 40, 80, 40, "p1")
        text_manager.add_text("0", pygame.Color("white"), 40, 1000, 40, "p2")


def start_game(screen):
    global text_manager
    text_manager = useful.Text(screen)
    game = Game()
    border1 = Borders((0, HEIGHT // 2), screen)
    border2 = Borders((WIDTH - 20, HEIGHT // 2), screen)
    screen.fill((0, 0, 0))
    text_manager.add_text("Очки игрока 1", pygame.Color("white"), 40, 10, 10, "sc1")
    text_manager.add_text("Очки игрока 2", pygame.Color("white"), 40, 920, 10, "sc2")
    text_manager.add_text("0", pygame.Color("white"), 40, 80, 40, "p1")
    text_manager.add_text("0", pygame.Color("white"), 40, 1000, 40, "p2")
    running = True
    round_is_run = False
    play_btn = useful.Button((530, 200), "play_2.png", (100, 100), border_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                useful.terminate()
                menu2.menu2(screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    round_is_play = False
                    ball.kill()
                    menu2.menu2(screen)
                    ball_group.empty()
                    border1.kill()
                    border2.kill()
                    border_sprites.empty()
                    useful.terminate()
                    screen.fill((0, 0, 0))
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.click(event.pos):
                    round_is_run = True
                    game.round_ended = False
                    text_manager.remove_text("win")
                    ball = Ball(screen)
                    border1.set_pos()
                    border2.set_pos()
                    play_btn.kill()
                    play_btn.killed = True
        if pygame.key.get_pressed()[pygame.K_w]:
            border1.move(-MOVE)

        if pygame.key.get_pressed()[pygame.K_s]:
            border1.move(MOVE)

        if pygame.key.get_pressed()[pygame.K_UP]:
            border2.move(-MOVE)

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            border2.move(MOVE)

        if round_is_run and not game.round_ended:
            res = game.play_round(ball)
            if game.point_2 == 10:
                game.end_game()
                text_manager.add_text("Игрок 2 победил", pygame.Color("white"), 40, 500, 300, "win")
                round_is_run = False
                game.round_ended = True
                play_btn = useful.Button((530, 200), "play_2.png", (100, 100), border_sprites)
            elif game.point_1 == 10:
                game.end_game()
                text_manager.add_text("Игрок 1 победил", pygame.Color("white"), 40, 500, 300, "win")
                round_is_run = False
                game.round_ended = True
                play_btn = useful.Button((530, 200), "play_2.png", (100, 100), border_sprites)
            if not res and round_is_run:
                game.round_ended = True
                ball.kill()
                ball_group.empty()
                time.sleep(1)
                ball = Ball(screen)
                border1.set_pos()
                border2.set_pos()
                game.round_ended = False

        if round_is_run and not game.round_ended:
            ball_group.draw(screen)
            ball_group.update()

        text_manager.update()
        border_sprites.draw(screen)
        border_sprites.update()
        pygame.display.flip()
        screen.fill((0, 0, 0))
        clock.tick(FPS)







