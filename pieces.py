#! python3
import pygame

def print_board():
    global board
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0 or board[i][j] == -1:
                print(board[i][j], end='|')
            else:
                print(board[i][j].score, end='|')
                # print(board[i][j].color, end = '|')
        print()


class Queen:
    def __init__(self, color, current_pos=None):
        self.color = color
        self.score = 9
        self.image = 'Pieces\\queen_' + self.color + '.png'
        self.current_pos = current_pos

    def move(self, coordinates):
        global board
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(coordinates):
            return False
        self.current_pos = coordinates
        board[y][x] = self
        board[cur_y][cur_x] = -1 if (cur_y+cur_x) % 2 == 0 else 0

    def validate_move(self, coordinates):
        # STILL MISSING INVALID MOVEMENT BECAUSE PROTECTING KING
        if not self.trajectory(coordinates) or self.is_blocked(coordinates) or self.same_color(coordinates):
            return False
        return True

    def trajectory(self, coordinates):
        y, x = coordinates
        cur_y, cur_x = self.current_pos
        option1 = ((cur_y == y and cur_x != x) or (cur_x == x and cur_y != y))
        option2 = (abs(cur_y - y) == abs(cur_x - x))
        if not (option1 or option2):
            return False
        return True

    def is_blocked(self, coordinates):
        global board
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        # HORIZONTAL/VERTICAL IMPEDIMENT
        ny = 1 if y > cur_y else -1
        nx = 1 if x > cur_x else -1
        if cur_y == y:
            for j in range(cur_x + nx, x, nx):
                if not (board[y][j] == 0 or board[y][j] == -1):
                    return True
        if cur_x == x:
            for i in range(cur_y + ny, y, ny):
                if not (board[i][x] == 0 or board[i][x] == -1):
                    return True
        # DIAGONAL IMPEDIMENT
        ny = 1 if y > cur_y else -1
        nx = 1 if x > cur_x else -1
        iter_y = [e for e in range(cur_y + ny, y + ny, ny)]
        iter_x = [z for z in range(cur_x + nx, x + nx, nx)]
        for i, j in zip(iter_y, iter_x):
            if not (board[i][j] == 0 or board[i][j] == -1) and not (coordinates == (i, j)):
                return True
        return False

    def same_color(self, coordinates):
        global board
        y, x = coordinates
        if not (board[y][x] == -1 or board[y][x] == 0):
            return board[y][x].color == self.color
        return False

    def available_moves(self):
        global board
        moves = []
        for i in range(8):
            for j in range(8):
                if self.validate_move((i, j)) and not (i, j) == self.current_pos:
                    if self.same_color((i, j)) or self.is_check((i, j)):
                        continue
                    moves.append((i, j))
        return moves

    def is_check(self, move):
        global board
        for i in range(8):
            for j in range(8):
                if not (board[i][j] == 0 or board[i][j] == -1) and board[i][j].color == self.color:
                    if type(board[i][j]) == King:
                        if not board[i][j].temporal_move(self, move):
                            return True
                        return False


