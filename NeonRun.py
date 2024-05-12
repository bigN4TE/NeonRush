import pygame
from pygame.locals import *

pygame.init()

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Neon Run')

#tile size
tile_size = 128
img_size = (128, 128)

#background
fond = pygame.image.load("background proto.png")

#tile grid
def draw_grid():
    for line in range(0, 25):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

#tile system
class World():
    def __init__(self, data):
        self.tile_list = []

        #tile assets
        stage_img1 = pygame.image.load("Floor 1.png")
        stage_img2 = pygame.image.load("Floor 2.png")
        frame_img = pygame.image.load("Floor 3.png")
        speaker_img = pygame.image.load("Speaker.png")
        drum_img = pygame.image.load("Drum.png")
        cymbals_img = pygame.image.load("Cymbals 1.png")

        #tile value
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(stage_img1, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(stage_img2, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(frame_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(speaker_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

#tile placement
world_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

#character
class Player():
    def __init__(self, x, y):

        self.image_right = []
        self.image_left = []
        self.image_jump_right = []
        self.image_jump_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 9):
            img_right = pygame.image.load(f'Character/Walk {num}.png')
            img_right = pygame.transform.scale(img_right, (128, 128))
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_right.append(img_right)
            self.image_left.append(img_left)
        self.image = self.image_right[self.index]
        """for num in range (1, 10):
            img_jumpr = pygame.image.load(f"Jump R {num}.png")
            img_jumpr = pygame.transform.scale(img_right, (192, 192))
            img_jumpl = pygame.transform.flip(img_right, True, False)
            self.image_jump_right.append(img_jumpr)
            self.image_jump_left.append(img_jumpl)
        self.image = self.image_jump_right[self.index]"""
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 1.5

    #controles
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.jumped == False:
            self.vel_y = -20
            self.jumped = True
        if key[pygame.K_UP] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 20
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 20
            self.counter += 1
            self.direction = 1

        """if""" 
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.direction = 0
            if self.direction == 1:
                self.image = self.image_right[self.index]
            if self.direction == -1:
                self.image = self.image_left[self.index]
        """elif 
            if key[pygame.K_UP] == False:
                self.counter = 0
                self.direction = 0
                if self.vel_y == 1:
                    self.image = self.image_right[self.index]
                if self.vel_y == -1:
                    self.image = self.image_left[self.index]"""

        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.image_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.image_right[self.index]
            if self.direction == -1:
                self.image = self.image_left[self.index]
        
        #gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 12
        dy += self.vel_y

        #collision
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        #coordinates update
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

pygame.display.flip()

#jump pad

#Loop
player = Player(100, screen_height - 335)
world = World(world_data)

run = True
pygame.key.set_repeat(10,10)
while run:

    screen.blit(fond, (0,0))

    world.draw()

    draw_grid()

    player.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            run = False

    pygame.display.update()

pygame.quit()