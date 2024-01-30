import pygame
from pygame.locals import *

pygame.init()

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Neon Run')

#background
fond = pygame.image.load("NRR background1.png").convert()
screen.blit(fond, (0,0))

#character
class Player():
    def __init__(self, x, y):
        perso = pygame.image.load("NRR still test.png").convert_alpha()
        self.personnage = pygame.transform.scale(perso, (192, 192))
        self.rect = self.personnage.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        screen.blit(self.personnage, self.rect)

pygame.display.flip()

player = Player(100, screen_height - 335)

run = 1
pygame.key.set_repeat(10,10)
while run:

    player.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            run = 0

    pygame.display.update()

