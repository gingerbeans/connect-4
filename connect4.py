import numpy as np
import pygame
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7


def get_selection(player):
    my_number = -1
    first_ask = True
    while not 0 <= my_number <= ROW_COUNT:
        if not first_ask:
            print('Invalid selection.')
        my_number = input(f'Player {player} Make your move (0-{ROW_COUNT}) ')
        try:
            my_number = int(my_number)
        except ValueError:
            my_number = -1
        first_ask = False
    return my_number


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Horizontal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Vertical Win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Positive diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Negative diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


def _draw_piece(color, c, r):
    pygame.draw.circle(
        screen,
        color,
        (
            c * SQUARESIZE + MIDSQUARE,
            height - (r * SQUARESIZE + MIDSQUARE)),
        PIECESIZE
    )


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c*SQUARESIZE + MIDSQUARE, r*SQUARESIZE + SQUARESIZE + MIDSQUARE), PIECESIZE)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                _draw_piece(RED, c, r)
            elif board[r][c] == 2:
                _draw_piece(YELLOW, c, r)
    pygame.display.update()


board = create_board()
game_over = False
turn = 0
piece = 1

pygame.init()

SQUARESIZE = 100
MIDSQUARE = int(SQUARESIZE / 2)
PIECESIZE = MIDSQUARE - 2

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont('monospace', 75)


def draw_top_piece():
    global posx
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
    posx = event.pos[0]
    if turn % 2 == 0:
        pygame.draw.circle(screen, RED, (posx, MIDSQUARE), PIECESIZE)
    elif turn % 2 != 0:
        pygame.draw.circle(screen, YELLOW, (posx, MIDSQUARE), PIECESIZE)


while not game_over:

    for event in pygame.event.get():
        if winning_move(board, piece):
            label = myfont.render(f'Player {piece} wins', 1, RED)
            screen.blit(label, (40, 10))
            pygame.display.update()
            pygame.time.wait(2000)
            game_over = True

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            draw_top_piece()
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn % 2 == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board, col):
                    piece = 1
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, piece)
                    turn += 1

            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board, col):
                    piece = 2
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, piece)
                    turn += 1

            draw_board(board)
            draw_top_piece()
            pygame.display.update()
