import numpy as np
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


board = create_board()
game_over = False
turn = 0
piece = 1


while not game_over:
    print_board(board)
    if turn % 2 == 0:
        col = get_selection('one')
        if is_valid_location(board, col):
            piece = 1
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)

    else:
        col = get_selection('two')
        if is_valid_location(board, col):
            piece = 2
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)

    turn += 1
    if turn > 6:
        if winning_move(board, piece):
            print(f'Player {piece} wins!')
            print_board(board)
            game_over = True
