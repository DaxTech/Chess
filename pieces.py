#! python3

PATH = '.\\chess_pieces\\'


class Piece:
    """
    Piece class containing most methods and attributes
    common to all all pieces.

    Methods
    -------

    __init__:
        Initializes object with color and a current position (default None).

    move:
        Moves piece from point y1, x1 to y2, x2.

    validate_move:
        Validates movement from current position to given coordinates.

    available_moves:
        Returns list of valid movements for a given piece.

    all_moves:
        Returns list of all almost valid movements for a given piece.

    trajectory:
        Validates the trajectory of a move for a given piece.

    is_blocked:
        Returns boolean depending if the given coordinates are blocked.

    same_color:
        Returns boolean regarding the color of the piece at a given location.

    is_check:
        Returns boolean depending if the team king is in check or not.

    will_check:
        Returns boolean depending if the given move will jeopardize
        the team king.
    """

    def __init__(self, color: str, current_pos=None):
        """
        Initializes Piece object.

        Parameters
        ----------
        color: str
            color of the piece
        current_pos: tuple
            current position of the piece (default None).
        """
        self.color = color
        self.current_pos = current_pos

    def move(self, board: list, coordinates: tuple, forced=False):
        """

        Moves piece from y1,x1 to y2,x2 if movement is valid.

        Parameters
        ----------
        board: list
            chess board.
        coordinates: tuple
            y, x coordinates, destination cell.
        forced: bool
            movement is forced by another piece like in castling (default False).
        """
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not forced and not self.validate_move(board, coordinates):
            return False
        self.current_pos = coordinates
        board[y][x] = self
        board[cur_y][cur_x] = 0 if (cur_y + cur_x) % 2 == 0 else -1
        return True

    def validate_move(self, board: list, coordinates: tuple):
        """
        Returns True if movement is valid, False otherwise.

        Parameters
        ----------
        board: list
            chess board.
        coordinates: tuple
            y, x coordinates, destination cell.
        """
        # Conditions to make move in order of importance.
        c1 = self.is_check(board)
        c2 = self.will_check(board, coordinates)
        c3 = self.trajectory(board, coordinates)
        c4 = self.is_blocked(board, coordinates)
        c5 = self.same_color(board, coordinates)

        # The movement won't let the king in check, and the king
        #  is currently in check, and all the other conditions
        #  are fulfilled.
        if not c2 and c1 and c3 and not (c5 or c4):
            return True
        if c1 or c2 or not c3 or c4 or c5:
            return False
        return True

    def available_moves(self, board: list):
        """
        Returns list of available valid movements for a given piece.

        Parameters
        ----------
        board: list
            chess board.
        """
        moves = []
        for i in range(8):
            for j in range(8):
                if not self.trajectory(board, (i, j)):
                    continue
                if self.validate_move(board, (i, j)) and not (i, j) == self.current_pos:
                    moves.append((i, j))
        return moves

    def all_moves(self, board: list):
        """
        Returns all moves available, for check validation purposes.

        Parameters
        ----------
        board: list
            chess board.
        """
        moves = []
        for i in range(8):
            for j in range(8):
                c1 = self.trajectory(board, (i, j))
                c2 = self.is_blocked(board, (i, j))
                c3 = self.same_color(board, (i, j))
                if c1 and not c2 and not c3:
                    moves.append((i, j))
        return moves

    def trajectory(self, board: list, coordinates: tuple):
        """
        Returns True if the input trajectory for given piece is valid,
        False otherwise.

        Parameters
        ----------
        board: list
            chess board.
        coordinates: tuple
            y, x coordinates, destination cell.
        """
        pass

    @staticmethod
    def is_blocked(board: list, coordinates: tuple):
        """
        Returns True if the path to given location is blocked,
        False otherwise.

        Parameters
        ----------
        board: list
            chess board.
        coordinates: tuple
            y, x coordinates, destination cell.
        """
        pass

    def same_color(self, board: list, coordinates: tuple):
        """
        Returns True if the cell at given location is of the same color,
        False otherwise.

        Parameters
        ----------
        board: list
            chess board.
        coordinates: tuple
            y, x coordinates, destination cell.
        """
        y, x = coordinates
        if not type(board[y][x]) == int:  # means the cell is empty.
            return board[y][x].color == self.color
        return False

    def is_check(self, board: list):
        """
        Returns True if the team king is in check, False otherwise

        Parameters
        ----------
        board: list
            chess board.
        """
        for i in range(8):
            for j in range(8):
                if type(board[i][j]) == King and board[i][j].color == self.color:
                    return board[i][j].check(board)

    def will_check(self, board: list, coordinates: tuple):
        """
        Returns True if given move will jeopardize the team king,
        False otherwise.

        Parameters
        ----------
        board: list
            chess board.
        coordinates: tuple
            y, x coordinates, destination cell.
        """

        cur_y, cur_x = self.current_pos
        y, x = coordinates
        # Temporal movement.
        temp = board[y][x]
        board[y][x] = self
        board[cur_y][cur_x] = 0 if (cur_y + cur_x) % 2 == 0 else -1
        self.current_pos = coordinates
        results = self.is_check(board)
        # Return everything back to normal.
        board[cur_y][cur_x] = self
        board[y][x] = temp
        self.current_pos = (cur_y, cur_x)
        return results


