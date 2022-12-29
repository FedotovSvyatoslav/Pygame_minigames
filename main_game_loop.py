import pygame

import games.chess

if __name__ == "__main__":
    pygame.init()
    SIZE = WIDTH, HEIGHT = 1120, 630
    screen = pygame.display.set_mode(SIZE)
    games.chess.chess_loop(screen)
  # !!!
  # основной игровой цикл с выбором игры можно сразу тут, но сами игры сначала в отдельных ветках, потом будем пробовать объединять
  # !!!
