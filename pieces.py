#! python3

import copy

def print_board(board):
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0 or board[i][j] == -1:
                print(board[i][j], end='|')
            else:
                print(board[i][j].score, end='|')
                # print(board[i][j].color, end = '|')
        print()


class Piece:
    def __init__(self, color, current_pos=None):
        self.color = color
        self.current_pos = current_pos

    def move(self, board, coordinates):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(board, coordinates):
            return False
        self.current_pos = coordinates
        board[y][x] = self
        board[cur_y][cur_x] = -1 if (cur_y+cur_x) % 2 == 0 else 0
        return True

    def validate_move(self, board, coordinates):
        c1 = self.is_check(board)
        c2 = self.will_check(board, coordinates)
        c3 = self.trajectory(board, coordinates)
        c4 = self.is_blocked(board, coordinates)
        c5 = self.same_color(board, coordinates)

        if not c2 and c1 and c3:
            return True
        if c1 or c2 or not c3 or c4 or c5:
            return False
        return True

    def available_moves(self, board):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.validate_move(board, (i, j)) and not (i, j) == self.current_pos:
                    moves.append((i, j))
        return moves

    def all_moves(self, board):
        moves = []
        for i in range(8):
            for j in range(8):
                c1 = self.trajectory(board, (i, j))
                c2 = self.is_blocked(board, (i, j))
                c3 = self.same_color(board, (i, j))
                if c1 and not c2 and not c3:
                    moves.append((i, j))
        return moves

    def trajectory(self, coordinates):
        pass

    def is_blocked(self, board, coordinates):
        pass

    def same_color(self, board, coordinates):
        y, x = coordinates
        if not (board[y][x] == -1 or board[y][x] == 0):
            return board[y][x].color == self.color
        return False

    def is_check(self, board):
        for i in range(8):
            for j in range(8):
                if type(board[i][j]) == King and board[i][j].color == self.color:
                    return board[i][j].check(board)

    def will_check(self, board, coordinates):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        temp = board[y][x]
        board[y][x] = self
        board[cur_y][cur_x] = -1 if (cur_y+cur_x) % 2 == 0 else 0
        self.current_pos = coordinates
        results = self.is_check(board)
        board[cur_y][cur_x] = self
        board[y][x] = temp
        self.current_pos = (cur_y, cur_x)
        return results


class Queen(Piece):
    def __init__(self, color, current_pos=None):
        super().__init__(color, current_pos)
        self.score = 9

    def trajectory(self, board, coordinates):
        y, x = coordinates
        cur_y, cur_x = self.current_pos
        # horizontal / vertical movement
        option1 = ((cur_y == y and not cur_x == x) or (cur_x == x and not cur_y == y))
        # diagonal movement
        option2 = (abs(cur_y - y) == abs(cur_x - x))
        if not (option1 or option2):
            return False
        return True

    def is_blocked(self, board, coordinates):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        # HORIZONTAL / VERTICAL IMPEDIMENT
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
        iter_y = [e for e in range(cur_y + ny, y + ny, ny)]
        iter_x = [z for z in range(cur_x + nx, x + nx, nx)]
        for i, j in zip(iter_y, iter_x):
            if not (board[i][j] == 0 or board[i][j] == -1) and not (coordinates == (i, j)):
                return True
        return False


class Rook(Piece):
    def __init__(self, color, current_pos=None, moved=False):
        super().__init__(color, current_pos)
        self.score = 5
        self.moved = moved

    def trajectory(self, board, coordinates):
        y, x = coordinates
        cur_y, cur_x = self.current_pos
        if (cur_y == y and cur_x != x) or (cur_x == x and cur_y != y):
            return True
        return False

    def is_blocked(self, board, coordinates):
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


class Bishop(Piece):
    def __init__(self, color, current_pos=None):
        super().__init__(color, current_pos)
        self.score = 3.5

    def trajectory(self, board, coordinates):
        y, x = coordinates
        cur_y, cur_x = self.current_pos
        if not (abs(cur_y - y) == abs(cur_x - x)):
            return False
        return True

    def is_blocked(self, board, coordinates):
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


class Knight(Piece):
    def __init__(self, color, current_pos=None):
        super().__init__(color, current_pos)
        self.score = 3

    def validate_move(self, board, coordinates):
        c1 = self.is_check(board)
        c2 = self.will_check(board, coordinates)
        c3 = self.trajectory(board, coordinates)
        c4 = self.same_color(board, coordinates)
        if not c2 and c1 and c3:
            return True
        if c1 or not c3 or c4:
            return False
        return True

    def trajectory(self, board, coordinates):
        y, x = coordinates
        cur_y, cur_x = self.current_pos
        option1 = (abs(cur_y - y) == 1 and abs(cur_x - x) == 2)
        option2 = (abs(cur_x - x) == 1 and abs(cur_y - y) == 2)
        if option1 or option2:
            return True
        return False


