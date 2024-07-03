import pygame
from pygame.locals import (
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    KEYDOWN,
    QUIT,
)

pygame.init()
running = True
vspeed = 14

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

   def update_player(self, pressed_keys):
       if pressed_keys[K_UP] and not self.is_jumping:
           self.y_velocity = -13
           self.is_jumping = True
       #if pressed_keys[K_DOWN]:
           #self.y_velocity = 13

       if pressed_keys[K_LEFT]:
           self.rect.move_ip(-5, 0)
       if pressed_keys[K_RIGHT]:
           self.rect.move_ip(5, 0)

       self.y_velocity += 0.5
       self.rect.move_ip(0, self.y_velocity)

       if self.rect.bottom >= screen_height:
          self.rect.bottom = screen_height
          self.is_jumping = False

       if self.rect.left < 0:
            self.rect.left = 0
       if self.rect.right > screen_width:
            self.rect.right = screen_width
       if self.rect.top <= 0:
            self.rect.top = 0
       if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

       for sprite in platforms:
            offset_x = sprite.rect.left - self.rect.left
            offset_y = sprite.rect.top - self.rect.top
            if self.mask.overlap(sprite.mask, (offset_x, offset_y)):
                self.y_velocity = 0
                self.is_jumping = False



player = Player(screen_width / 9, screen_height - 205)


class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Platform, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("platform.png").convert_alpha(), (200, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height() 

platforms = []
for i in range(3):
    x = 130 + i * 290
    y = (screen_height - 100) - (i * 100)
    platforms.append(Platform(x, y))


class spike(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(
            pygame.image.load("spike.png").convert_alpha(), (800, 80))
        self.rect = self.image.get_rect(center=(x, y))

    def draw_hitbox(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)


Spike = spike(screen_width/2, 25)
#for i in range(20):
#    x = 50 + i * 50
#    y = (25)
#    Spike = spike(x, y)


class star(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(star, self).__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("star.png").convert_alpha(), (50, 50))
        self.rect = self.image.get_rect(center=(x, y))


Star = star(700, 180)

clock = pygame.time.Clock()

while running:
    screen.fill(background_color)
    screen.blit(player.image, player.rect)
    screen.blit(Star.image, Star.rect)
    screen.blit(Spike.image, Spike.rect)
    
    for sprite in platforms:
        screen.blit(sprite.image, sprite.rect)

    #for sprite in spikes:
        #screen.blit(sprite.image, sprite.rect)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    if player.rect.colliderect(Star.rect):
        running = False

    for sprite in platforms:
        if player.rect.colliderect(sprite.rect):
            player.y_velocity = 0
            player.is_jumping = False


    if player.rect.colliderect(Spike.rect):
        running = False

    if not running:
        break
        
    pygame.display.flip()

    pressed_keys = pygame.key.get_pressed()

    pressed_keys = pygame.key.get_pressed()

    player.update_player(pressed_keys)

    clock.tick(45)

pygame.quit()
