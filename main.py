import pygame
from settings import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

#GLOBALS
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earth Clicker")
pygame.display.set_icon(pygame.image.load("icon.png"))
clock = pygame.time.Clock()

#FONTS
medium_font = pygame.font.SysFont("comicsans", 30)
large_font = pygame.font.SysFont("comicsans", 50)

#IMAGES
background = pygame.image.load("background.png")
earth_lvl_1 = pygame.image.load("earth_lvl_1.png")
shop_button = pygame.image.load("shop_button.png")

#SOUNDS
pygame.mixer.music.load("background_sound.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

#CLASS
class Earth:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    def draw(self):
        sc.blit(self.image, (self.x, self.y))

class Shop:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    def draw(self):
        sc.blit(self.image, (self.x, self.y))

    def shop_screen(self):
        ...

#OBJECTS
earth = Earth(earth_lvl_1, 105, 400)
shop = Shop(shop_button, 30, 30)

#GAME
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.mixer.Sound("click.mp3").play()
                energy += 1
                


    sc.blit(background, (0, 0))
    earth.draw()
    shop.draw()
    
    #TEXT
    energy_text = medium_font.render(f"Energy: {energy}", 1, WHITE)
    sc.blit(energy_text, (280, 300))

    pygame.display.update()
    clock.tick(FPS)