class Queen(Piece):
    """
    Queen class, Piece subclass containing customized methods according
    to the queen piece.
    """

    def __init__(self, color: str, current_pos=None):
        super().__init__(color, current_pos)
        self.letter = 'Q'
        self.score = 900  # num value of the queen.
        self.image = PATH+color[0]+'Queen.png'

    def trajectory(self, board: list, coordinates: tuple):
        y, x = coordinates
        cur_y, cur_x = self.current_pos
        # Horizontal / Vertical movement.
        option1 = ((cur_y == y and not cur_x == x) or
                   (cur_x == x and not cur_y == y))
        # Diagonal movement.
        option2 = (abs(cur_y - y) == abs(cur_x - x))
        if not (option1 or option2):
            return False
        return True

    def is_blocked(self, board: list, coordinates: tuple):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        # HORIZONTAL / VERTICAL IMPEDIMENT.
        ny = 1 if y > cur_y else -1
        nx = 1 if x > cur_x else -1
        if cur_y == y:
            for j in range(cur_x + nx, x, nx):
                if not type(board[y][j]) == int:
                    return True
        if cur_x == x:
            for i in range(cur_y + ny, y, ny):
                if not type(board[i][x]) == int:
                    return True
        # DIAGONAL IMPEDIMENT.
        iter_y = [e for e in range(cur_y + ny, y + ny, ny)]
        iter_x = [z for z in range(cur_x + nx, x + nx, nx)]
        # Iterate through all diagonal combinations.
        for i, j in zip(iter_y, iter_x):
            if not (board[i][j] == 0 or board[i][j] == -1) and \
               not (coordinates == (i, j)):
                return True
        return False


class Rook(Piece):
    """
    Rook class, Piece subclass containing customized methods according
    to the rook piece.
    """
    def __init__(self, color: str, current_pos=None, moved=False):
        super().__init__(color, current_pos)
        self.letter = 'R'
        self.score = 500  # num value of the rook
        self.moved = moved
        self.image = PATH + color[0] + 'Rook.png'

    def trajectory(self, board: list, coordinates: tuple):
        y, x = coordinates
        cur_y, cur_x = self.current_pos
        if (cur_y == y and not cur_x == x) or (cur_x == x and not cur_y == y):
            return True
        return False

    def is_blocked(self, board: list, coordinates: tuple):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        ny = 1 if y > cur_y else -1
        nx = 1 if x > cur_x else -1
        if cur_y == y:
            for j in range(cur_x + nx, x, nx):
                if not type(board[y][j]) == int:
                    return True
        if cur_x == x:
            for i in range(cur_y + ny, y, ny):
                if not type(board[i][x]) == int:
                    return True
        return False