class Rook:
    def __init__(self, color, current_pos=None):
        self.color = color
        self.score = 5
        self.image = 'Pieces\\rook_' + self.color + '.png'
        self.current_pos = current_pos

    def move(self, coordinates):
        global board
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(coordinates):
            return False
        self.current_pos = coordinates
        board[y][x] = self
        board[cur_y][cur_x] = -1 if (cur_y+cur_x) % 2 == 0 else 0

    def validate_move(self, coordinates):
        # STILL MISSING INVALID MOVEMENT BECAUSE PROTECTING KING
        if not self.trajectory(coordinates) or self.is_blocked(coordinates) or self.same_color(coordinates):
            return False
        return True

    def trajectory(self, coordinates):
        y, x = coordinates
        cur_y, cur_x = self.current_pos
        if (cur_y == y and cur_x != x) or (cur_x == x and cur_y != y):
            return True
        return False

    def is_blocked(self, coordinates):
        global board
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        ny = 1 if y > cur_y else -1
        nx = 1 if x > cur_x else -1
        if cur_y == y:
            for j in range(cur_x + nx, x, nx):
                if not (board[y][j] == 0 or board[y][j] == -1):
                    return True
        if cur_x == x:
            for i in range(cur_y + ny, y, ny):
                if not (board[i][x] == 0 or board[i][x] == -1):
                    return True
        return False

    def same_color(self, coordinates):
        global board
        y, x = coordinates
        if not (board[y][x] == -1 or board[y][x] == 0):
            return board[y][x].color == self.color
        return False

    def available_moves(self):
        global board
        moves = []
        for i in range(8):
            for j in range(8):
                if self.validate_move((i, j)) and not (i, j) == self.current_pos:
                    if self.same_color((i, j)) or self.is_check((i, j)):
                        continue
                    moves.append((i, j))
        return moves

    def is_check(self, move):
        global board
        for i in range(8):
            for j in range(8):
                if not (board[i][j] == 0 or board[i][j] == -1) and board[i][j].color == self.color:
                    if type(board[i][j]) == King:
                        if not board[i][j].temporal_move(self, move):
                            return True
                        return False


class Bishop:
    def __init__(self, color, cells, current_pos=None):
        self.color = color
        self.cells = cells
        self.score = 3.5
        self.image = 'Pieces\\bishop_' + self.color + '.png'
        self.current_pos = current_pos

    def move(self, coordinates):
        global board
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(coordinates):
            return False
        self.current_pos = coordinates
        board[y][x] = self
        board[cur_y][cur_x] = -1 if (cur_y+cur_x) % 2 == 0 else 0

    def validate_move(self, coordinates):
        # STILL MISSING INVALID MOVEMENT BECAUSE PROTECTING KING
        if not self.trajectory(coordinates) or self.is_blocked(coordinates) or self.same_color(coordinates):
            return False
        return True

    def trajectory(self, coordinates):
        y, x = coordinates
        cur_y, cur_x = self.current_pos
        if not (abs(cur_y - y) == abs(cur_x - x)):
            return False
        return True

    def is_blocked(self, coordinates):
        global board
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        ny = 1 if y > cur_y else -1
        nx = 1 if x > cur_x else -1
        iter_y = [e for e in range(cur_y + ny, y + ny, ny)]
        iter_x = [z for z in range(cur_x + nx, x + nx, nx)]
        for i, j in zip(iter_y, iter_x):
            if not (board[i][j] == 0 or board[i][j] == -1) and not (coordinates == (i, j)):
                return True
        return False

    def same_color(self, coordinates):
        global board
        y, x = coordinates
        if not (board[y][x] == -1 or board[y][x] == 0):
            return board[y][x].color == self.color
        return False

    def available_moves(self):
        global board
        moves = []
        for i in range(8):
            for j in range(8):
                if self.validate_move((i, j)) and not (i, j) == self.current_pos:
                    if self.same_color((i, j)) or self.is_check((i, j)):
                        continue
                    moves.append((i, j))
        return moves

    def is_check(self, move):
        global board
        for i in range(8):
            for j in range(8):
                if not (board[i][j] == 0 or board[i][j] == -1) and board[i][j].color == self.color:
                    if type(board[i][j]) == King:
                        if not board[i][j].temporal_move(self, move):
                            return True
        return False


