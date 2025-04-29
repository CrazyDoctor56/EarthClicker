import pygame
import sys

#SETTINGS
HEIGHT = 1000
WIDTH = 1100
FPS = 60

#COLOR
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#GLOBAL
energy = 0
epc = 1
upgrade_purchased = False
new_planet_purchased = False
rotation_angle = 0
scale_factor = 1
scaling = False

pygame.init()
pygame.font.init()
pygame.mixer.init()

#SCREEN
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
earth_lvl_2 = pygame.image.load("earth_lvl_2.png")
shop_button = pygame.image.load("shop_button.png")

#SOUNDS
pygame.mixer.music.load("background_sound.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
click_sound = pygame.mixer.Sound("click.mp3")
purchase_sound = pygame.mixer.Sound("purchase.mp3")

#CLASSES
class Earth:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, rotation_angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)

        scaled_image = pygame.transform.scale(rotated_image, (int(rotated_image.get_width() * scale_factor), 
                                                              int(rotated_image.get_height() * scale_factor)))
        scaled_rect = scaled_image.get_rect(center=self.rect.center)

        sc.blit(scaled_image, scaled_rect.topleft)

    def update(self):
        global rotation_angle
        global scale_factor, scaling

        rotation_angle += 0.2

        if scaling:
            scale_factor = 1.2
        else:
            scale_factor = 1

earth_width = earth_lvl_1.get_width()
earth_height = earth_lvl_1.get_height()

earth = Earth(earth_lvl_1, (WIDTH - earth_width) // 2, (HEIGHT - earth_height) // 3)

button_width = 300
button_height = 80
button_spacing = 20

upgrade_button_rect = pygame.Rect((WIDTH - button_width) // 2, 850, button_width, button_height)
new_planet_button_rect = pygame.Rect((WIDTH - button_width) // 2, 950, button_width, button_height)

exit_button_rect = pygame.Rect(WIDTH - 170, 30, 140, 50)

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                if earth.rect.collidepoint(pos):
                    click_sound.play()
                    energy += epc

                    scaling = True

                if upgrade_button_rect.collidepoint(pos) and not upgrade_purchased and energy >= 200:
                    energy -= 200
                    epc = 2
                    upgrade_purchased = True
                    purchase_sound.play()

                if new_planet_button_rect.collidepoint(pos) and not new_planet_purchased and energy >= 500:
                    energy -= 500
                    epc = 5
                    new_planet_purchased = True
                    earth.image = earth_lvl_2
                    purchase_sound.play()

                if exit_button_rect.collidepoint(pos):
                    game = False

        if event.type == pygame.MOUSEBUTTONUP:
            scaling = False

    sc.blit(background, (0, 0))
    earth.update()
    earth.draw()

    pygame.draw.rect(sc, (255, 50, 50), exit_button_rect)
    exit_text = medium_font.render("Exit", 1, WHITE)
    sc.blit(exit_text, (exit_button_rect.x + 35, exit_button_rect.y + 10))

    energy_text = medium_font.render(f"Energy: {energy}", 1, WHITE)
    sc.blit(energy_text, (WIDTH // 2 - 50, 100))

    color = (180, 180, 180) if upgrade_purchased else (50, 200, 50)
    pygame.draw.rect(sc, color, upgrade_button_rect)
    if upgrade_purchased:
        text = medium_font.render("Purchased", 1, WHITE)
    else:
        text = medium_font.render("Upgrade: +1 EPC (200)", 1, WHITE)
    sc.blit(text, (upgrade_button_rect.x + 10, upgrade_button_rect.y + 25))

    color = (180, 180, 180) if new_planet_purchased else (50, 200, 50)
    pygame.draw.rect(sc, color, new_planet_button_rect)
    if new_planet_purchased:
        text = medium_font.render("Purchased", 1, WHITE)
    else:
        text = medium_font.render("New Planet: +5 EPC (500)", 1, WHITE)
    sc.blit(text, (new_planet_button_rect.x + 10, new_planet_button_rect.y + 25))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()