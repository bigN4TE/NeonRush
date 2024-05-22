import pygame
from pygame.locals import *
from pygame import mixer
import time
import pickle
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Neon Run')


"""pygame.mixer.music.load('Assets/Music/.mp4')
pygame.mixer.music.play(-1, 0.0, 5000)
notes_fx = pygame.mixer.sound('Assets/Audio/.mp4')
notes_fx.set_volume(0.5)
run_fx = pygame.mixer.sound('Assets/Audio/.mp4')
run_fx.set_volume(0.5)
jump_fx = pygame.mixer.sound('Assets/Audio/.mp4')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.sound('Assets/Audio/.mp4')
game_over_fx.set_volume(0.5)
button_fx = pygame.mixer.sound('Assets/Audio/.mp4')
button_fx.set_volume(0.5)"""

#font
font_score = pygame.font.SysFont('OS X', 75)

#tile size
tile_size = 128
img_size = (128, 128)

game_over = 0

main_menu = True
dialogue_menu1 = False
dialogue_menu2 = False

level = 0
max_levels = 1

score = 0

#colors
orange = (255, 165, 0)

#background
background = pygame.image.load('Assets/Backgrounds/Full Background.png')

#restart
gameover_menu = pygame.image.load('Assets/Menus/Game Over.png')
restart = pygame.image.load('Assets/Buttons/Retry.png')
restart = pygame.transform.scale(restart, (384, 192))

#main menu
start = pygame.image.load('Assets/Menus/Start Menu.png')
play = pygame.image.load('Assets/Buttons/Play.png')
play = pygame.transform.scale(play, (384, 192))
next = pygame.image.load('Assets/misc/Note 2.png')

#dialogues
dialogue1 = pygame.image.load('Assets/Dialogue/Dialogue 1.png')
dialogue2 = pygame.image.load('Assets/Dialogue/Dialogue 2.png')

#tile grid
def draw_grid():
    for line in range(0, 25):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#level reset
def reset_level(level):
    player.reset(100, screen_height - 335)
    pig_group.empty()
    cables_group.empty()
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    return world

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
                """button_fx.play()"""
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
            if key[pygame.K_UP] and not self.in_air:
                """jump_fx.play()"""
                self.vel_y = -20
                self.in_air = True
            if key[pygame.K_LEFT]:
                """run_fx.play()"""
                dx -= 20
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                """run_fx.play()"""
                dx += 20
                self.counter += 1
                self.direction = 1

            """if:"""
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.direction = 0
                """if self.direction == 0:
                    self.image = self.image_front[self.index]
                if self.direction == 1:
                    self.image = self.image_right[self.index]
                if self.direction == -1:
                    self.image = self.image_left[self.index]"""
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
                if self.index >= len(self.image_still):
                    self.index = 0
                if self.index >=  len(self.image_jump_right):
                    self.index = 0

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
                """game_over_fx.play()"""
            
            if pygame.sprite.spritecollide(self, cables_group, False):
                game_over = -1
                """game_over_fx.play()"""
            
            #coordinates update
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > -100:
                self.rect.y -= 5

        if self.direction == 1:
            self.image = self.image_right[self.index]
        elif self.direction == -1:
            self.image = self.image_left[self.index]
        else:
            self.image = self.image_still[self.index]

        screen.blit(self.image, self.rect)
        """pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)"""

        return game_over

    def reset(self, x, y):
        self.image_right = []
        self.image_left = []
        self.image_jump_right = []
        self.image_jump_left = []
        self.image_still = []
        self.index = 0
        self.counter = 0
        for num in range(1, 9):
            img_right = pygame.image.load(f'Assets/Character/Walk {num}.png')
            img_right = pygame.transform.scale(img_right, (128, 128))
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_right.append(img_right)
            self.image_left.append(img_left)
        self.image = self.image_right[self.index]
        for num in range(1, 6):
            img_still = pygame.image.load(f'Assets/Character/Still {num}.png')
            img_still = pygame.transform.scale(img_still, (128, 128))
            self.image_still.append(img_still)
        self.image = self.image_still[self.index]
        for num in range (1, 10):
            img_jumpr = pygame.image.load(f"Assets/Character/Jump {num}.png")
            img_jumpr = pygame.transform.scale(img_jumpr, (128, 128))
            img_jumpl = pygame.transform.flip(img_jumpr, True, False)
            self.image_jump_right.append(img_jumpr)
            self.image_jump_left.append(img_jumpl)
        self.image = self.image_jump_right[self.index]
        self.dead_image = pygame.image.load('Assets/Character/Death.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.direction = 0
        self.in_air = True

# enemy1
class Enemy1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f'Assets/Pig1/Pig1 Walk {i}.png') for i in range(1, 4)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.animation_speed = 5

    def update(self):
        self.move_counter += 1
        if self.move_counter % self.animation_speed == 0:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.rect.x += self.move_direction
        if abs(self.move_counter) > 128:
            self.move_direction *= -1
            self.move_counter *= -1
            for i in range(len(self.images)):
                self.images[i] = pygame.transform.flip(self.images[i], True, False)