class Bishop(Piece):
    """
    Bishop class, Piece subclass containing customized methods according
    to bishop piece.
    """
    def __init__(self, color: str, current_pos=None):
        super().__init__(color, current_pos)
        self.letter = 'B'
        self.score = 330  # num value of the bishop.
        self.image = PATH + color[0] + 'Bishop.png'

    def trajectory(self, board: list, coordinates: tuple):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        # Diagonal movement has equal change in y than in x.
        if not (abs(cur_y - y) == abs(cur_x - x)):
            return False
        return True

    def is_blocked(self, board: list, coordinates: tuple):
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
    """
    Knight class, Piece subclass containing customized methods according
    to knight piece
    """
    def __init__(self, color: str, current_pos=None):
        super().__init__(color, current_pos)
        self.letter = 'N'
        self.score = 320  # num value of the knight
        self.image = PATH + color[0] + 'Knight.png'

    def validate_move(self, board: list, coordinates: tuple):
        # Does not contain the is_blocked() condition, as knights
        #  jump over pieces.
        c1 = self.is_check(board)
        c2 = self.will_check(board, coordinates)
        c3 = self.trajectory(board, coordinates)
        c4 = self.same_color(board, coordinates)
        if not c2 and c1 and c3 and not c4:
            return True
        if c1 or c2 or not c3 or c4:
            return False
        return True

    def trajectory(self, board: list, coordinates: tuple):
        y, x = coordinates
        cur_y, cur_x = self.current_pos
        # The movement of the knight is always forming an L
        option1 = (abs(cur_y - y) == 1 and abs(cur_x - x) == 2)
        option2 = (abs(cur_x - x) == 1 and abs(cur_y - y) == 2)
        if option1 or option2:
            return True
        return False


class Pawn(Piece):
    """
    Pawn class, Piece subclass containing customized and additional
    methods according to the pawn piece.
    """
    def __init__(self, color: str, current_pos=None, first_move=True,
                 view=1, just_moved=False):
        super().__init__(color, current_pos)
        self.letter = 'P'
        self.score = 100  # num value of the pawn
        self.first_move = first_move
        self.view = view
        self.just_moved = just_moved
        self.image = PATH + color[0] + 'Pawn.png'

    def move(self, board: list, coordinates: tuple, forced=False):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(board, coordinates):
            return False
        # Handling take of en_passant exception.
        if self.en_passant(board, coordinates):
            n = y+1 if self.view == -1 else y-1  # one before or one after
            board[n][x] = 0 if (n + x) % 2 == 0 else -1
        self.current_pos = coordinates
        board[y][x] = self
        board[cur_y][cur_x] = 0 if (cur_y + cur_x) % 2 == 0 else -1

        if self.first_move:
            self.first_move = False  # cannot move 2 cells ahead anymore
            self.just_moved = True  # important for en passant exception.
            if y == 0 or y == 7:
                board[y][x] = Queen(self.color, current_pos=coordinates)
            return True
        if y == 0 or y == 7:
            board[y][x] = Queen(self.color, current_pos=coordinates)
        self.just_moved = False
        return True

    def available_moves(self, board: list):
        """
        Returns list of available valid movements for a given piece.

        Parameters
        ----------
        board: list
            chess board.
        """
        moves = []
        for i in range(8):
            for j in range(8):
                if not (self.trajectory(board, (i, j)) or self.en_passant(board, (i, j)) \
                   or self.exc(board, (i, j))):
                    continue
                if self.validate_move(board, (i, j)) and not (i, j) == self.current_pos:
                    moves.append((i, j))
        return moves

    def validate_move(self, board: list, coordinates: tuple):
        a = self.exc(board, coordinates)
        c1 = self.is_check(board)
        c2 = self.will_check(board, coordinates)
        c3 = self.trajectory(board, coordinates)
        c4 = self.is_blocked(board, coordinates)
        c5 = self.same_color(board, coordinates)
        # En passant exception movement
        if self.en_passant(board, coordinates) and not (c2 or c1):
            return True
        # Movement won't check, but king is in check right now.
        if not c2 and c1 and ((c3 and not c4) or a):
            return True
        if c1 or c2:  # movement will check or king is in check now.
            return False
        if a:  # diagonal movement to take another piece.
            return True
        if not c3 or c4 or c5:  # inadequate trajectory or blocked or same color.
            return False
        return True

    def all_moves(self, board: list):
        moves = []
        for i in range(8):
            for j in range(8):
                loc = (i, j)
                if self.exc(board, (i, j)) or self.en_passant(board, (i, j)):
                    moves.append((i, j))
                    continue
                if self.trajectory(board, loc) and not self.is_blocked(board, loc) \
                   and not self.same_color(board, loc):
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

    def exc(self, board: list, coordinates: tuple):
        """
        Returns True if the given coordinates match with the action of
        a pawn taking another piece, False otherwise.

        Parameters
        ----------
         board: list
            chess board.
        coordinates: tuple
            y, x coordinates, destination cell.
        """
        # Taking another piece exception.
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if self.view == 1:
            n = (y - cur_y) == 1 and abs(cur_x - x) == 1
        else:
            n = (y - cur_y) == -1 and abs(cur_x - x) == 1
        result = self.is_blocked(board, coordinates) and \
            n and not self.same_color(board, coordinates)
        return result

    def en_passant(self, board: list, coordinates: tuple):
        """
        Returns True if en passant action is possible, False otherwise.

        Parameters
        ----------
         board: list
            chess board.
        coordinates: tuple
            y, x coordinates, destination cell.
        """
        # En passant exception
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        n = 4 if self.view == 1 else 3
        if not cur_y == n:
            return False
        if not y == (n + self.view) or not abs(cur_x - x) == 1:
            return False
        if not type(board[n][x]) == Pawn:
            return False
        if not board[n][x].just_moved:
            return False
        return True

    @staticmethod
    def is_blocked(board: list, coordinates: tuple):
        y, x = coordinates
        if not type(board[y][x]) == int:
            return True
        return False


