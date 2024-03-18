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
        self.rect.x = self.velocity_x
        self.rect.y = self.velocity_y

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
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.velocity_x = -3
                elif event.key == pygame.K_RIGHT:
                    player.velocity_x = 3
                elif event.key == pygame.K_UP:
                    player.velocity_y = -3
                elif event.key == pygame.K_DOWN:
                    player.velocity_y = 3
        elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.velocity_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.velocity_x = 0

    pygame.display.update()
    