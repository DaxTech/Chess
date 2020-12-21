#! python3

import pygame


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = self.format_board()

    @staticmethod
    def format_board():
        board = [[0 for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in range(8):
                if (i+j) % 2 != 0:
                    board[i][j] = -1
        return board

    def divide(self):
        for i in range(80, 640, 80):
            pygame.draw.line(self.screen, (0, 0, 0), (i, 0), (i, 640))
            pygame.draw.line(self.screen, (0, 0, 0), (0, i), (640, i))
        pygame.display.flip()

    def draw_cells(self):
        n = 80
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == -1:
                    x = n * i
                    y = n * j
                    pygame.draw.rect(self.screen, (155, 118, 83), (x, y, 80, 80))
        pygame.display.flip()


pygame.init()
window = pygame.display.set_mode((640, 640))
window.fill((255, 255, 255))
test = Game(window)
#test.divide()
test.draw_cells()
pygame.display.set_caption('Chess')
s = pygame.image.load('C:\\Users\\Manu\\Desktop\\Pieces\\bishop.png')

window.blit(s, (168, 8))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