#enemy2
class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f'Assets/Pig2/Pig2 Walk {i}.png') for i in range(1, 4)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.animation_speed = 5

    def update(self):
        self.move_counter += 1
        if self.move_counter % self.animation_speed == 0:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.rect.x += self.move_direction
        if abs(self.move_counter) > 128:
            self.move_direction *= -1
            self.move_counter *= -1
            for i in range(len(self.images)):
                self.images[i] = pygame.transform.flip(self.images[i], True, False)

#cables
class Cables(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Assets/Tiles/Cable.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#exit
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Assets/Items/Guitar.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#notes
class Notes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Assets/Items/Note 1.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        drum_img = pygame.image.load('Assets/Tiles/Drum.png')
        
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
                if tile == 7:
                    cables = Cables(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    cables_group.add(cables)
                if tile == 8:
                    pig1 = Enemy1(col_count * tile, row_count * tile_size)
                    pig_group.add(pig1)
                if tile == 9:
                    pig2 = Enemy2(col_count * tile, row_count * tile_size)
                    pig_group.add(pig2)
                if tile == 10:
                    note = Notes(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    notes_group.add(note)
                if tile == 11:
                    exit = Exit(col_count * tile_size, row_count * tile_size)
                    exit_group.add(exit)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

#tile placement
world_data = [
[4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
[4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
[4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
[4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
[4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
[4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
[4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 4],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

pygame.display.flip()

#Loop
player = Player(256, screen_height - 335)
pig_group = pygame.sprite.Group()
cables_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
notes_group = pygame.sprite.Group()
world = World(world_data)
restart_button = Button(screen_width // 2 - 175, screen_height // 2 + 250, restart)
play_button = Button(screen_width // 2 - 200, screen_height // 2 + 100 , play)
next_button1 = Button(screen_width // 2 + 700, screen_height // 2 + 100, next)
next_button2 = Button(screen_width // 2 + 700, screen_height // 2 + 100, next)

score_note = Notes(tile_size * 7 + 10, tile_size + 32)
notes_group.add(score_note)

if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

run = True
pygame.key.set_repeat(10,10)
while run:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            run = False

    screen.blit(background, (0, 0))
    if main_menu == True:
        screen.blit(start, (0, 0))
        if play_button.draw():
            main_menu = False
            dialogue_menu1 = True
    
    else:
        if dialogue_menu1 == True:
            screen.blit(dialogue1, (0, 0))
            if next_button1.draw():
                dialogue_menu1 = False
                dialogue_menu2 = True

        elif dialogue_menu2 == True:
            screen.blit(dialogue2, (0, 0))
            if next_button2.draw():
                dialogue_menu2 = False
        
        world.draw()
        """draw_grid()"""

        if game_over == 0:
            pig_group.update()
            cables_group.update()
            exit_group.update()
            notes_group.update()
            if pygame.sprite.spritecollide(player, notes_group, True):
                score += 1
                """notes_fx.play()"""
            draw_text(str(score), font_score, orange, tile_size * 7 + 64, 168)
    
        pig_group.draw(screen)
        cables_group.draw(screen)
        notes_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)
     
        #if player dead
        if game_over == -1:
            screen.blit(gameover_menu, (0, 0))
            if restart_button.draw():
                player.reset(256, screen_height - 335)
                game_over = 0
                score = 0

        if game_over == 1:
            level += 1
            if level <= max_levels:
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                if restart_button.draw():
                    level = 1
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

    pygame.display.update()

pygame.quit()