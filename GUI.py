import pygame
from pieces import *
from AI import *

BLACK = (0, 0, 0)


class Game:
    """
    Game class containing all methods necessary to use the GUI.

    Attributes
    ----------
    screen: pygame.Surface
        640x640px pygame.Surface, main game window

    board: list
        2-D list containing chess board.

    Methods
    -------

    __init__:
        Initializes Game object with a screen(640x640px) and
        a chess board containing all pieces.

    format_board:
        Creates the chess board (2-D list) initializing all Piece objects inside it.

    get_pos:
        Calculates board position given the mouse location

    print_stalemate:
        Prints "STALEMATE" onto the screen

    checkmate:
        Returns True if the current state of the board is checkmate, False otherwise.

    stalemate:
        Returns True if the current state of the board is a draw, False otherwise.

    pawns:
        Handles some Pawn attributes to allow the en passant rule to work.

    terminal_condition:
        Handles pawn, checkmate and stalemate methods.

    draw_cells:
        Splits the screen in an 8x8 grid alternating brown and white squares,
        it uses a special color for the last piece moved. Displays the pieces' images
        depending on their current position.

    draw_helper:
        Handles main menu features (background color, shapes, images and text).

    select_helper:
        Handles user choice whether to go against AI or another player.

    main_menu:
        Main menu loop found here.

    main_loop:
        Main game loop found here. Handles AI or player moves, as well as the drawing
        of the board.

    end_loop:
        End game loop found here. The screen is frozen in the last position, a message
        displaying the result of the steady appears in the middle of the window.
    """

    def __init__(self):
        """Initializes game object."""
        self.screen = pygame.display.set_mode((640, 640))
        self.board = self.format_board()
        pygame.display.set_caption('CHESS')

    @staticmethod
    def format_board():
        """Creates chess board (2-D list) initializing all Piece objects inside it."""
        board = [[0 if (z + e) % 2 == 0 else -1 for z in range(8)] for e in range(8)]
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

    @staticmethod
    def get_pos(coordinates: tuple):
        """Calculates board position given the mouse location."""
        y, x = coordinates[0] // 80, coordinates[1] // 80
        return y, x

    def print_stalemate(self):
        """Prints "STALEMATE" onto the screen."""
        font = pygame.font.SysFont('comicsans', 80)
        text = font.render('STALEMATE', 1, BLACK)
        self.screen.blit(text, (160, 260))
        pygame.display.flip()

    def checkmate(self, turn: bool):
        """
        Returns True if the current state of the board is checkmate, False otherwise.

        Parameters
        ----------
        turn: bool
            True if it's white turn, False otherwise.
        """
        color = 'white' if turn else 'black'
        for i in range(8):
            for j in range(8):
                if type(self.board[i][j]) == King and self.board[i][j].color == color:
                    king = self.board[i][j]
                    if king.check(self.board) and not king.available_moves(self.board):
                        team = king.get_team_pieces(self.board)
                        if not team:
                            font = pygame.font.SysFont('comicsans', 80, True)
                            if king.color == 'white':
                                text = font.render('BLACK WON', 1, BLACK)
                            else:
                                text = font.render('WHITE WON', 1, BLACK)
                            self.screen.blit(text, (200, 200))
                            pygame.display.flip()
                            return True
                        counts = 0
                        for piece in team:
                            if not piece.available_moves(self.board):
                                counts += 1
                                font = pygame.font.SysFont('comicsans', 80)
                        if king.color == 'white':
                            text = font.render('BLACK WON', 1, BLACK)
                        else:
                            text = font.render('WHITE WON', 1, BLACK)
                        if counts == len(team):
                            self.screen.blit(text, (160, 260))
                            pygame.display.flip()
                            return True
                    return False

    def stalemate(self, turn: bool):
        """
        Returns True if the current state of the board is a draw, False otherwise.

        Parameters
        ----------
        turn: bool
            True if it's white's turn, False otherwise.
        """
        color = 'white' if turn else 'black'
        counts = 0
        for i in range(8):
            for j in range(8):
                if not type(self.board[i][j]) == int:
                    counts += 1
        if counts == 2:  # it's king against king
            self.print_stalemate()
            return True

        for i in range(8):
            for j in range(8):
                if type(self.board[i][j]) == King and self.board[i][j].color == color:
                    king = self.board[i][j]
                    if king.check(self.board) or king.available_moves(self.board):
                        return False
                    team = king.get_team_pieces(self.board)
                    if not team:  # drowned.
                        self.print_stalemate()
                        return True
                    for piece in team:
                        if piece.available_moves(self.board):
                            return False
                    self.print_stalemate()
                    return True

    def pawns(self, white: bool):
        """
        Handles some Pawn attributes to allow the en passant rule to work.

        Parameters
        ----------
        white: bool
            True if it's white's turn, else False.
        """
        for i in range(8):
            if type(self.board[3][i]) == Pawn and self.board[3][i].color == 'black' and \
                    not white:
                self.board[3][i].just_moved = False
            if type(self.board[4][i]) == Pawn and self.board[4][i].color == 'white' and white:
                self.board[4][i].just_moved = False

    def terminal_condition(self, turn: bool):
        """
        Handles pawn, checkmate and stalemate methods.

        Parameters
        ----------
        turn: bool
            True if it's white's turn, False otherwise.
        """
        self.pawns(turn)
        return self.checkmate(turn) or self.stalemate(turn)

    def draw_cells(self, last_pos: tuple, new_pos: tuple):
        """
        Splits the screen in an 8x8 grid alternating brown and white squares,
        uses a special color for the last piece moved. Displays the pieces' images
        depending on their current position.

        Parameters
        ---------
        last_pos: tuple
            Position from which the last piece was moved.
        new_pos: tuple
            Position to which the last piece was moved.
        """
        n = 80
        y, x = new_pos
        from_y, from_x = last_pos
        for i in range(8):
            for j in range(8):
                cell_x = n * i
                cell_y = n * j
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.screen, (255, 255, 255), (cell_y, cell_x, 80, 80))
                else:
                    pygame.draw.rect(self.screen, (155, 118, 83), (cell_y, cell_x, 80, 80))
                if not y == 10:
                    if i == y and j == x:
                        pygame.draw.rect(self.screen, (201, 174, 51), (x * n, y * n, 80, 80))
                    if i == from_y and j == from_x:
                        pygame.draw.rect(self.screen, (201, 174, 51), (from_x * n, from_y * n, 80, 80))
                if not type(self.board[i][j]) == int:
                    temp = self.board[i][j]
                    piece = pygame.image.load(temp.image)
                    self.screen.blit(piece, (cell_y + 10, cell_x + 10))
                    pygame.display.flip()
        pygame.display.flip()

    def draw_helper(self):
        """Handles main menu features (background color, shapes, images and text)."""
        # Coordinates for all drawings, text and images have been done by eyesight, there are no calculations behind it.
        self.screen.fill((200, 200, 0))
        # Defining text fonts:
        font = pygame.font.SysFont('comicsans', 60)
        font2 = pygame.font.SysFont('caveat', 60, True)
        # Loading main menu images.
        board_img = pygame.image.load('.\\imgs\\board-games.png')
        board_img2 = pygame.image.load('.\\imgs\\board-games2.png')
        cobra = pygame.image.load('.\\imgs\\cobra.png')
        # Rendering text.
        game_name = font2.render('Python Chess with pygame', 1, BLACK)
        text = font.render('SELECT GAME MODE:', 1, BLACK)
        text2 = font.render('Player vs Player', 1, (110, 44, 0))
        text3 = font.render('Player vs AI', 1, (110, 44, 0))
        # Drawing some outlines to emulate "buttons".
        pygame.draw.rect(self.screen, BLACK, (45, 280, 555, 280), width=3)
        pygame.draw.rect(self.screen, BLACK, (125, 390, 370, 70), width=3)
        pygame.draw.rect(self.screen, BLACK, (175, 480, 285, 70), width=3)
        # Printing everything on screen.
        self.screen.blit(text, (95, 300))
        self.screen.blit(text2, (145, 400))
        self.screen.blit(text3, (195, 500))
        self.screen.blit(game_name, (45, 20))
        self.screen.blit(board_img, (65, 100))
        self.screen.blit(board_img2, (427, 100))
        self.screen.blit(cobra, (255, 100))
        pygame.display.flip()

    @staticmethod
    def select_helper(position: tuple):
        """
        Handles user choice whether to go against AI or another player.

        Parameters
        ----------
        position: tuple
            X, y mouse position when clicked.
        """
        against_player = [(j, i) for i in range(390, 390 + 71) for j in range(125, 125 + 371)]
        against_ai = [(j, i) for i in range(480, 480 + 71) for j in range(175, 175 + 286)]
        if position in against_player:
            return 1
        elif position in against_ai:
            return -1
        else:
            return 0

    def main_menu(self):
        """Main menu loop found here."""
        choosing = True
        self.draw_helper()  # no need to draw it at every iteration.
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    choosing = False
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    selection = self.select_helper(pos)
                    if not selection == 0:
                        choosing = False
                        return selection

    def main_loop(self):
        """
        Main game loop found here. Handles AI or player moves, as well as the drawing
        of the board.
        """
        running = True
        ai_active = self.main_menu()
        selected = None
        white_turn = True
        src = (10, 10)
        dsn = (10, 10)
        while running:
            self.draw_cells(src, dsn)
            if self.terminal_condition(white_turn):
                running = False
                continue
            if not white_turn and ai_active == -1:
                result = alpha_beta(self.board, depth=2, turn=False, alpha=(None, None, float('-inf')),
                                    beta=(None, None, float('inf')))
                src = result[0].current_pos
                dsn = result[1]
                y, x = result[1]
                result[0].move(self.board, (y, x))
                white_turn = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if selected is None:
                        cur_x, cur_y = event.pos
                        y, x = self.get_pos((cur_y, cur_x))
                        if type(self.board[y][x]) == int:
                            continue
                        if (self.board[y][x].color == 'black' and white_turn) \
                                or (self.board[y][x].color == 'white' and not white_turn):
                            break
                        selected = self.board[y][x]
                    else:
                        cur_x, cur_y = event.pos
                        y, x = self.get_pos((cur_y, cur_x))
                        src = selected.current_pos
                        if selected.move(self.board, (y, x)):
                            dsn = (y, x)
                            if white_turn:
                                white_turn = False
                            else:
                                white_turn = True
                        selected = None
                        break

    @staticmethod
    def end_loop():
        """
        End game loop found here. The screen is frozen in the last position, a message
        displaying the result of the steady appears in the middle of the window.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
