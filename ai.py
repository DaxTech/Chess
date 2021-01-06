
from pieces import *

def checkmate(board):
    for i in range(8):
        for j in range(8):
            if type(board[i][j]) == King:
                king = board[i][j]
                if king.check(board) and not king.available_moves(board):
                    team = king.get_team_pieces(board)
                    if not team:
                        return True
                    counts = 0
                    for piece in team:
                        if not piece.available_moves(board):
                            counts += 1
                    if counts == len(team):
                        return True
    return False

def stalemate(board, turn):
    turn = 'black' if turn else 'white'
    counts = 0
    for i in range(8):
        for j in range(8):
            if not type(board[i][j]) == int:
                counts += 1
    if counts == 2:
        return True

    for i in range(8):
        for j in range(8):
            if type(board[i][j]) == King and board[i][j].color == turn:
                king = board[i][j]
                if king.check(board) or king.available_moves(board):
                    return False
                team = king.get_team_pieces(board)
                if not team:
                    return True
                for piece in team:
                    if piece.available_moves(board):
                        return False
                return True

def terminal_state(board, turn):
    """Returns True if the current state is checkmate or stalemate."""
    if checkmate(board) or stalemate(board, turn):
        return True
    return False

def doubled_pawns(board, piece):
    x = piece.current_pos[1]
    counts = 0
    for i in range(1, 7):
        y = i * piece.view
        if type(board[y][x]) == Pawn and board[y][x].color == piece.color:
            counts +=1
    if counts >= 2:
        return True
    return False


def heuristic(board, turn):
    """Returns value of the board."""
    if checkmate(board):
        return float('-inf') if not turn else float('inf')
    if stalemate(board, turn):
        return 0

    w = {'M': 0, 'D': 0, 'S': 0}  # w = white
    b = {'M': 0, 'D': 0, 'S': 0}  # b = black

    for i in range(8):
        for j in range(8):
            if not type(board[i][j]) == int:
                p = board[i][j]  # p means piece
                if p.color == 'white':
                    w[p.letter] = w.get(p.letter, 0) + 1
                    if type(p) == Pawn:
                        if doubled_pawns(board, p):
                            w['D'] += 1
                        if not p.available_moves(board):
                            w['S'] += 1
                            continue
                    w['M'] += len(p.available_moves(board))

                else:
                    b[p.letter] = b.get(p.letter, 0) + 1
                    if type(p) == Pawn:
                        if doubled_pawns(board, p):
                            b['D'] += 1
                        if not p.available_moves(board):
                            b['S'] += 1
                            continue
                    b['M'] += len(p.available_moves(board))
    return calculate_results(w, b, turn)

def calculate_results(w_dict, b_dict, turn):
    n = -1 if not turn else 1
    keys = ['K','Q','R','B','N','P','S','D','M']
    keys2 = [200, 9, 5, 3, 3, 1, -0.5, -0.5, 0.1]
    result = 0
    for k, k2 in zip(keys, keys2):
        if turn:
            result += (b_dict.get(k, 0) - w_dict.get(k, 0)) * k2
        else:
            result += (w_dict.get(k, 0) - b_dict.get(k, 0)) * k2
    return result * n



def get_pieces(board, color='black'):
    """Returns list all team pieces in the board."""
    p = []
    for i in range(8):
        for j in range(8):
            if not (type(board[i][j]) == int) and board[i][j].color == color:
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


def alpha_beta_max(board, depth, alpha=(None, None, float('-inf')),
                  beta=(None, None, float('inf')), turn=False):
    res = None
    if depth == 0 or terminal_state(board, turn):
        return None, None, heuristic(board, turn)
    for piece in get_pieces(board):
        for move in piece.available_moves(board):
            position = piece.current_pos
            transition(board,piece, position, move)  # making move.
            v2 = alpha_beta_min(board, depth - 1, alpha=alpha, beta=beta)[2]
            go_back(board, piece, position, move)  # unmaking move.
            if v2 >= beta[2]:  # min already has a better move than this one.
                beta = move, piece, beta[2]
            if v2 > alpha[2]:  # this is the best max can do.
                alpha = move, piece, v2
                res = alpha
    if not res:
        return alpha
    return res


def alpha_beta_min(board, depth, alpha=(None, None, float('-inf')),
                   beta=(None, None, float('inf')), turn=True):
    res = None
    if depth == 0 or terminal_state(board, turn):
        return None, None, heuristic(board, turn)
    for piece in get_pieces(board, color='white'):
        for move in piece.available_moves(board):
            position = piece.current_pos
            transition(board, piece, position, move)
            v2 = alpha_beta_min(board, depth - 1, alpha=alpha, beta=beta)[2]
            go_back(board, piece, position, move)
            if v2 <= alpha[2]:  # max already has a better move than this one.
                alpha = move, piece, alpha[2]
                return alpha
            if v2 < beta[2]:
                beta = move, piece, v2
                res = beta
    if not res:
        return beta
    return res

def format_board():
    # REDO - LET THE PIECES BE SETTLED ON A FOR LOOP, WE DON'T CARE ABOUT CREATING VARIABLES FOR THEM.
    board = [[0 if (z+e) % 2 == 0 else -1 for z in range(8)] for e in range(8)]
    for i in range(8):
        board[1][i] = Pawn('black', current_pos=(1, i))
        board[6][i] = Pawn('white', view=-1, current_pos=(6, i))
    for i in range(8):
        if i == 0 or i == 7:
            board[0][i] = Rook('black', current_pos=(0, i))
            board[7][i] = Rook('white', current_pos=(7, i))
        if i == 1 or i == 6:
            board[0][i] = Knight('black', current_pos=(0, i))
            board[7][i] = Knight('white', current_pos=(7, i))
        if i == 2 or i == 5:
            board[0][i] = Bishop('black', current_pos=(0, i))
            board[7][i] = Bishop('white', current_pos=(7, i))
        if i == 3:
            board[0][i] = Queen('black', current_pos=(0, i))
            board[7][i] = Queen('white', current_pos=(7, i))
        if i == 4:
            board[0][i] = King('black', current_pos=(0, i))
            board[7][i] = King('white', current_pos=(7, i))

    return board

# test = format_board()
# test[1][4].move(test, (3, 4))
# test[0][5].move(test, (1, 4))
# test[0][6].move(test, (2, 5))
# transition(test, test[0][4], (0, 4), (0, 6))
# #go_back(test, test[0][6], (0, 4), (0, 6))
# for i in range(8):
#     for j in range(8):
#         if not type(test[i][j]) == int:
#             print(test[i][j].score,'|', end = '')
#         else:
#             print(test[i][j],'|', end = '')
#     print()