class Pawn(Piece):
    def __init__(self, color, current_pos=None, first_move=True, view=1):
        super().__init__(color, current_pos)
        self.score = 1
        self.first_move = first_move
        self.view = view

    def move(self, board, coordinates):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(board, coordinates):
            return False
        self.current_pos = coordinates
        board[y][x] = self
        board[cur_y][cur_x] = -1 if (cur_y + cur_x) % 2 == 0 else 0
        if self.first_move:
            self.first_move = False
        return True

    def validate_move(self, board, coordinates):
        c1 = self.is_check(board)
        c2 = self.will_check(board, coordinates)
        c = self.exc(board, coordinates)
        c3 = self.trajectory(board, coordinates)
        c4 = self.is_blocked(board, coordinates)
        c5 = self.same_color(board, coordinates)

        if not c2 and c1 and (c3 or c):
            return True
        if c1 or c2:
            return False
        if c:
            return True
        if not c3 or c4 or c5:
            return False
        return True

    def all_moves(self, board):
        moves = []
        for i in range(8):
            for j in range(8):
                c = self.exc(board, (i, j))
                c1 = self.trajectory(board, (i, j))
                c2 = self.is_blocked(board, (i, j))
                c3 = self.same_color(board, (i, j))
                if c:
                    moves.append((i, j))
                    continue
                if c1 and not c2 and not c3:
                    moves.append((i, j))
        return moves

    def trajectory(self, board, coordinates):
        y, x = coordinates
        cur_y, cur_x = self.current_pos

        case1 = (self.first_move and (y == (cur_y + 2 * self.view)) and cur_x == x)
        case2 = (y == (cur_y + self.view) and cur_x == x)
        if (case1 and not self.is_blocked(board, (y - self.view, x))) or case2:
            return True
        return False

    def exc(self, board, coordinates):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if self.view == 1:
            n = (y - cur_y) == 1 and abs(cur_x - x) == 1
        else:
            n = (y-cur_y) == -1 and abs(cur_x-x) == 1
        result1 = self.is_blocked(board, coordinates) and \
            n and not self.same_color(board, coordinates)
        return result1

    @staticmethod
    def is_blocked(board, coordinates):
        y, x = coordinates
        if not (board[y][x] == 0 or board[y][x] == -1):
            return True
        return False


class King(Piece):
    def __init__(self, color, current_pos=None, moved=False):
        super().__init__(color, current_pos)
        self.score = 10
        self.moved = moved

    def move(self, board, coordinates):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(board, coordinates):
            return False
        self.current_pos = coordinates
        board[y][x] = self
        board[cur_y][cur_x] = -1 if (cur_y+cur_x) % 2 == 0 else 0
        self.moved = True
        return True

    def validate_move(self, board, coordinates):
        c1 = self.will_check(board, coordinates)
        c2 = self.trajectory(board, coordinates)
        c3 = self.is_blocked(board, coordinates)
        c4 = self.same_color(board, coordinates)
        if c1 or not c2 or c3 or c4:
            return False
        return True

    def trajectory(self, board, coordinates):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        condition1 = (abs(cur_y - y) == 1 or cur_y == y)
        condition2 = (abs(cur_x - x) == 1 or cur_x == x)
        #condition3 = self.can_castle(board, coordinates)
        if condition1 and condition2:
            return True
        return False

    def is_blocked(self, board, coordinates):
        y, x = coordinates
        if not (board[y][x] == 0 or board[y][x] == -1) and board[y][x].color == self.color:
            return True
        return False

    def check(self, board):
        # Temporal conditional, can be deleted
        y, x = self.current_pos
        # Going through diagonals
        # Upper left diagonal
        n = y if y < x else x
        low_y, low_x = y-n, x-n
        iter_y = [e for e in range(low_y, 8)]
        iter_x = [z for z in range(low_x, 8)]
        diag_threats = [Bishop, Pawn, Queen]
        for i, j in zip(iter_y, iter_x):
            if type(board[i][j]) in diag_threats and not (board[i][j].color == self.color):
                target = board[i][j].all_moves(board)
                if self.current_pos in target:
                    return True
        # Lower left diagonal
        n = (7-y) if (7-y) < x else x
        high_y = y+n
        high_x = x-n
        iter_y = [e for e in range(high_y, 0, -1)]
        iter_x = [z for z in range(high_x, 8)]
        for i, j in zip(iter_y, iter_x):
            if type(board[i][j]) in diag_threats and not board[i][j].color == self.color:
                target = board[i][j].all_moves(board)
                if self.current_pos in target:
                    return True
        # Going through vertical/horizontal lines
        straight_threats = [Rook, Queen]
        for i in range(8):
            if type(board[y][i]) in straight_threats and not board[y][i].color == self.color:
                target = board[y][i].all_moves(board)
                if self.current_pos in target:
                    return True
            if type(board[i][x]) in straight_threats and not board[i][x].color == self.color:
                target = board[i][x].all_moves(board)
                if self.current_pos in target:
                    return True
        knight_moves = [
            (y-2, x+1), (y-2, x-1),
            (y+2, x+1), (y+2, x-1),
            (y+1, x-2), (y-1, x-2),
            (y+1, x+2), (y-1, x+2)]

        final_moves = []
        for m in knight_moves:
            c1 = m[0] < 0 or m[0] > 7
            c2 = m[1] < 0 or m[1] > 7
            if not c1 and not c2:
                final_moves.append(m)
        for y_pos, x_pos in final_moves:
            if type(board[y_pos][x_pos]) == Knight and not board[y_pos][x_pos].color == self.color:
                return True
        return False

    def get_team_pieces(self, board):
        team = []
        for i in range(8):
            for j in range(8):
                if not (type(board[i][j]) == int) and board[i][j].color == self.color:
                    team.append(board[i][j])
        return team


#table = [[0 for i in range(8)] for j in range(8)]
#for i in range(8):
#    for j in range(8):
#        if (i + j) % 2 == 0:
#            table[i][j] = -1