class Knight:
    def __init__(self, color, current_pos=None):
        self.color = color
        self.score = 3
        self.image = 'Pieces\\knight_' + self.color + '.png'
        self.current_pos = current_pos

    def move(self, coordinates):
        global board
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(coordinates):
            return False
        self.current_pos = coordinates
        board[y][x] = self
        board[cur_y][cur_x] = -1 if (cur_y+cur_x) % 2 == 0 else 0

    def validate_move(self, coordinates):
        # STILL MISSING INVALID MOVEMENT BECAUSE PROTECTING KING
        if not self.trajectory(coordinates) or self.same_color(coordinates):
            return False
        return True

    def trajectory(self, coordinates):
        y, x = coordinates
        cur_y, cur_x = self.current_pos
        option1 = (abs(cur_y - y) == 1 and abs(cur_x - x) == 2)
        option2 = (abs(cur_x - x) == 1 and abs(cur_y - y) == 2)
        if option1 or option2:
            return True
        return False

    def same_color(self, coordinates):
        global board
        y, x = coordinates
        if not (board[y][x] == -1 or board[y][x] == 0):
            return board[y][x].color == self.color
        return False

    def available_moves(self):
        global board
        moves = []
        for i in range(8):
            for j in range(8):
                if self.validate_move((i, j)) and not (i, j) == self.current_pos:
                    if self.same_color((i, j)) or self.is_check((i, j)):
                        continue
                    moves.append((i, j))
        return moves

    def is_check(self, move):
        global board
        for i in range(8):
            for j in range(8):
                if not (board[i][j] == 0 or board[i][j] == -1) and board[i][j].color == self.color:
                    if type(board[i][j]) == King:
                        if not board[i][j].temporal_move(self, move):
                            return True
        return False


class Pawn:
    def __init__(self, color, current_pos=None, first_move=True, view=1):
        self.color = color
        self.score = 1
        self.image = 'Pieces\\pawn_' + self.color + '.png'
        self.current_pos = current_pos
        self.first_move = first_move
        self.view = view

    def change_pos(self, coordinates):
        self.current_pos = coordinates

    def move(self, coordinates):
        global board
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(coordinates):
            return False
        if self.first_move:
            self.first_move = False
        self.change_pos(coordinates)
        board[y][x] = self
        board[cur_y][cur_x] = -1 if (cur_y+cur_x) % 2 == 0 else 0

    def validate_move(self, coordinates):
        # STILL MISSING INVALID MOVEMENT BECAUSE PROTECTING KING
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if self.view == 1:
            n = (y - cur_y) == 1 and abs(cur_x - x) == 1
        else:
            n = (y-cur_y) == -1 and abs(cur_x-x) == 1

        exc = self.is_blocked(coordinates) and \
                n and not self.same_color(coordinates)
        if exc:
            return True
        if not self.trajectory(coordinates) or self.is_blocked(coordinates) or self.same_color(coordinates):
            return False
        return True

    def trajectory(self, coordinates):
        y, x = coordinates
        cur_y, cur_x = self.current_pos
        option1 = (self.first_move and (y == (cur_y + 2 * self.view)) and cur_x == x)
        option2 = (y == (cur_y + self.view) and cur_x == x)
        if option1 or option2:
            return True

        return False

    def is_blocked(self, coordinates):
        global board
        y, x = coordinates
        if not (board[y][x] == 0 or board[y][x] == -1):
            return True
        return False

    def same_color(self, coordinates):
        global board
        y, x = coordinates
        if not (board[y][x] == -1 or board[y][x] == 0):
            return board[y][x].color == self.color
        return False

    def available_moves(self):
        global board
        moves = []
        for i in range(8):
            for j in range(8):
                if self.validate_move((i, j)) and not (i, j) == self.current_pos:
                    if self.same_color((i, j)) or self.is_check((i, j)):
                        continue
                    moves.append((i, j))
        return moves

    def is_check(self, move):
        global board
        for i in range(8):
            for j in range(8):
                if not (board[i][j] == 0 or board[i][j] == -1) and board[i][j].color == self.color:
                    if type(board[i][j]) == King:
                        if not board[i][j].temporal_move(self, move):
                            return True
        return False


