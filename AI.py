from pieces import *
from piece_square_tables import *


def checkmate(board: list, turn: bool):
    """
    Returns True if current state of the board is checkmate, False otherwise.

    Parameters
    ----------
    board: list
        Chess board.
    turn: bool
        True if it's white's turn, False otherwise.
    """
    color = 'white' if turn else 'black'
    for i in range(8):
        for j in range(8):
            if type(board[i][j]) == King and board[i][j].color == color:
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


def stalemate(board: list, turn: bool):
    """
    Returns True if the current state is a draw, False otherwise.

    Parameters
    ----------
    board: list
        Chess board.

    turn: bool
        True if it's white's turn, False otherwise.
    """
    color = 'white' if turn else 'black'
    counts = 0
    for i in range(8):
        for j in range(8):
            if not type(board[i][j]) == int:
                counts += 1
    if counts == 2:
        return True
    for i in range(8):
        for j in range(8):
            if type(board[i][j]) == King and board[i][j].color == color:
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


def terminal_state(board: list, turn: bool):
    """
    Returns True if the current state is checkmate or stalemate.

    Parameters
    ----------
    board: list
        Chess board.
    turn: bool
        True if it's white's turn, False otherwise.
    """
    return checkmate(board, turn) or stalemate(board, turn)


def doubled_pawns(board, piece: Pawn):
    """
    Returns True if there are doubled pawns at the given column.

    Parameters
    ----------
    board: list
        Chess board.
    piece: Pawn
        Pawn object.
    """
    x = piece.current_pos[1]
    counts = 0
    for i in range(1, 7):
        y = i * piece.view
        if type(board[y][x]) == Pawn and board[y][x].color == piece.color:
            counts += 1
    if counts >= 2:
        return True
    return False


def evaluate(board, turn):
    """
    Returns relative value of the board.

    Parameters
    ----------
    board: list
        Chess board.
    turn: bool
        True if it's white's turn, False otherwise.
    """
    if checkmate(board, turn):
        # turn white, and checkmate means black won, turn black, the other way around.
        return float('inf') if turn else float('-inf')
    if stalemate(board, turn):
        return 0
    # M: mobility (amount of available moves), D: doubled pawns, S: blocked pawns
    w = {'M': 0, 'D': 0, 'S': 0}  # w = white
    b = {'M': 0, 'D': 0, 'S': 0}  # b = black
    for i in range(8):
        for j in range(8):
            if not type(board[i][j]) == int:
                p = board[i][j]  # p means piece
                if p.color == 'white':
                    w[p.letter] = w.get(p.letter, 0) + piece_value(p)
                    if type(p) == Pawn:
                        if doubled_pawns(board, p):
                            w['D'] += 1
                        if not p.available_moves(board):
                            w['S'] += 1
                            continue
                    w['M'] += len(p.available_moves(board))
                else:
                    b[p.letter] = b.get(p.letter, 0) + piece_value(p)
                    if type(p) == Pawn:
                        if doubled_pawns(board, p):
                            b['D'] += 1
                        if not p.available_moves(board):
                            b['S'] += 1
                            continue
                    b['M'] += len(p.available_moves(board))
    return calculate_results(w, b, turn)


def piece_value(piece: Piece):
    """
    Returns value of the piece considering its score and position in the board.

    piece: Piece
        Piece object (King, Queen, Rook, Knight, Bishop, Pawn).
    """
    y, x = piece.current_pos
    return piece.score + PIECE_TABLES[piece.color + '_' + piece.letter][y][x]


def calculate_results(w_dict: dict, b_dict: dict, turn: bool):
    """
    Calculates the value of the board, considering the given features.

    Parameters
    ----------
    w_dict: dict
        White dictionary containing values for the white team.
    b_dict: dict
        Black dictionary containing values for the black team.
    turn: bool
        True if it's white's turn, False otherwise.
    """
    n = -1 if turn else 1  # turn=True for white, turn=False for black.
    keys = ['K', 'Q', 'R', 'B', 'N', 'P', 'S', 'D', 'M']
    keys2 = [1, 1, 1, 1, 1, 1, -5, -5, 1]
    result = 0
    for k, k2 in zip(keys, keys2):
        if turn:
            result += (w_dict.get(k, 0) - b_dict.get(k, 0)) * k2
        else:
            result += (b_dict.get(k, 0) - w_dict.get(k, 0)) * k2
    return result * n


def get_pieces(board: list, color='black'):
    """
    Returns list of all team pieces in the board.

    board: list
        Chess board.
    color: str
        Either 'black' or 'white'.
    """
    p = []
    for i in range(8):
        for j in range(8):
            if not (type(board[i][j]) == int) and (board[i][j].color == color):
                p.append(board[i][j])
    return p


def castling(piece: Piece, cur_pos: tuple, action: tuple):
    """Returns True if the given movement is castling, False otherwise

    Parameters
    ----------
    piece: Piece
        Any piece object.
    cur_pos: tuple
        Y, x coordinates for the current position of the given piece.
    action: tuple
        Y, x coordinates for the destination of the given piece.
    """
    if not type(piece) == King:
        return False
    cur_y, cur_x = cur_pos
    y, x = action
    if abs(cur_x - x) == 2 and y == cur_y:
        return True
    return False


