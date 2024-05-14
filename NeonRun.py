import pygame
from pygame.locals import *
import time

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Neon Run')

#tile size
tile_size = 128
img_size = (128, 128)

game_over = 0

#background
background = pygame.image.load('Assets/Backgrounds/Background 0.png')

#restart
"""restart = pygame.image.load('Assets/Buttons/.png')"""

"""bg_image1 = 'Assets/Backgrounds/Background 0.png'
bg_image2 = 'Assets/Backgrounds/Background 1.png'
bg_image3 = 'Assets/Backgrounds/Background 2.png'
bg_image4 = 'Assets/Backgrounds/Background 3.png'
bg_image5 = 'Assets/Backgrounds/Background 4.png'

class AnimatedBackground(pygame.sprite.Sprite):
    def __init__(self, x, y, animations, frame_delta=3000):
        pygame.sprite.Sprite.__init__(self)
        self.animation_frames = [pygame.image.load(f'Assets/Backgrounds/Background 0.png').convert_alpha() for filename in animations]
        self.image = self.animation_frames[0]

        self.rect = self.image.get_rect()        
        self.rect.x = x
        self.rect.y = y

        self.current_frame = 0
        self.last_update = 0
        self.frame_delta = frame_delta

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delta:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]
    
    def update(self):
        self.animate()
        self.my_background = AnimatedBackground(0, 0, [bg_image1, bg_image2, bg_image3, bg_image4, bg_image1], frame_delta = 3000)"""

#tile grid
def draw_grid():
    for line in range(0, 25):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

#buttons
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action

#character
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 1.5

        if game_over == 0:

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

            """if:"""
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.direction = 0
                if self.direction == 1:
                    self.image = self.image_right[self.index]
                if self.direction == -1:
                    self.image = self.image_left[self.index]
            """elif:
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
            self.in_air = True
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
                        self.in_air = False

            if pygame.sprite.spritecollide(self, pig_group, False):
                game_over = -1
            
            """if pygame.sprite.spritecollide(self, cable_group, False):
                game_over = -1"""
            
            #coordinates update
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            """self.image = self.dead_image"""
            
            if self.rect.y > 200:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

    def reset(self, x, y):
        self.image_right = []
        self.image_left = []
        self.image_jump_right = []
        self.image_jump_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 9):
            img_right = pygame.image.load(f'Assets/Character/Walk {num}.png')
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
        self.image = self.image_jump_right[self.index]
        self.dead_image = pygame.image.load('Assets/Character/.png')"""
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

#Enemy1
class Enemy1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Assets/Pig1/Pig1 Still 1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 128:
            self.move_direction *= -1
            self.move_counter *= -1

#Cables
"""class Cables(pygame.sprit.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Assets/Tiles/.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y"""

#jump pad

#tile system
class World():
    def __init__(self, data):
        self.tile_list = []

        #tile assets
        stage_img1 = pygame.image.load('Assets/Tiles/Floor 1.png')
        stage_img2 = pygame.image.load('Assets/Tiles/Floor 2.png')
        frame_img = pygame.image.load('Assets/Tiles/Floor 3.png')
        speaker_img = pygame.image.load('Assets/Tiles/Speaker.png')
        piano_img = pygame.image.load('Assets/Tiles/Piano.png')
        drum_img = pygame.image.load('Assets/Items/Drum.png')
        
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
                if tile == 5:
                    img = pygame.transform.scale(piano_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 6:
                    img = pygame.transform.scale(drum_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                """if tile == 7:
                    cables = Cables(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    cables_group.add(cables)"""
                if tile == 8:
                    pig1 = Enemy1(col_count * tile, row_count * tile_size)
                    pig_group.add(pig1)
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

pygame.display.flip()

#Loop
player = Player(100, screen_height - 335)
pig_group = pygame.sprite.Group()
"""Cable_group = pygame.sprite.Groupe()"""
world = World(world_data)
"""restart_button = Button(screen_width // 2 - 128, screen_height // 2 + 256, restart_img)"""

run = True
pygame.key.set_repeat(10,10)
while run:

    clock.tick(fps)

    screen.blit(background, (0, 0))

    world.draw()

    draw_grid()

    if game_over == 0:
        pig_group.update()
    
    pig_group.draw(screen)
    """cables_group.draw(screen)"""

    game_over = player.update(game_over)

    #if player dead
    """if game_over == -1:
        if restart_button.draw():
            player.reset()
            game_over = 0"""

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            run = False

    pygame.display.update()

pygame.quit()