import pygame
import random

# Initialize the game engine
pygame.init()

# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

# This sets the name of the window
pygame.display.set_caption("Collision Example")

# Set the background color
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

GREEN = (0,255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)

class Ball(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # set speed
        self.velocity_x = 0
        self.velocity_y = 0

    def move(self):
        if ball.velocity_y > 0:
            if ball.rect.bottom + ball.velocity_y > screen_height:
                ball.velocity_y = 0
        if ball.velocity_y < 0:
            if ball.rect.top + ball.velocity_y <= 0:
                ball.velocity_y = 0
        if ball.velocity_x > 0:
            if ball.rect.right + ball.velocity_x > screen_width:
                ball.velocity_x = 0
        if ball.velocity_x + ball.velocity_x < 0:
            if ball.rect.left <= 0:
                ball.velocity_x = 0
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y



    def draw_rect(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)


obstacle_rect = pygame.Rect(random.randint(0, 600), random.randint(0,300), 25, 25)
obstacle_rect_block = pygame.Rect(random.randint(0, 600), random.randint(0,300), 50, 50)

if __name__ == "__main__":
    ball = Ball(GREEN, 20, 15)
    ball.rect.x = 100
    ball.rect.y = 100

    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(ball)

    clock = pygame.time.Clock()

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ball.velocity_x = -3
                elif event.key == pygame.K_RIGHT:
                    ball.velocity_x = 3
                elif event.key == pygame.K_UP:
                    ball.velocity_y = -3
                elif event.key == pygame.K_DOWN:
                    ball.velocity_y = 3
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ball.velocity_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    ball.velocity_x = 0
   

        if ball.rect.colliderect(obstacle_rect):
            ball.image.fill(RED)
        else:
            ball.image.fill(GREEN)

        if obstacle_rect_block.colliderect(ball):
            if ball.velocity_y > 0:
                if ball.rect.bottom + ball.velocity_y >= obstacle_rect_block.top and ball.rect.y + ball.velocity_y < obstacle_rect_block.y:
                    ball.velocity_y = 0
            if ball.velocity_y < 0:
                if ball.rect.top + ball.velocity_y <= obstacle_rect_block.bottom and ball.rect.y + ball.velocity_y > obstacle_rect_block.y:
                    ball.velocity_y = 0
            if ball.velocity_x > 0:
                if ball.rect.right + ball.velocity_x >= obstacle_rect_block.left and ball.rect.x + ball.velocity_x < obstacle_rect_block.x:
                    ball.velocity_x = 0
            if ball.velocity_x < 0:
                if ball.rect.left + ball.velocity_x <= obstacle_rect_block.right and ball.rect.x + ball.velocity_x > obstacle_rect_block.x:
                    ball.velocity_x = 0

        ball.move()

        screen.fill((255, 255, 255))

        ball.draw_rect()
        pygame.draw.rect(screen, BLUE, obstacle_rect)
        pygame.draw.rect(screen, ORANGE, obstacle_rect_block)

        all_sprites_list.draw(screen)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
