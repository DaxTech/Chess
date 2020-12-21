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
        print()


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
        board[cur_y][cur_x] = -1 if board[cur_y-1][cur_x] == 0 else 0

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
                    if self.same_color((i, j)):
                        continue
                    moves.append((i, j))
        return moves

    def is_check(self):
        return self


class Bishop:
    def __init__(self, color, cells, current_pos=None):
        self.color = color
        self.cells = cells
        self.score = 3.5
        self.image = 'Pieces\\bishop_'+self.color+'.png'
        self.current_pos = current_pos

    def move(self, coordinates):
        global board
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(coordinates):
            return False
        self.current_pos = coordinates
        board[y][x] = self
        board[cur_y][cur_x] = self.cells

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
        for i in range(cur_y+ny, y, ny):
            for j in range(cur_x+nx, x, nx):
                if not (board[i][j] == 0 or board[i][j] == -1):
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
                    if self.same_color((i, j)):
                        continue
                    moves.append((i, j))
        return moves

    def is_check(self):
        return self


class Knight:
    def __init__(self, color, current_pos=None):
        self.color = color
        self.score = 3
        self.image = 'Pieces\\knight_'+self.color+'.png'
        self.current_pos = current_pos

    def move(self, coordinates):
        global board
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(coordinates):
            return False
        self.current_pos = coordinates
        board[y][x] = self
        board[cur_y][cur_x] = -1 if board[cur_y-1][cur_x] == 0 else 0

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
                    if self.same_color((i, j)):
                        continue
                    moves.append((i, j))
        return moves

    def is_check(self):
        return self


board = [[0 for i in range(8)] for j in range(8)]
for i in range(8):
    for j in range(8):
        if (i+j) % 2 == 0:
            board[i][j] = -1

bishop1 = Bishop('black', -1)
rook1 = Rook('white')
knight1 = Knight('white')
board[1][2] = knight1
board[3][4] = bishop1
board[3][3] = rook1
print_board()
print()
knight1.current_pos = (1, 2)
bishop1.current_pos = (3, 4)
rook1.current_pos = (3, 3)

knight1.move((0, 0))
print_board()



class Queen:
    pass


class Pawn:
    pass


class King:
    def __init__(self, color, current_pos=None):
        self.color = color
        self.score = 10
        self.image = 'Pieces\\king_'+self.color+'.png'
        self.current_pos = current_pos

    def move(self, coordinates):
        pass

    def validate_move(self):
        pass

    def trajectory(self, coordinates):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if (abs(cur_y-y) == 1 or cur_y == y) and (abs(cur_x-x) == 1 or cur_x == x):
            return True
        return False

    def check(self):
        pass

k = King('white')
k.current_pos = (0, 4)

