
from pieces import *


def terminal_state(board):
    """Returns True if the current state is checkmate or stalemate."""
    pass


def heuristic(board):
    """Returns value of the board."""
    pass


def get_pieces(board, color='black'):
    """Returns list all team pieces in the board."""
    p = []
    for i in range(8):
        for j in range(8):
            if not (type(board[i][j]) == int or board[i][j].color == color):
                p.append(board[i][j])
    return p


def transition(board, piece, cur_pos, action):
    y, x = action
    cur_y, cur_x = cur_pos
    if not type(board[y][x]) == int:
        temp = board[y][x]
        temp.current_pos = cur_pos
    else:
        temp = 0 if (cur_y+cur_x) % 2 == 0 else -1
    board[y][x] = piece
    board[cur_y][cur_x] = temp
    piece.current_pos = action


def go_back(board, piece, cur_pos, action):
    y, x = action
    cur_y, cur_x = cur_pos
    if not type(board[cur_y][cur_x]) == int:
        temp = board[cur_y][cur_x]
        temp.current_pos = action
    else:
        temp = 0 if (y+x) % 2 == 0 else -1
    board[cur_y][cur_x] = piece
    board[y][x] = temp
    piece.current_pos = cur_pos


# TODO.
def maximizer(board, depth):
    if depth == 0 or terminal_state():
        return heuristic(board)

    v = float('-inf')
    for piece in get_pieces(board):
        for move in piece.available_moves(board):
            position = piece.current_pos
            v2 = max(v, minimizer(transition(board,piece, position, move), depth))
            if not v2 == v:
                res = move


def minimizer(board, depth):
    if depth == 0 or terminal_state():
        return heuristic(board)

    v = float('inf')
    for piece in get_pieces(board):
        for move in piece.available_moves(board):
            position = piece.current_pos
            v2 = min(v, minimizer(transition(board, piece, position, move), depth))
            if not v2 == v:
                res = move