def transition(board: list, piece: Piece, cur_pos: tuple, action: tuple):
    """
    Makes temporal move to the board

    Parameters
    ----------
    board: list
        Chess board.
    piece: Piece
        Piece object (any)
    cur_pos: tuple
        Y, x coordinates of the current position of the given piece.
    action: tuple
        Y, x coordinates of the destination for the given piece.
    """
    last_taken = None
    y, x = action  # move to
    cur_y, cur_x = cur_pos  # move from
    if castling(piece, cur_pos, action):
        board[cur_y][cur_x] = 0 if (cur_y + cur_x) % 2 == 0 else -1
        if x == 6:  # short castling
            board[y][x] = piece
            piece.current_pos = action
            # Moving the rook
            temp = board[y][7]
            temp.current_pos = (y, 5)
            board[y][7] = 0 if (y + 7) % 2 == 0 else -1
            board[y][5] = temp
        else:  # x == 2, long castling
            board[y][x] = piece
            piece.current_pos = action
            # Moving the Rook
            temp = board[y][0]
            temp.current_pos = (y, 3)
            board[y][0] = 0 if y % 2 == 0 else -1
            board[y][3] = temp
    else:
        if not type(board[y][x]) == int:
            last_taken = board[y][x]
        board[y][x] = piece
        board[cur_y][cur_x] = 0 if (cur_y + cur_x) % 2 == 0 else -1
        piece.current_pos = action
    return last_taken


def go_back(board: list, piece: Piece, cur_pos: tuple, action: tuple, bucket=None):
    """
    Returns board to its original state after temporal transition

    board: list
        Chess board.
    piece: Piece
        Piece object (any).
    cur_pos: tuple
        y, x coordinates of the current position of the given piece.
    action: tuple
        y, x coordinates of the destination for the given piece.
    bucket: Piece or None
        Piece object of a previous taken piece.
    """
    y, x = action  # actually, is the current_pos
    cur_y, cur_x = cur_pos  # actually, is where we moved to before
    if castling(piece, cur_pos, action):
        board[cur_y][cur_x] = 0 if (cur_y + cur_x) % 2 == 0 else -1
        if cur_x == 6:  # from short castle back to normal
            board[y][x] = piece
            piece.current_pos = action
            # Moving the rook back
            temp = board[y][5]
            temp.current_pos = (y, 7)
            board[y][5] = 0 if (y + 5) % 2 == 0 else -1
            board[y][7] = temp
        else:  # cur_x == 2, from long castle
            board[y][x] = piece  # y and x are always either 0, 4 or 7, 4
            piece.current_pos = action
            # Moving the Rook
            temp = board[y][3]
            temp.current_pos = (y, 0)
            board[y][3] = -1 if (y + 3) % 2 == 0 else -1
            board[y][0] = temp
    else:
        board[y][x] = piece
        if bucket is not None:
            board[cur_y][cur_x] = bucket
        else:
            board[cur_y][cur_x] = 0 if (cur_y + cur_x) % 2 == 0 else -1
        piece.current_pos = action


def alpha_beta(board: list, depth: int, turn: bool, alpha: tuple, beta: tuple):
    """
    Alpha-Beta pruning algorithm, returns best move after search.

    board: list
        Chess board.
    depth: int
        Desired depth of search.
    turn: bool
        True if it's white's turn, False otherwise.
    alpha: tuple
        Tuple containing Piece, move and value of the best move MAX can achieve.
    beta: tuple
        Tuple containing Piece, move and value of the best move MIN can achieve.
    """
    if depth == 0 or terminal_state(board, turn):
        return None, None, evaluate(board, turn)
    cut_off = False
    if turn:
        best_res = None, None, float('inf')
        for piece in get_pieces(board, color='white'):
            if cut_off: break
            for move in piece.available_moves(board):
                pos = piece.current_pos
                bucket = transition(board, piece, pos, move)
                v = alpha_beta(board, depth - 1, False, alpha, beta)[2]
                go_back(board, piece, move, pos, bucket=bucket)
                if v <= best_res[2]:
                    best_res = piece, move, v
                if best_res[2] <= beta[2]:
                    beta = best_res
                if beta[2] <= alpha[2]:
                    cut_off = True
                    break
        return best_res
    else:
        best_res = None, None, float('-inf')
        for piece in get_pieces(board):
            if cut_off:
                break
            for move in piece.available_moves(board):
                pos = piece.current_pos
                bucket = transition(board, piece, pos, move)
                v = alpha_beta(board, depth - 1, True, alpha, beta)[2]
                go_back(board, piece, move, pos, bucket=bucket)
                if v >= best_res[2]:
                    best_res = piece, move, v
                if best_res[2] >= alpha[2]:
                    alpha = best_res
                if beta[2] <= alpha[2]:
                    cut_off = True
                    break
        return best_res
