import sys

import pygame

pygame.init()

WHITE = "white"
BLACK = "black"


def chess_loop(screen):
    """screen -- тот, на котором обычно рисуем """

    def correct_coords(row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def opponent(color):
        if color == WHITE:
            return BLACK
        return WHITE

    class Board:
        def __init__(self):
            self.color = WHITE
            self.w_figures_dead_count = 0
            self.b_figures_dead_count = 0
            self.field = []
            for row in range(8):
                self.field.append([None] * 8)
            self.field[0] = [
                Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
                King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
            ]
            self.field[1] = [
                Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
                Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
            ]
            self.field[6] = [
                Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
                Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
            ]
            self.field[7] = [
                Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
                King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
            ]

        def current_player_color(self):
            return self.color

        def cell(self, row, col):
            piece = self.field[row][col]
            if piece is None:
                return '  '
            color = piece.get_color()
            c = 'w' if color == WHITE else 'b'
            return c + piece.char()

        def move_piece(self, row, col, row1, col1):
            """Переместить фигуру из точки (row, col) в точку (row1, col1).
            Если перемещение возможно, метод выполнит его и вернёт True.
            Если нет --- вернёт False"""

            if not correct_coords(row, col) or not correct_coords(row1, col1):
                return False
            if row == row1 and col == col1:
                return False  # нельзя пойти в ту же клетку
            piece = self.field[row][col]
            if piece is None:
                return False
            if piece.get_color() != self.color:
                return False

            if not piece.can_move(self, row, col, row1, col1):
                return False
            self.field[row][col] = None  # Снять фигуру.
            piece.is_moved_once = True
            if self.field[row1][col1]:
                if self.field[row1][col1].color == WHITE:
                    self.field[row1][col1].sprite.image = \
                        pygame.transform.scale(
                            self.field[row1][col1].sprite.image, (20, 20))
                    self.field[row1][col1].sprite.move(
                        (630 - 560) // 2 + 570 + self.w_figures_dead_count
                        * 20, 575)
                    self.w_figures_dead_count += 1
                else:
                    self.field[row1][col1].sprite.image = \
                        pygame.transform.scale(
                            self.field[row1][col1].sprite.image, (20, 20))
                    self.field[row1][col1].sprite.move(
                        (630 - 560) // 2 + 570 + self.b_figures_dead_count
                        * 20, 45)
                    self.b_figures_dead_count += 1
                # self.field[row1][col1].sprite.kill()
            self.field[row1][col1] = piece  # Поставить на новое место.
            new_sprite_coords = board_to_window_coords(col1, row1)
            piece.move_sprite(new_sprite_coords[0] + 5, new_sprite_coords[1] + 5)
            self.color = opponent(self.color)
            return True

        def is_under_attack(self, row1, col1, color):
            """Проверяются все возможные ходы для всех фигур нужного цвета"""
            i1 = 0
            for i in self.field:
                j1 = 0
                for j in i:
                    if not (j is None):
                        if j.color == color:
                            if j.can_move(self, i1, j1, row1, col1,
                                          is_THIS_piece_moving=False):
                                return True
                    j1 += 1
                i1 += 1
            return False

        def get_piece(self, row, col):
            return self.field[row][col]

        def move_and_promote_pawn(self, row, col, row1, col1, char):
            if not isinstance(self.field[row][col], Pawn):
                return False
            color = self.field[row][col].color
            if not correct_coords(row1, col1) or not correct_coords(row, col):
                return False
            if self.field[row][col].can_move(self, row, col, row1, col1) or \
                    self.field[row][col].can_attack(self, row, col, row1,
                                                    col1):
                if self.field[row][col].color == 1 and row1 == 7 or \
                        self.field[row][col].color == 2 and row1 == 0:
                    self.field[row][col] = None
                    if char == 'Q':
                        self.field[row1][col1] = Queen(color,
                                                       is_moved_once=True)
                    elif char == 'R':
                        self.field[row1][col1] = Rook(color,
                                                      is_moved_once=True)
                    elif char == 'N':
                        self.field[row1][col1] = Knight(color,
                                                        is_moved_once=True)
                    elif char == 'B':
                        self.field[row1][col1] = Bishop(color,
                                                        is_moved_once=True)
                    self.color = opponent(self.color)
                    return True
            return False

        def castling0(self):
            i = 0 if self.color == WHITE else 7
            king, rook = self.field[i][4], self.field[i][0]
            if isinstance(king, King) and isinstance(rook, Rook):
                if (not king.is_moved_once) and (not rook.is_moved_once):
                    if self.field[i][1] == self.field[i][2] == self.field[i][
                        3] \
                            is None:
                        self.field[i][4], self.field[i][0] = None, None
                        self.field[i][3], self.field[i][2] = rook, king
                        self.color = opponent(self.color)
                        return True
            return False

        def castling7(self):
            i = 0 if self.color == WHITE else 7
            king, rook = self.field[i][4], self.field[i][7]
            if isinstance(king, King) and isinstance(rook, Rook):
                if (not king.is_moved_once) and (not rook.is_moved_once):
                    if self.field[i][6] == self.field[i][5] is None:
                        self.field[i][4], self.field[i][7] = None, None
                        self.field[i][5], self.field[i][6] = rook, king
                        self.color = opponent(self.color)
                        return True
            return False

    class Pawn:
        def __init__(self, color, is_moved_once=False):
            self.color = color
            self.is_moved_once = is_moved_once
            self.sprite = None

        def set_sprite(self, sprite):
            self.sprite = sprite

        def move_sprite(self, x, y):
            self.sprite.rect.x = x
            self.sprite.rect.y = y

        def get_color(self):
            return self.color

        def char(self):
            return 'P'

        def can_move(self, board, row, col, row1, col1,
                     is_THIS_piece_moving=True):
            if self.can_attack(board, row, col, row1, col1):
                return True

            # Пешка может ходить только по вертикали
            # "взятие на проходе" не реализовано
            if col != col1:
                return False

            # Пешка может сделать из начального положения ход на 2 клетки
            # вперёд, поэтому поместим индекс начального ряда в start_row.
            if self.color == WHITE:
                direction = 1
                start_row = 1
            else:
                direction = -1
                start_row = 6

            # ход на 1 клетку
            if row + direction == row1 and board.field[row1][col1] is None:
                return True

            # ход на 2 клетки из начального положения
            if (row == start_row
                    and row + 2 * direction == row1
                    and board.field[row1][col1] is None
                    and board.field[row1 + direction][col] is None):
                return True
            return False

        def can_attack(self, board, row, col, row1, col1):
            direction = 1 if (self.color == WHITE) else -1
            if board.field[row1][col1] is None:
                return False
            return (row + direction == row1
                    and (col + 1 == col1 or col - 1 == col1)
                    and board.field[row1][col1].color != self.color)

    class Queen:
        def __init__(self, color, is_moved_once=False):
            self.color = color
            self.is_moved_once = is_moved_once
            self.sprite = None

        def set_sprite(self, sprite):
            self.sprite = sprite

        def move_sprite(self, x, y):
            self.sprite.rect.x = x
            self.sprite.rect.y = y

        def set_position(self, row, col):
            self.row = row
            self.col = col

        def char(self):
            return 'Q'

        def get_color(self):
            return self.color

        def can_move(self, board, row, col, row1, col1,
                     is_THIS_piece_moving=True):
            if not correct_coords(row, col):
                return False
            if row == row1 and col == col1:
                return False
            # движение по вертикали
            if col == col1:
                step = 1 if (row1 >= row) else -1
                for r in range(row + step, row1 + step, step):
                    # если это финальная точка
                    if r == row1 and not (board.field[row1][col1] is None):
                        if board.field[row1][col1].color != self.color:
                            return True
                        return False
                    # если на пути встречается фигура
                    if not board.field[r][col1] is None:
                        return False
                return True
            # движение по горизонтали
            if row == row1:
                step = 1 if (col1 >= col) else -1
                for c in range(col + step, col1 + step, step):
                    # если это финальная точка
                    if c == col1 and not (board.field[row1][col1] is None):
                        if board.field[row1][col1].color != self.color:
                            return True
                        return False
                    # если на пути встречается фигура
                    if not board.field[row1][c] is None:
                        return False
                return True
            if abs(col1 - col) == abs(row1 - row):
                step_v = 1 if row1 >= row else -1
                step_h = 1 if col1 >= col else -1
                r, c = row + step_v, col + step_h
                while (r != row1 + step_v) and (c != col1 + step_h):
                    if c == col1 and r == row1 and not (
                            board.field[row1][col1]
                            is None):
                        if board.field[row1][col1].color != self.color:
                            return True
                        return False
                    if not board.field[r][c] is None:
                        return False
                    r, c = r + step_v, c + step_h
                return True
            return False

    class Rook:
        def __init__(self, color, is_moved_once=False):
            self.color = color
            self.is_moved_once = is_moved_once
            self.sprite = None

        def set_sprite(self, sprite):
            self.sprite = sprite

        def move_sprite(self, x, y):
            self.sprite.rect.x = x
            self.sprite.rect.y = y

        def get_color(self):
            return self.color

        def char(self):
            return 'R'

        def can_move(self, board, row, col, row1, col1,
                     is_THIS_piece_moving=True):
            if not correct_coords(row, col):
                return False
            if row == row1 and col == col1:
                return False
            # Невозможно сделать ход в клетку,
            # которая не лежит в том же ряду или столбце клеток.
            if row != row1 and col != col1:
                return False
            # движение по вертикали
            if col == col1:
                step = 1 if (row1 >= row) else -1
                for r in range(row + step, row1 + step, step):
                    # если это финальная точка
                    if r == row1 and not (board.field[row1][col1] is None):
                        if board.field[row1][col1].color != self.color:
                            return True
                        return False
                    # если на пути встречается фигура
                    if not board.field[r][col1] is None:
                        return False
                return True
            # движение по горизонтали
            if row == row1:
                step = 1 if (col1 >= col) else -1
                for c in range(col + step, col1 + step, step):
                    # если это финальная точка
                    if c == col1 and not (board.field[row1][col1] is None):
                        if board.field[row1][col1].color != self.color:
                            return True
                        return False
                    # если на пути встречается фигура
                    if not board.field[row1][c] is None:
                        return False
                return True
            return False

        def can_attack(self, board, row, col, row1, col1):
            return self.can_move(board, row, col, row1, col1)

    class Knight:
        def __init__(self, color, is_moved_once=False):
            self.color = color
            self.is_moved_once = is_moved_once
            self.sprite = None

        def set_sprite(self, sprite):
            self.sprite = sprite

        def move_sprite(self, x, y):
            self.sprite.rect.x = x
            self.sprite.rect.y = y

        def set_position(self, row, col):
            self.row = row
            self.col = col

        def char(self):
            return 'N'

        def get_color(self):
            return self.color

        def can_move(self, board, row, col, row1, col1,
                     is_THIS_piece_moving=True):
            if not correct_coords(row, col):
                return False
            if abs(col1 - col) == 2 and abs(row1 - row) == 1:
                if board.field[row1][col1] is None:
                    return True
                if board.field[row1][col1].color != self.color:
                    return True
            if abs(col1 - col) == 1 and abs(row1 - row) == 2:
                if board.field[row1][col1] is None:
                    return True
                if board.field[row1][col1].color != self.color:
                    return True
            return False

    class Bishop:
        def __init__(self, color, is_moved_once=False):
            self.color = color
            self.is_moved_once = is_moved_once
            self.sprite = None

        def set_sprite(self, sprite):
            self.sprite = sprite

        def move_sprite(self, x, y):
            self.sprite.rect.x = x
            self.sprite.rect.y = y

        def set_position(self, row, col):
            self.row = row
            self.col = col

        def char(self):
            return 'B'

        def get_color(self):
            return self.color

        def can_move(self, board, row, col, row1, col1,
                     is_THIS_piece_moving=True):
            if not correct_coords(row, col):
                return False
            if row == row1 and col == col1:
                return False
            if abs(col1 - col) == abs(row1 - row):
                step_v = 1 if row1 >= row else -1
                step_h = 1 if col1 >= col else -1
                r, c = row + step_v, col + step_h
                while (r != row1 + step_v) and (c != col1 + step_h):
                    if c == col1 and r == row1 and not (
                            board.field[row1][col1]
                            is None):
                        if board.field[row1][col1].color != self.color:
                            return True
                        return False
                    if not board.field[r][c] is None:
                        return False
                    r, c = r + step_v, c + step_h
                return True
            return False

    class King:
        def __init__(self, color, is_moved_once=False):
            self.color = color
            self.is_moved_once = is_moved_once
            self.sprite = None

        def set_sprite(self, sprite):
            self.sprite = sprite

        def move_sprite(self, x, y):
            self.sprite.rect.x = x
            self.sprite.rect.y = y

        def set_position(self, row, col):
            self.row = row
            self.col = col

        def char(self):
            return 'K'

        def get_color(self):
            return self.color

        def can_move(self, board, row, col, row1, col1,
                     is_THIS_piece_moving=True):
            if not correct_coords(row, col):
                return False
            if is_THIS_piece_moving:
                if board.is_under_attack(row1, col1, opponent(self.color)):
                    return False
            if (abs(col1 - col) == abs(row1 - row) == 1) and (
                    board.field[row1][col1] is None):
                return True
            if abs(col - col1) == 1 and row == row1 and board.field[row1][
                col1] is None:
                return True
            if abs(row - row1) == 1 and col == col1 and board.field[row1][
                col1] is None:
                return True
            return False

    all_figures = pygame.sprite.Group()

    class FigureSprite(pygame.sprite.Sprite):
        def __init__(self, image_name, x, y):
            super(FigureSprite, self).__init__(all_figures)
            self.image = pygame.image.load(image_name)
            self.image = self.image.convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
            self.rect = pygame.Rect((x, y, 70, 70))

        def move(self, x, y):
            self.rect.x, self.rect.y = x, y

    screen_rect = screen.get_rect()
    screen_copy = pygame.Surface((screen_rect.w, screen_rect.h))
    screen_copy.blit(screen, (0, 0))
    screen.fill((0, 0, 0))

    def draw_board(screen, board_width, square_width, indent=None):
        if indent is None:
            indent = (630 - board_width) // 2
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, pygame.Color("#333231"),
                         (indent, indent, board_width, board_width))
        # изначальная заливка тёмная, рисует светлые квадраты
        for y in range(board_width + indent - square_width, -1 + indent,
                       -square_width):
            for x in range(indent, board_width + indent, square_width):
                f = 1 if (8 % 2 == 1) else 0
                if (y // square_width) % 2 == 0:
                    if (x // square_width) % 2 == (not f):
                        continue
                else:
                    if (x // square_width) % 2 == f:
                        continue
                screen.fill(
                    pygame.Color("#565555"),
                    (x, y, square_width, square_width))

    def window_pos_to_board(mouse_x, mouse_y, indent=None):
        if indent is None:
            indent = (630 - 560) // 2  # 630 - window size, 560 - board size
        if mouse_x < indent or mouse_x > 560 + indent or \
                mouse_y < indent or mouse_y > 560 + indent:
            return None
        x = (mouse_x - indent) // 70  # 70 - cell size
        y = (mouse_y - indent) // 70
        return x, y

    def board_to_window_coords(x, y, indent=None):
        if indent is None:
            indent = (630 - 560) // 2  # 630 - window size, 560 - board size
        wnd_x = x * 70 + indent
        wnd_y = y * 70 + indent
        return wnd_x, wnd_y

    any_piece_chosen = False
    chosen_piece = None
    piece_cell = None

    board = Board()
    b_b_im_name = "games/data/b_bishop_png_128px.png"
    b_k_im_name = "games/data/b_king_png_128px.png"
    b_n_im_name = "games/data/b_knight_png_128px.png"
    b_p_im_name = "games/data/b_pawn_png_128px.png"
    b_q_im_name = "games/data/b_queen_png_128px.png"
    b_r_im_name = "games/data/b_rook_png_128px.png"
    w_b_im_name = "games/data/w_bishop_png_128px.png"
    w_k_im_name = "games/data/w_king_png_128px.png"
    w_n_im_name = "games/data/w_knight_png_128px.png"
    w_p_im_name = "games/data/w_pawn_png_128px.png"
    w_q_im_name = "games/data/w_queen_png_128px.png"
    w_r_im_name = "games/data/w_rook_png_128px.png"

    figure_images = {
        "bB": b_b_im_name,
        "bK": b_k_im_name,
        "bN": b_n_im_name,
        "bP": b_p_im_name,
        "bQ": b_q_im_name,
        "bR": b_r_im_name,
        "wB": w_b_im_name,
        "wK": w_k_im_name,
        "wN": w_n_im_name,
        "wP": w_p_im_name,
        "wQ": w_q_im_name,
        "wR": w_r_im_name
    }

    def create_sprites():
        for i in range(len(board.field)):
            for j in range(len(board.field[i])):
                piece = board.field[i][j]
                wnd_coords = board_to_window_coords(j, i)
                if piece is not None:
                    sprite = FigureSprite(figure_images[board.cell(i, j)],
                                          wnd_coords[0] + 5, wnd_coords[1] + 5)
                    piece.set_sprite(sprite)
    create_sprites()

    cells_to_move = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == 13:
                    print('123132')
                    for sp in all_figures:
                        sp.kill()
                    board = Board()
                    create_sprites()
            if event.type == pygame.MOUSEBUTTONDOWN:
                draw_board(screen, 560, 70)
                all_figures.draw(screen)
                coords = window_pos_to_board(*event.pos)
                if coords is not None:
                    if not any_piece_chosen:
                        piece = board.field[coords[1]][coords[0]]
                        chosen_piece = piece
                        piece_cell = (coords[1], coords[0])
                        if piece:
                            if not any_piece_chosen:
                                any_piece_chosen = True
                            cells_to_move = []
                            for i in range(len(board.field)):
                                for j in range(len(board.field[i])):
                                    if piece.can_move(board, coords[1],
                                                      coords[0],
                                                      j, i):
                                        wnd_coords = board_to_window_coords(i,
                                                                            j)
                                        pygame.draw.circle(
                                            screen, (50, 150, 50, 50),
                                            (wnd_coords[0] + 35,
                                             wnd_coords[1] + 35), 10)
                                        cells_to_move.append((i, j))
                    else:
                        piece = board.field[coords[1]][coords[0]]
                        if coords not in cells_to_move:
                            any_piece_chosen = False
                            chosen_piece = None
                            cells_to_move = []
                            continue
                        if piece is not None:
                            if piece.color != chosen_piece.color:
                                if coords in cells_to_move:
                                    board.move_piece(*piece_cell, coords[1],
                                                     coords[0])
                                    any_piece_chosen = False
                                    chosen_piece = None
                                    cells_to_move = []
                        else:
                            if coords in cells_to_move:
                                board.move_piece(*piece_cell, coords[1],
                                                 coords[0])
                                any_piece_chosen = False
                                chosen_piece = None
                                cells_to_move = []
        if not any_piece_chosen:
            draw_board(screen, 560, 70)
        all_figures.draw(screen)
        pygame.display.flip()

#
# screen = pygame.display.set_mode((1120, 630))
# chess_loop(screen)
