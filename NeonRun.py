import pygame
from pygame.locals import *

pygame.init()

fenetre = pygame.display.set_mode((1920, 1080), FULLSCREEN)

#background
fond = pygame.image.load("NRR background1.png").convert()
fenetre.blit(fond, (0,0))

#character
perso = pygame.image.load("NRR still test.png").convert_alpha()
DEFAULT_IMAGE_SIZE = (192,192)
perso = pygame.transform.scale(perso, DEFAULT_IMAGE_SIZE)
position_perso = perso.get_rect()
fenetre.blit(perso, position_perso)

pygame.display.flip()

y_gravity = 1
jump_height = 20
y_velocity = jump_height

continuer = 1
pygame.key.set_repeat(10,10)
while continuer:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            continuer = 0
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                position_perso = position_perso.move(5,0)
            if event.key == K_LEFT:
                position_perso = position_perso.move(-5,0)
            if event.key == K_UP:
                position_perso = position_perso.move(0,-5)
            if event.key == K_DOWN:
                position_perso = position_perso.move(0,5)
                
                
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, position_perso)

    pygame.display.flip()

