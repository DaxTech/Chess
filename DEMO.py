#! python3

import pygame
from pieces import *
from DEMO import *
from ai import heuristic

pygame.init()
window = pygame.display.set_mode((640, 640))
window.fill((255, 255, 255))
test = Game(window)
pygame.display.set_caption('Chess')

running = True
selected = None
white_turn = True
src, dsn = None, None
while running:
    heuristic(test.board)
    test.draw_cells()
    test.pawns(white_turn)
    if test.checkmate():
        running = False
    if test.stalemate(white_turn):
        running = False
    if selected is None:
        dsn, src = None, None
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
                src = selected.current_pos
                if selected.move(test.board, (pos_y, pos_x)):
                    dsn = (pos_y, pos_x)
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