class King(Piece):
    """
    King class, Piece subclass containing customized and additional
    methods according to the king piece.
    """
    def __init__(self, color: str, current_pos=None, moved=False):
        super().__init__(color, current_pos)
        self.letter = 'K'
        self.score = 20000  # num value of the king
        self.moved = moved
        self.image = PATH + color[0] + 'King.png'

    def move(self, board: list, coordinates: tuple, forced=False):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        if not self.validate_move(board, coordinates):
            return False

        if self.can_castle(board, coordinates):
            # Force rook movement
            if x < cur_x:
                board[y][0].move(board, (y, x + 1), forced=True)
            else:
                board[y][7].move(board, (y, x - 1), forced=True)
        self.current_pos = coordinates
        board[y][x] = self
        board[cur_y][cur_x] = 0 if (cur_y + cur_x) % 2 == 0 else -1
        self.moved = True
        return True

    def validate_move(self, board: list, coordinates: tuple):
        c1 = self.will_check(board, coordinates)
        c2 = self.trajectory(board, coordinates)
        c3 = self.is_blocked(board, coordinates)
        c4 = self.same_color(board, coordinates)
        c5 = self.check(board)
        if self.can_castle(board, coordinates) and not c1 and not c5:
            return True
        if c1 or not c2 or c3 or c4:
            return False
        return True

    def trajectory(self, board: list, coordinates: tuple):
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        # Movement in any direction, but 1 spot
        condition1 = (abs(cur_y - y) == 1 or cur_y == y)
        condition2 = (abs(cur_x - x) == 1 or cur_x == x)
        if condition1 and condition2:
            return True
        return False

    def is_blocked(self, board: list, coordinates: tuple):
        y, x = coordinates
        if not type(board[y][x]) == int and board[y][x].color == self.color:
            return True
        return False

    def can_castle(self, board: list, coordinates: tuple):
        """
        Returns True if castling is possible, False otherwise.

        Parameters
        ----------
         board: list
            chess board.
        coordinates: tuple
            y, x coordinates, destination cell.
        """
        cur_y, cur_x = self.current_pos
        y, x = coordinates
        n = 0 if x < cur_x else 7
        m = -1 if x < cur_x else 1
        if self.moved:
            return False
        if not cur_y == y:  # castling happens in same row
            return False
        if not abs(cur_x - x) == 2:  # king always moves 2 cells away
            return False
        if not type(board[y][n]) == Rook or board[y][n].moved:
            return False
        # Checking for pieces blocking the way or checks.
        if x == 6:
            for i in range(1, 3):
                e = cur_x + i * m
                if not type(board[y][e]) == int or self.will_check(board, (y, e)):
                    return False
        else:
            for i in range(1, 4):
                e = cur_x + i * m
                if i == 3:
                    if not type(board[y][e]) == int:
                        return False
                    continue
                if not type(board[y][e]) == int or self.will_check(board, (y, e)):
                    return False
        return True

    def knight_check(self, board: list):
        """
        Returns True if King is in check originated from a Knight, False otherwise.

        Parameters
        ----------
        board: list
            chess board.
        """
        y, x = self.current_pos
        # All possible knight moves EVER
        knight_moves = [
                    (y - 2, x + 1), (y - 2, x - 1),
                    (y + 2, x + 1), (y + 2, x - 1),
                    (y + 1, x - 2), (y - 1, x - 2),
                    (y + 1, x + 2), (y - 1, x + 2)]
        # List containing valid moves depending on cur pos.
        final_moves = []
        for m in knight_moves:
            c1 = m[0] < 0 or m[0] > 7
            c2 = m[1] < 0 or m[1] > 7
            if not (c1 or c2): # both need to conditions evaluate to False.
                final_moves.append(m)
        for y_pos, x_pos in final_moves:
            if type(board[y_pos][x_pos]) == Knight and \
               not board[y_pos][x_pos].color == self.color:
                return True
        return False

    def vertical_horizontal_check(self, board: list):
        """
        Returns True if King is in check vertically or horizontally, False otherwise.

        Parameters
        ----------
        board: list
            chess board.
        """
        y, x = self.current_pos
        # Going through vertical/horizontal lines.
        straight_threats = [Rook, Queen, King]
        for i in range(8):
            # Horizontal check.
            if type(board[y][i]) in straight_threats and \
               not board[y][i].color == self.color:
                target = board[y][i].all_moves(board)
                if self.current_pos in target:
                    return True
            # Vertical check.
            if type(board[i][x]) in straight_threats and \
               not board[i][x].color == self.color:
                target = board[i][x].all_moves(board)
                if self.current_pos in target:
                    return True
        return False

    def diagonal_check(self, board: list):
        """
        Returns True if King is in check diagonally, False otherwise.

        Parameters
        ----------
        board: list
            chess board.
        """
        y, x = self.current_pos
        # Going through diagonals.
        # Upper left diagonal.
        n = y if y < x else x
        low_y, low_x = y - n, x - n
        n2 = low_y if low_y < low_x else low_x
        iter_y = [e for e in range(low_y, 8-n2)]
        iter_x = [z for z in range(low_x, 8-n2)]
        diag_threats = [Bishop, Pawn, Queen, King]
        for i, j in zip(iter_y, iter_x):
            if type(board[i][j]) in diag_threats and \
               not board[i][j].color == self.color:
                target = board[i][j].all_moves(board)
                if self.current_pos in target:
                    return True
        # Lower left diagonal.
        n = (7 - y) if (7-y) < x else x
        high_y = y + n
        low_x = x - n
        iter_y = [e for e in range(high_y, low_x-1, -1)]
        iter_x = [z for z in range(low_x, high_y+1)]
        for i, j in zip(iter_y, iter_x):
            if type(board[i][j]) in diag_threats and \
               not board[i][j].color == self.color:
                target = board[i][j].all_moves(board)
                if self.current_pos in target:
                    return True
        return False

    def check(self, board: list):
        """
        Returns True if King is in check, False otherwise.

        Parameters
        ----------
        board: list
            chess board.
        """
        danger = [self.diagonal_check(board), self.vertical_horizontal_check(board), self.knight_check(board)]
        # (b means bool, as every element of danger is a boolean value)
        for b in danger:
            if b:
                return True
        return False

    def get_team_pieces(self, board: list):
        """
        Returns list of all team pieces.

        Parameters
        ----------
        board: list
            chess board.
        """
        team = []
        for i in range(8):
            for j in range(8):
                if not (type(board[i][j]) == int) and board[i][j].color == self.color:
                    team.append(board[i][j])
        return team
