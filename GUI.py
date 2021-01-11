#! python3

import pygame
from pieces import *
from AI import *

BLACK = (0, 0, 0)
class Game:

    def __init__(self, screen):
        self.screen = screen
        self.board = self.format_board()

    @staticmethod
    def format_board():
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

    def checkmate(self, turn):
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
                                font = pygame.font.SysFont('comicsans', 80, True)
                        if king.color == 'white':
                            text = font.render('BLACK WON', 1, BLACK)
                        else:
                            text = font.render('WHITE WON', 1, BLACK)
                        if counts == len(team):
                            self.screen.blit(text, (200, 200))
                            pygame.display.flip()
                            return True
                    return False

    def stalemate(self, turn):
        color = 'white' if turn else 'black'
        counts = 0
        for i in range(8):
            for j in range(8):
                if not type(self.board[i][j]) == int:
                    counts += 1
        if counts == 2:
            return True

        for i in range(8):
            for j in range(8):
                if type(self.board[i][j]) == King and self.board[i][j].color == color:
                    king = self.board[i][j]
                    if king.check(self.board) or king.available_moves(self.board):
                        return False
                    team = king.get_team_pieces(self.board)
                    if not team:
                        return True
                    for piece in team:
                        if piece.available_moves(self.board):
                            return False
                    return True

    def pawns(self, white):
        for i in range(8):
            if type(self.board[3][i]) == Pawn and self.board[3][i].color == 'black' and \
              not white:
                self.board[3][i].just_moved = False
            if type(self.board[4][i]) == Pawn and self.board[4][i].color == 'white' and white:
                self.board[4][i].just_moved = False

    def terminal_condition(self, turn):
        """Returns True if it's a stalemate or checkmate, i.e. terminal state of the game."""
        self.pawns(turn)
        return self.checkmate(turn) or self.stalemate(turn)

    def draw_cells(self, last_pos, new_pos):
        n = 80
        y, x = new_pos
        from_y, from_x = last_pos
        for i in range(8):
            for j in range(8):
                cell_x = n * i
                cell_y = n * j
                if (i+j) % 2 == 0:
                    pygame.draw.rect(self.screen, (255, 255, 255), (cell_y, cell_x, 80, 80))
                else:
                    pygame.draw.rect(self.screen, (155, 118, 83), (cell_y, cell_x, 80, 80))
                if not y == 10:
                    if i == y and j == x:
                        pygame.draw.rect(self.screen, (201, 174, 51), (x*n, y*n, 80, 80))
                    if i == from_y and j == from_x:
                        pygame.draw.rect(self.screen, (201, 174, 51), (from_x*n, from_y*n, 80, 80))
                if not type(self.board[i][j]) == int:
                    temp = self.board[i][j]
                    piece = pygame.image.load(temp.image)
                    self.screen.blit(piece, (cell_y+10, cell_x+10))
                    pygame.display.flip()
        pygame.display.flip()

    @staticmethod
    def get_pos(coordinates):
        y, x = coordinates[0] // 80, coordinates[1] // 80
        return y, x

    def divide_cells(self):
        for i in range(8):
            pygame.draw.line(self.screen, BLACK, (0, i*80), (640, i*80), width=1)
            pygame.draw.line(self.screen, BLACK, (i * 80, 0), (i * 80, 640), width=1)
            pygame.display.flip()

    def draw_helper(self):
        # Coordinates for all drawings, text and images have been done by eyesight, there are no calculations behind it.
        self.screen.fill((200, 200, 0))
        # Defining text fonts:
        font = pygame.font.SysFont('comicsans', 60)
        font2 = pygame.font.SysFont('caveat', 60, True)
        # Loading main menu images.
        board_img = pygame.image.load('.\\board-games.png')
        board_img2 = pygame.image.load('.\\board-games2.png')
        cobra = pygame.image.load('.\\cobra.png')
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
    def select_helper(position):
        against_player = [(j, i) for i in range(390, 390+71) for j in range(125, 125+371)]
        against_ai = [(j, i) for i in range(480, 480+71) for j in range(175, 175+286)]
        if position in against_player:
            return 1
        elif position in against_ai:
            return -1
        else:
            return 0

    def main_menu(self):
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
                result = alpha_beta(test.board, depth=2, turn=False, alpha=(None, None, float('-inf')),
                                    beta=(None, None, float('inf')))
                src = result[0].current_pos
                dsn = result[1]
                y, x = result[1]
                result[0].move(test.board, (y, x))
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
                        selected = test.board[y][x]
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
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
