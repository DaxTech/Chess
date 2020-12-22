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
                    if self.same_color((i, j)):
                        continue
                    moves.append((i, j))
        return moves

    def is_check(self):
        return self


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
                    if self.same_color((i, j)):
                        continue
                    moves.append((i, j))
        return moves

    def is_check(self):
        return self


class Pawn:
    def __init__(self, color, current_pos=None, first_move=True, view=1):
        self.color = color
        self.score = 1
        self.image = 'Pieces\\pawn_' + self.color + '.png'
        self.current_pos = current_pos
        self.first_move = first_move
        self.view = 1

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
        cur_y, cur_x = self.current_pos
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
                    if self.same_color((i, j)):
                        continue
                    moves.append((i, j))
        return moves

    def is_check(self):
        return self


board = [[0 for i in range(8)] for j in range(8)]
for i in range(8):
    for j in range(8):
        if (i + j) % 2 == 0:
            board[i][j] = -1


rook1 = Rook('white')
knight1 = Knight('white')
bishop1 = Bishop('white',-1)
queen1 = Queen('white')
pawn1 = Pawn('white')
pawn2 = Pawn('white')
pawn3 = Pawn('white')
pawn4 = Pawn('white')

board[0][0], board[0][1], board[0][2], board[0][3] = rook1, knight1, bishop1, queen1
board[1][0], board[1][1], board[1][2], board[1][3] = pawn1, pawn2, pawn3, pawn4

rook1.current_pos = (0, 0)
knight1.current_pos = (0, 1)
bishop1.current_pos = (0, 2)
queen1.current_pos = (0, 3)
pawn1.current_pos, pawn2.current_pos, pawn3.current_pos, pawn4.current_pos = (1, 0), (1, 1), (1, 2), (1, 3)
print_board()
print()

print(len(queen1.available_moves()))
print(len(knight1.available_moves()))
print(len(bishop1.available_moves()))
print(len(rook1.available_moves()))
print(pawn4.available_moves())
pawn4.move((3, 3))
print()
print(print_board())
print(len(queen1.available_moves()))
print(len(bishop1.available_moves()))


class King:
    def __init__(self, color, current_pos=None):
        self.color = color
        self.score = 10
        self.image = 'Pieces\\king_' + self.color + '.png'
        self.current_pos = current_pos

    def move(self, coordinates):
        pass

    def validate_move(self):
        pass

    def trajectory(self, coordinates):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if (abs(cur_y - y) == 1 or cur_y == y) and (abs(cur_x - x) == 1 or cur_x == x):
            return True
        return False

    def check(self):
        pass


k = King('white')
k.current_pos = (0, 4)