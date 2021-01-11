#! python3

from GUI import *

pygame.init()
window = pygame.display.set_mode((640, 640))
window.fill((255, 255, 255))
pygame.display.set_caption('Chess')
test = Game(window)
test.main_loop()
test.end_loop()
