#! python3

import pygame
from pieces import *


PATH = '.\\chess_pieces\\'

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.board = self.format_board()

    @staticmethod
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

    def checkmate(self):
        for i in range(8):
            for j in range(8):
                if type(self.board[i][j]) == King:
                    king = self.board[i][j]
                    if king.check(self.board) and not king.available_moves(self.board):
                        team = king.get_team_pieces(self.board)
                        if not team:
                            font = pygame.font.SysFont('comicsans', 80, True)
                            if king.color == 'white':
                                text = font.render('BLACK WON', 1, (0, 0, 0))
                            else:
                                text = font.render('WHITE WON', 1, (0, 0, 255))
                            self.screen.blit(text, (200, 200))
                            pygame.display.flip()
                            return True
                        counts = 0
                        for piece in team:
                            if not piece.available_moves(self.board):
                                counts += 1
                                font = pygame.font.SysFont('comicsans', 80, True)
                        if king.color == 'white':
                            text = font.render('BLACK WON', 1, (0, 0, 0))
                        else:
                            text = font.render('WHITE WON', 1, (0, 0, 255))
                        if counts == len(team):
                            self.screen.blit(text, (200, 200))
                            pygame.display.flip()
                            return True
        return False

    def stalemate(self, turn):
        turn = 'white' if turn else 'black'
        counts = 0
        for i in range(8):
            for j in range(8):
                if not type(self.board[i][j]) == int:
                    counts += 1
        if counts == 2:
            return True
        
        for i in range(8):
            for j in range(8):
                if type(self.board[i][j]) == King and self.board[i][j].color == turn:
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

    def divide(self):
        for i in range(80, 640, 80):
            pygame.draw.line(self.screen, (0, 0, 0), (i, 0), (i, 640))
            pygame.draw.line(self.screen, (0, 0, 0), (0, i), (640, i))
        pygame.display.flip()

    def draw_cells(self):
        n = 80
        for i in range(8):
            for j in range(8):
                x = n * i
                y = n * j
                if (i+j) % 2 == 0:
                    pygame.draw.rect(self.screen, (255, 255, 255), (y, x, 80, 80))
                else:
                    pygame.draw.rect(self.screen, (155, 118, 83), (y, x, 80, 80))
                if not (self.board[i][j] == 0 or self.board[i][j] == -1):
                    temp = self.board[i][j]
                    color = temp.color[0]
                    if temp.score == 1:
                        piece = pygame.image.load(PATH+ color+'Pawn.png')
                        self.screen.blit(piece, (y, x))
                    elif temp.score == 3:
                        piece = pygame.image.load(PATH+ color+'Knight.png')
                        self.screen.blit(piece, (y, x))
                    elif temp.score == 3.5:
                        piece = pygame.image.load(PATH+ color + 'Bishop.png')
                        self.screen.blit(piece, (y, x))
                    elif temp.score == 5:
                        piece = pygame.image.load(PATH+ color + 'Rook.png')
                        self.screen.blit(piece, (y, x))
                    elif temp.score == 9:
                        piece = pygame.image.load(PATH+ color + 'Queen.png')
                        self.screen.blit(piece, (y, x))
                    elif temp.score == 10:
                        piece = pygame.image.load(PATH+ color + 'King.png')
                        self.screen.blit(piece, (y, x))
        pygame.display.flip()

    @staticmethod
    def get_pos(coordinates):
        y, x = coordinates[0] // 80, coordinates[1] // 80
        return y, x




pygame.init()
window = pygame.display.set_mode((640, 640))
window.fill((255, 255, 255))
test = Game(window)
pygame.display.set_caption('Chess')

running = True
selected = None
white_turn = True
#print(test.board[0][4].can_castle(test.board, (0, 6)))
while running:
    test.draw_cells()
    #if test.checkmate():
    #    running = False
    #if test.stalemate(white_turn):
    #    running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if selected is None:
                cur_x, cur_y = event.pos
                pos_y, pos_x = test.get_pos((cur_y, cur_x))
                if type(test.board[pos_y][pos_x]) == int:
                    continue
                if (test.board[pos_y][pos_x].color == 'black' and white_turn)\
                   or (test.board[pos_y][pos_x].color == 'white' and not white_turn):
                    continue

                selected = test.board[pos_y][pos_x]
            else:
                cur_x, cur_y = event.pos
                pos_y, pos_x = test.get_pos((cur_y, cur_x))
                if selected.move(test.board, (pos_y, pos_x)):
                    if white_turn:
                        white_turn = False
                    else:
                        white_turn = True
                selected = None
                continue


while not running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True
