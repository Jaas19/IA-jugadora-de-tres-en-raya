AI_INPUT = [0,0,1]
PLAYER_INPUT = [0,1,0]
EMPTY_INPUT = [1,0,0]

board = [list(EMPTY_INPUT) for _ in range(9)]

# Función ejecutada para comprobar si se continua el juego
def check_empty_tiles(board):
    for tile in board:
        if tile == EMPTY_INPUT:
            return True
    return False

# Función ejecutada en cada movimiento
def check_board(board):
    rows = [
        board[0:3],
        board[3:6],
        board[6:9],
        board[0::3],
        board[1::3],
        board[2::3],
        board[0::4],
        board[2:7:2]
    ]
    for row in rows:
        if row[0] == row[1] == row[2] and row[0] != EMPTY_INPUT:
            if row[0] == AI_INPUT:
                return +10
            elif row[0] == PLAYER_INPUT:
                return -10
        else:
            continue
    return 0

def change_board(position, movement):
    if board[position] != EMPTY_INPUT:
        return -100
    else:
        board[position] = list(movement)
        return check_board(board)

def restart_board():
    global board
    board = [list(EMPTY_INPUT) for _ in range(9)]