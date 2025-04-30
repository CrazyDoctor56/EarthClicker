import pygame
from screeninfo import get_monitors

pygame.init()
pygame.font.init()
pygame.mixer.init()

monitor = get_monitors()[0]
WIDTH, HEIGHT = monitor.width, monitor.height
FPS = 60

WHITE = (255, 255, 255)

energy = 999999
base_epc = 1
epc_bonus = 0
epc_price = 200

sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Earth Clicker")
pygame.display.set_icon(pygame.image.load("icon.png"))
clock = pygame.time.Clock()

medium_font = pygame.font.SysFont("comicsans", 30)
small_font = pygame.font.SysFont("comicsans", 22)

background = pygame.image.load("background.png")
click_sound = pygame.mixer.Sound("click.mp3")
purchase_sound = pygame.mixer.Sound("purchase.mp3")

pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1, 0.0)

class Planet:
    def __init__(self, image_path, price, epc):
        self.image = pygame.image.load(image_path)
        self.price = price
        self.epc = epc
        self.purchased = False

planets = [
    Planet("earth_lvl_1.png", 0, 1),
    Planet("earth_lvl_2.png", 500, 5),
    Planet("earth_lvl_3.png", 1500, 10),
    Planet("earth_lvl_4.png", 3000, 20),
]

current_planet_index = 0
current_planet = planets[current_planet_index]

rotation_angle = 0
rotation_speed = 0.2
scale_factor = 1
scaling = False
flash_texts = []

earth_rect = current_planet.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

upgrade_button_rect = pygame.Rect(WIDTH - 350, HEIGHT - 120, 300, 70)
planet_button_rect = pygame.Rect(50, HEIGHT - 120, 300, 70)
exit_button_rect = pygame.Rect(WIDTH - 150, 30, 100, 50)

def draw_planet():
    rotated_image = pygame.transform.rotate(current_planet.image, rotation_angle)
    rotated_rect = rotated_image.get_rect(center=earth_rect.center)
    scaled_image = pygame.transform.scale(rotated_image, (int(rotated_image.get_width() * scale_factor), int(rotated_image.get_height() * scale_factor)))
    scaled_rect = scaled_image.get_rect(center=earth_rect.center)
    sc.blit(scaled_image, scaled_rect.topleft)
    return scaled_rect

def draw_buttons():
    pygame.draw.rect(sc, (50, 150, 220), planet_button_rect)
    if current_planet_index < len(planets) - 1:
        planet_price = planets[current_planet_index + 1].price
        planet_label = "+New Planet" if not planets[current_planet_index + 1].purchased else "Next Selected"
        sc.blit(medium_font.render(f"{planet_label}", 1, WHITE), (planet_button_rect.x + 20, planet_button_rect.y + 20))
        sc.blit(small_font.render(f"{planet_price} Energy", 1, WHITE), (planet_button_rect.x + 20, planet_button_rect.y - 30))
    else:
        sc.blit(medium_font.render("No More Planets", 1, WHITE), (planet_button_rect.x + 20, planet_button_rect.y + 20))

    pygame.draw.rect(sc, (50, 200, 50), upgrade_button_rect)
    sc.blit(medium_font.render(f"+1 EPC", 1, WHITE), (upgrade_button_rect.x + 20, upgrade_button_rect.y + 20))
    sc.blit(small_font.render(f"{epc_price} Energy", 1, WHITE), (upgrade_button_rect.x + 20, upgrade_button_rect.y - 30))

    pygame.draw.rect(sc, (200, 50, 50), exit_button_rect)
    sc.blit(medium_font.render("Exit", 1, WHITE), (exit_button_rect.x + 10, exit_button_rect.y + 10))

def get_total_epc():
    return base_epc + epc_bonus

def draw_flash_texts():
    for text, pos, alpha in flash_texts[:]:
        surface = small_font.render(text, True, (255, 255, 0))
        surface.set_alpha(alpha)
        sc.blit(surface, pos)
        new_alpha = alpha - 5
        if new_alpha <= 0:
            flash_texts.remove((text, pos, alpha))
        else:
            flash_texts[flash_texts.index((text, pos, alpha))] = (text, (pos[0], pos[1]-1), new_alpha)

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                planet_rect = draw_planet()
                if planet_rect.collidepoint(pos):
                    click_sound.play()
                    earned = get_total_epc()
                    energy += earned
                    flash_texts.append((f"+{earned}", pos, 255))
                    scaling = True

                if upgrade_button_rect.collidepoint(pos) and energy >= epc_price:
                    energy -= epc_price
                    epc_bonus += 1
                    epc_price += 100
                    purchase_sound.play()

                if planet_button_rect.collidepoint(pos) and current_planet_index < len(planets) - 1:
                    next_planet = planets[current_planet_index + 1]
                    if not next_planet.purchased and energy >= next_planet.price:
                        energy -= next_planet.price
                        next_planet.purchased = True
                        current_planet_index += 1
                        current_planet = next_planet
                        earth_rect = current_planet.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        
                        # Оновлюємо EPC після покупки нової планети
                        epc_bonus += current_planet.epc
                        purchase_sound.play()

                if exit_button_rect.collidepoint(pos):
                    game = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                scaling = False

    sc.blit(background, (0, 0))
    rotation_angle = (rotation_angle + rotation_speed) % 360
    scale_factor = 1.05 if scaling else 1
    draw_planet()

    sc.blit(medium_font.render(f"Energy: {energy}", 1, WHITE), (50, 50))

    draw_buttons()
    draw_flash_texts()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()