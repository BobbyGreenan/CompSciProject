import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

running = True

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("My Platformer")

background_color = (51, 204, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.y_velocity = 0
        self.is_jumping = False
        self.mask = pygame.mask.from_surface(self.image)

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP] and not self.is_jumping:
            self.y_velocity = -14
            self.is_jumping = True
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        self.y_velocity += 0.5
        self.rect.move_ip(0, self.y_velocity)

        # Check if the player has landed
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.is_jumping = False

    # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

        # Check for collision with platforms using collision masks
        for sprite in sprites:
            offset_x = sprite.rect.left - self.rect.left
            offset_y = sprite.rect.top - self.rect.top
            if self.mask.overlap(sprite.mask, (offset_x, offset_y)):
                self.y_velocity = 0
                self.is_jumping = False

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Platform, self).__init__()
        self.image = pygame.image.load("platform.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

player = Player(screen_width / 9, screen_height - 205)

clock = pygame.time.Clock()

class star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(star, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("star.png").convert_alpha(), (50, 50))
        self.rect = self.image.get_rect(center=(x, y))

Star = star(700, 180)

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("spike.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))


# Define the sprites list here
sprites = []
for i in range(3):
    x = 130 + i * 290
    y = (screen_height - 100) - (i * 100)
    sprites.append(Platform(x, y))



spikes = []
for i in range(20):
    x = 0 + i * 50
    y = (25)
    spikes.append(Spike(x, y))


while running:
    screen.fill(background_color)
    screen.blit(player.image, player.rect)
    screen.blit(Star.image, Star.rect)



    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    # Draw all sprites
    for sprite in sprites:
        screen.blit(sprite.image, sprite.rect)





    for sprite in sprites:
        if player.rect.colliderect(sprite.rect):
            player.y_velocity = 0
            player.is_jumping = False

    for sprite in spikes:
        if player.rect.colliderect(sprite.rect):
            running = False # Stop the game loop if player touches a spike


    pygame.display.flip()

    pressed_keys = pygame.key.get_pressed()



    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    clock.tick(45)

pygame.quit()