class King:
    def __init__(self, color, current_pos=None, moved=False):
        self.color = color
        self.score = 10
        self.image = 'Pieces\\king_' + self.color + '.png'
        self.current_pos = current_pos
        self.moved = moved

    def move(self, coordinates):
        global board
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(coordinates):
            return False
        board[y][x] = self
        board[cur_y][cur_x] = -1 if (cur_y+cur_x) % 2 == 0 else 0

    def validate_move(self, coordinates):
        if not self.trajectory(coordinates) or self.same_color(coordinates) or self.unavailable(coordinates):
            return False
        return True

    def trajectory(self, coordinates):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        condition1 = (abs(cur_y - y) == 1 or cur_y == y)
        condition2 = (abs(cur_x - x) == 1 or cur_x == x)
        if condition1 and condition2:
            return True
        return False

    def available_moves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.validate_move((i, j)) and not (i, j) == self.current_pos:
                    if self.same_color((i, j)):
                        continue
                    moves.append((i, j))
        return moves

    def unavailable(self, coordinates):
        if self.check(coordinates):
            return True
        return False

    def same_color(self, coordinates):
        global board
        y, x = coordinates
        if not (board[y][x] == -1 or board[y][x] == 0):
            return board[y][x].color == self.color
        return False

    def check(self, coordinates=None):
        global board
        cur_y, cur_x = self.current_pos
        coordinates = self.current_pos if coordinates is None else coordinates
        y, x = coordinates
        bucket = board[y][x]
        board[y][x] = self
        self.current_pos = coordinates
        board[cur_y][cur_x] = -1 if (cur_y+cur_x) % 2 == 0 else 0
        for i in range(8):
            for j in range(8):
                if not (board[i][j] == -1 or board[i][j] == 0) and not board[i][j].color == self.color:
                    target = board[i][j].available_moves()
                    if coordinates in target:
                        board[cur_y][cur_x] = self
                        board[y][x] = bucket
                        self.current_pos = (cur_y, cur_x)
                        return True
        board[cur_y][cur_x] = self
        board[y][x] = bucket
        self.current_pos = (cur_y, cur_x)
        return False

    def checkmate(self):
        if self.check() and self.available_moves() == []:
            if self.team_pieces()[0]:
                return True
            if self.protect() == []:
                return True
        return False

    def team_pieces(self):
        global board
        t_pieces = []
        for i in range(8):
            for j in range(8):
                if not (board[i][j] == 0 or board[i][j] == -1):
                    if board[i][j].color == self.color and not board[i][j] == self:
                        t_pieces.append(board[i][j])
        if t_pieces == []:
            return True, None
        return False, t_pieces

    def protect(self):
        global board
        protection_moves = []
        for i in range(8):
            for j in range(8):
                if not (board[i][j] == 0 or board[i][j] == -1) and not board[i][j].color == self.color:
                    target = board[i][j].available_moves()
                    target.append(board[i][j].current_pos) # appending current position of the threatening piece
                    if self.current_pos in target: # Check is True
                        team = self.team_pieces()[1]
                        for piece in team:
                            piece_moves = piece.available_moves()
                            for move in piece_moves:
                                if move in target:
                                    if self.temporal_move(piece, move):
                                        protection_moves.append((piece.score, move))
        return protection_moves

    def temporal_move(self, piece, coordinates):
        global board
        y, x = coordinates
        cur_y, cur_x = piece.current_pos
        piece.current_pos = coordinates
        temp = board[y][x]
        board[y][x] = piece
        board[cur_y][cur_x] = -1 if (cur_y+cur_x) % 2 == 0 else 0
        if self.check():
            board[y][x] = temp
            board[cur_y][cur_x] = piece
            piece.current_pos = (cur_y, cur_x)
            return False # Move does not protect the king
        board[y][x] = temp
        board[cur_y][cur_x] = piece
        piece.current_pos = (cur_y, cur_x)
        return True


board = [[0 for i in range(8)] for j in range(8)]
for i in range(8):
    for j in range(8):
        if (i + j) % 2 == 0:
            board[i][j] = -1

