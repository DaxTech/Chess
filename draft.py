#! python3

import pygame
from pieces import *


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.board = self.format_board()

    @staticmethod
    def format_board():
        board = [[-1 if (z+e) % 2 == 0 else 0 for z in range(8)] for e in range(8)]
        wpawn1, wpawn2, wpawn3, wpawn4 = Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white')
        wpawn5, wpawn6, wpawn7, wpawn8 = Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white')
        wrook1, wrook2, wknight1, wknight2 = Rook('white'), Rook('white'), Knight('white'), Knight('white')
        wbishop1, wbishop2, wqueen, wking = Bishop('white'), Bishop('white'), Queen('white'), King('white')
        bpawn1, bpawn2, bpawn3, bpawn4 = Pawn('black', view=-1), Pawn('black', view=-1), Pawn('black', view=-1), Pawn('black', view=-1)
        bpawn5, bpawn6, bpawn7, bpawn8 = Pawn('black', view=-1), Pawn('black', view=-1), Pawn('black', view=-1), Pawn('black', view=-1)
        brook1, brook2, bknight1, bknight2 = Rook('black'), Rook('black'), Knight('black'), Knight('black')
        bbishop1, bbishop2, bqueen, bking = Bishop('black'), Bishop('black'), Queen('black'), King('black')
        white_pieces = [[wrook1, wknight1, wbishop1, wqueen, wking, wbishop2, wknight2, wrook2],
                        [wpawn1, wpawn2, wpawn3, wpawn4, wpawn5, wpawn6, wpawn7, wpawn8]]
        black_pieces = [[brook1, bknight1, bbishop1, bqueen, bking, bbishop2, bknight2, brook2],
                        [bpawn1, bpawn2, bpawn3, bpawn4, bpawn5, bpawn6, bpawn7, bpawn8]]
        for i in range(2):
            for j in range(8):
                board[i][j] = white_pieces[i][j]
                white_pieces[i][j].current_pos = (i, j)
        for i in range(7, 5, -1):
            for j in range(8):
                board[i][j] = black_pieces[abs(i-7)][j]
                black_pieces[abs(i-7)][j].current_pos = (i, j)

        return board

    def checkmate(self):
        for i in range(8):
            for j in range(8):
                if type(self.board[i][j]) == King:
                    king = self.board[i][j]
                    if king.check(self.board):
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
                        for piece in team:
                            if not piece.available_moves(self.board):
                                font = pygame.font.SysFont('comicsans', 80, True)
                                if king.color == 'white':
                                    text = font.render('BLACK WON', 1, (0, 0, 0))
                                else:
                                    text = font.render('WHITE WON', 1, (0, 0, 255))
                                self.screen.blit(text, (200, 200))
                                pygame.display.flip()
                                return True
        return False


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
                    pygame.draw.rect(self.screen, (155, 118, 83), (y, x, 80, 80))
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), (y, x, 80, 80))

                if not (self.board[i][j] == 0 or self.board[i][j] == -1):
                    font = pygame.font.SysFont('comicsans', 64, True)
                    temp = self.board[i][j]
                    color = (0, 0, 0) if temp.color == 'black' else (0, 0, 255)
                    if temp.score == 1:
                        text = font.render('P', 1, color)
                        self.screen.blit(text, (y, x))
                    elif temp.score == 3:
                        text = font.render('Kn', 1, color)
                        self.screen.blit(text, (y, x))
                    elif temp.score == 3.5:
                        text = font.render('B', 1, color)
                        self.screen.blit(text, (y, x))
                    elif temp.score == 5:
                        text = font.render('R', 1, color)
                        self.screen.blit(text, (y, x))
                    elif temp.score == 9:
                        text = font.render('Q', 1, color)
                        self.screen.blit(text, (y, x))
                    elif temp.score == 10:
                        text = font.render('K', 1, color)
                        self.screen.blit(text, (y, x))
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
while running:
    test.draw_cells()
    if test.checkmate():
        running = False
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