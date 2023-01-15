import sys

import pygame

pygame.init()


def space_invaders_loop(screen):
    BLUE = pygame.Color('blue')
    RED = pygame.Color('red')
    GREEN = pygame.Color('green')

    with open("data/space_invaders_levels.txt", 'rt') as levels_file:
        data = levels_file.readlines()
        levels = [[j.split(",") for j in i.strip('\n').split(";")]
                  for i in data]
    last_level = levels[-1]
    current_level = 9

    class EnemyGroup(pygame.sprite.Group):
        def __init__(self):
            super(EnemyGroup, self).__init__()
            self.enemies = [[], [], [], [], [], [], [], [], [], [], []]
            self.direction = 1

        def my_add(self, enemy, col):
            self.enemies[col].append(enemy)
            enemy.row = len(self.enemies[col]) - 1
            self.add(enemy)
            self.set_shooters()

        def change_direction(self):
            self.direction = self.direction * -1
            for sprite in self.sprites():
                sprite.rect = sprite.rect.move(
                    (3 + (current_level // 5) * 3) * self.direction, 6)

        def set_shooters(self):
            for i in self.enemies:
                for j in i:
                    j.is_first = False
                if i:
                    i[-1].is_first = True

        def my_clear(self):
            for i in self.sprites():
                i.kill()
            self.enemies = [[], [], [], [], [], [], [], [], [], [], []]
            self.direction = 1
            self.set_shooters()

    all_sprites = pygame.sprite.Group()
    hero1_group = pygame.sprite.Group()
    hero2_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    enemies_group = EnemyGroup()
    shields_group = pygame.sprite.Group()
    rocket_group = pygame.sprite.Group()

    def get_hero_image(color):
        image = pygame.Surface((45, 45))
        pygame.draw.rect(image, color, (0, 12, 45, 9))
        pygame.draw.rect(image, color, (3, 9, 39, 3))
        pygame.draw.rect(image, color, (0, 12, 45, 9))
        pygame.draw.rect(image, color, (18, 3, 9, 6))
        pygame.draw.rect(image, color, (21, 0, 3, 3))
        image.set_colorkey(image.get_at((0, 0)))
        return image

    def draw_field():
        pygame.draw.rect(screen, GREEN, (245, 15, 5, 600))
        pygame.draw.rect(screen, GREEN, (870, 15, 5, 600))
        pygame.draw.rect(screen, GREEN, (250, 15, 620, 5))
        pygame.draw.rect(screen, GREEN, (250, 610, 620, 5))

    def draw_heroes_hp():
        font = pygame.font.Font("games/data/DePixelHalbfett.otf", 32)

        text1 = font.render('P1   LIVES:', True, RED)
        screen.blit(text1, (10, 10))
        for i in range(10, 10 + hero2.live_count * 45 +
                           (hero2.live_count - 1) * 10, 55):
            screen.blit(get_hero_image(RED), (i, 50))

        text2 = font.render("P2   LIVES:", True, BLUE)
        for i in range(885, 885 + hero1.live_count * 45 +
                            (hero2.live_count - 1) * 10, 55):
            screen.blit(get_hero_image(BLUE), (i, 50))
        screen.blit(text2, (885, 10))

    def get_enemy_image(difficulty):
        black = pygame.Color("black")
        if difficulty == '0':
            image = pygame.Surface((33, 24))
            image.fill(black)
            pygame.draw.rect(image, GREEN, (0, 6, 33, 15))
            pygame.draw.rect(image, GREEN, (9, 21, 6, 3))
            pygame.draw.rect(image, GREEN, (18, 21, 6, 3))
            pygame.draw.rect(image, GREEN, (6, 0, 3, 3))
            pygame.draw.rect(image, GREEN, (9, 3, 3, 3))
            pygame.draw.rect(image, GREEN, (24, 0, 3, 3))
            pygame.draw.rect(image, GREEN, (21, 3, 3, 3))
            pygame.draw.rect(image, black, (9, 9, 3, 3))
            pygame.draw.rect(image, black, (21, 9, 3, 3))
            pygame.draw.rect(image, black, (3, 15, 3, 6))
            pygame.draw.rect(image, black, (9, 18, 15, 3))
            pygame.draw.rect(image, black, (0, 6, 6, 3))
            pygame.draw.rect(image, black, (0, 9, 3, 3))
            pygame.draw.rect(image, black, (27, 6, 6, 3))
            pygame.draw.rect(image, black, (30, 9, 3, 3))
            pygame.draw.rect(image, black, (27, 15, 3, 6))
        elif difficulty == '1':
            image = pygame.Surface((36, 24))
            image.fill(black)
            pygame.draw.rect(image, GREEN, (12, 0, 12, 3))
            pygame.draw.rect(image, GREEN, (3, 3, 30, 3))
            pygame.draw.rect(image, GREEN, (0, 6, 36, 9))
            pygame.draw.rect(image, black, (9, 9, 6, 3))
            pygame.draw.rect(image, black, (21, 9, 6, 3))
            pygame.draw.rect(image, GREEN, (6, 15, 9, 3))
            pygame.draw.rect(image, GREEN, (21, 15, 9, 3))
            pygame.draw.rect(image, GREEN, (3, 18, 6, 3))
            pygame.draw.rect(image, GREEN, (15, 18, 6, 3))
            pygame.draw.rect(image, GREEN, (27, 18, 6, 3))
            pygame.draw.rect(image, GREEN, (6, 21, 6, 3))
            pygame.draw.rect(image, GREEN, (24, 21, 6, 3))
        elif difficulty == '2':
            image = pygame.Surface((24, 24))
            image.fill(black)
            pygame.draw.rect(image, GREEN, (9, 0, 6, 3))
            pygame.draw.rect(image, GREEN, (6, 3, 12, 3))
            pygame.draw.rect(image, GREEN, (3, 6, 18, 3))
            pygame.draw.rect(image, GREEN, (0, 9, 24, 6))
            pygame.draw.rect(image, black, (6, 9, 3, 3))
            pygame.draw.rect(image, black, (15, 9, 3, 3))
            pygame.draw.rect(image, GREEN, (6, 15, 3, 3))
            pygame.draw.rect(image, GREEN, (15, 15, 3, 3))
            pygame.draw.rect(image, GREEN, (3, 18, 3, 3))
            pygame.draw.rect(image, GREEN, (9, 18, 6, 3))
            pygame.draw.rect(image, GREEN, (18, 18, 3, 3))
            pygame.draw.rect(image, GREEN, (0, 21, 3, 3))
            pygame.draw.rect(image, GREEN, (6, 21, 3, 3))
            pygame.draw.rect(image, GREEN, (15, 21, 3, 3))
            pygame.draw.rect(image, GREEN, (21, 21, 3, 3))
        else:
            print(f'{difficulty=}')
            image = pygame.Surface(36, 24)
        image.set_colorkey(image.get_at((0, 0)))
        return image

    def load_level():
        nonlocal current_level
        current_level += 1
        enemies_group.my_clear()
        for x in range(260 + (600 // 12 - 18), 260 + 600 - 18, 600 // 12):
            col = (x - 260) // (600 // 12)
            for y in range(100 + (200 // 6 - 12), 100 + 200 - 18, 200 // 6):
                row = (y - 100) // (200 // 6)
                enemies_group.my_add(Enemy(
                    x, y, levels[current_level][col][row], col), col)

    def game_over():
        pass

    class Wall(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super(Wall, self).__init__(vertical_walls_group)
            self.rect = pygame.Rect(x, y, w, h)

        def update(self):
            if pygame.sprite.spritecollideany(self, enemies_group):
                enemies_group.change_direction()

    class Hero(pygame.sprite.Sprite):
        def __init__(self, x, y, color, group):
            super(Hero, self).__init__(group, all_sprites)
            self.image = get_hero_image(color)
            self.rect = pygame.Rect(x, y, 45, 45)
            self.live_count = 2
            self.bullet = None

        def move(self, direction):
            if direction in (pygame.K_LEFT, 97):
                self.rect = self.rect.move(-3, 0)
                if self.rect.x < 250:
                    self.rect.x = 250
            if direction in (pygame.K_RIGHT, 100):
                self.rect = self.rect.move(3, 0)
                if self.rect.x > 825:
                    self.rect.x = 825

        def shoot(self):
            if self.bullet is not None:
                return
            self.bullet = Bullet(self.rect.x + 21, self.rect.y - 6, self)

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, cannon):
            super(Bullet, self).__init__(bullets_group, all_sprites)
            self.image = pygame.Surface((3, 6))
            self.image.fill((255, 255, 255))
            self.rect = pygame.Rect(x, y, 3, 6)
            self.cannon = cannon

        def update(self):
            self.rect = self.rect.move(0, -3)
            if self.rect.y < 15:
                self.cannon.bullet = None
                self.kill()
            if pygame.sprite.spritecollide(self, shields_group, True):
                self.rect.y -= 3
                if pygame.sprite.spritecollide(self, shields_group, True):
                    self.rect.y -= 3
                    if pygame.sprite.spritecollide(self, shields_group, True):
                        self.rect.y -= 3
                        pygame.sprite.spritecollide(self, shields_group, True)
                self.cannon.bullet = None
                self.kill()
            enemy_collides = pygame.sprite.spritecollideany(self, enemies_group)
            if enemy_collides:
                self.cannon.bullet = None
                self.kill()
                enemies_group.enemies[enemy_collides.column].pop(enemy_collides.row)
                for i in range(len(enemies_group.enemies[enemy_collides.column])):
                    enemies_group.enemies[enemy_collides.column][i].row = i
                for _ in range(len(enemies_group.enemies)):
                    for j in range(len(enemies_group.enemies)):
                        if not enemies_group.enemies[j]:
                            enemies_group.enemies.pop(j)
                            break
                for i in range(len(enemies_group.enemies)):
                    for j in range(len(enemies_group.enemies[i])):
                        enemies_group.enemies[i][j].column = i
                        enemies_group.enemies[i][j].row = j
                enemy_collides.kill()
                enemies_group.set_shooters()
                print([[j.is_first for j in i] for i in enemies_group.enemies])

    class Shield(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super(Shield, self).__init__(shields_group, all_sprites)
            self.image = pygame.Surface((3, 3))
            self.image.fill(GREEN)
            self.rect = pygame.Rect(x, y, 3, 3)

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y, difficulty, column):
            super(Enemy, self).__init__(enemies_group, all_sprites)
            self.image = get_enemy_image(difficulty)
            self.image = pygame.transform.scale(self.image, (36, 24))
            self.rect = pygame.Rect(x, y, 36, 24)
            self.difficulty = difficulty
            self.column = column
            self.row = None
            self.my_group = enemies_group
            self.is_first = False

        def update(self):
            self.rect = self.rect.move(
                (3 + (current_level // 5) * 3) * self.my_group.direction, 0)
            pygame.sprite.spritecollide(self, shields_group, True)
            if pygame.sprite.spritecollideany(self, bottom_wall_group):
                game_over()

    class Rocket(pygame.sprite.Sprite):
        def __init__(self, x, y, enemy, group):
            super(Rocket, self).__init__(all_sprites, rocket_group)
            self.image = pygame.Surface()

    for x in range(260 + (600 // 5 - 33), 260 + 600 - 33, 600 // 5):
        for x1 in range(x, x + 18, 3):  # 1st layer
            Shield(x1, 500)
            Shield(x1 + 48, 500)
        for _ in range(4):  # 2-5 layers
            for x1 in range(x, x + (3 * (_ + 6)), 3):
                Shield(x1, 500 - (3 * (_ + 1)))
                Shield(x1 + 48 - _ * 3, 500 - (3 * (_ + 1)))
        for _ in range(5):  # 6-10 layers
            for x1 in range(x, x + 66, 3):
                Shield(x1, 500 - 15 - (_ * 3))
        for _ in range(4):
            for x1 in range(x + ((_ + 1) * 3), x + 63 - (_ * 3), 3):
                Shield(x1, 500 - 30 - (_ * 3))

    vertical_walls_group = pygame.sprite.Group()
    left_wall_sprite = Wall(245, 15, 5, 600)
    right_wall_sprite = Wall(870, 15, 5, 600)
    bottom_wall_group = pygame.sprite.Group()
    bottom_wall_sprite = pygame.sprite.Sprite(bottom_wall_group)
    bottom_wall_sprite.rect = pygame.Rect(250, 610, 620, 5)

    hero1 = Hero(710, 560, BLUE, hero1_group)
    hero2 = Hero(410, 560, RED, hero2_group)

    load_level()
    print([[j.is_first for j in i] for i in enemies_group.enemies])

    PLAYERSMOVEEVENT = pygame.USEREVENT + 123
    pygame.time.set_timer(PLAYERSMOVEEVENT, 15)

    BULLETMOVEEVENT = pygame.USEREVENT + 124
    pygame.time.set_timer(BULLETMOVEEVENT, 10)

    ENEMYMOVEEVENT = pygame.USEREVENT + 125
    pygame.time.set_timer(ENEMYMOVEEVENT, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    hero1.move(event.key)
                if event.key in (97, 100):
                    hero2.move(event.key)
                if event.key == 119:
                    hero2.shoot()
                if event.key == pygame.K_UP:
                    hero1.shoot()
            if event.type == PLAYERSMOVEEVENT:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_LEFT]:
                    hero1.move(pygame.K_LEFT)
                if pressed_keys[pygame.K_RIGHT]:
                    hero1.move(pygame.K_RIGHT)
                if pressed_keys[97]:
                    hero2.move(97)
                if pressed_keys[100]:
                    hero2.move(100)
            if event.type == BULLETMOVEEVENT:
                bullets_group.update()
            if event.type == ENEMYMOVEEVENT:
                enemies_group.update()
        screen.fill((0, 0, 0))
        vertical_walls_group.update()
        draw_field()
        draw_heroes_hp()
        all_sprites.draw(screen)
        pygame.display.flip()
