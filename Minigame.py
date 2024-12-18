import pygame
import random

# Pygame initialisieren
pygame.init()

# Konstanten
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fenster erstellen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Verbesserte Sprungmechanik")
clock = pygame.time.Clock()

# Spieler-Einstellungen
player_x, player_y = 50, SCREEN_HEIGHT - 100
player_width, player_height = 40, 40
player_speed = 5
jump_force = -15
gravity = 0.7
y_velocity = 0
is_jumping = False

# Plattformen erstellen
platforms = [{'x': 50, 'y': SCREEN_HEIGHT - 150, 'width': 100, 'height': 20}]
for i in range(8):
    platforms.append({
        'x': random.randint(0, SCREEN_WIDTH - 100),
        'y': SCREEN_HEIGHT - (i + 2) * 80,
        'width': random.randint(80, 120),
        'height': 20
    })

# Ziel erstellen
goal = {'x': SCREEN_WIDTH - 70, 'y': 50, 'width': 40, 'height': 40}

# Vollbildmodus
is_fullscreen = False

# Hauptspiel-Schleife
running = True
while running:
    # Event-Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                y_velocity = jump_force
                is_jumping = True
            if event.key == pygame.K_F11:  # Vollbildmodus umschalten
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
                else:
                    screen = pygame.display.set_mode((800, 600))
                    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

    # Spieler-Bewegung
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Gravitation anwenden
    y_velocity += gravity
    player_y += y_velocity

    # Plattform-Kollision
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    is_jumping = True  # Standardmäßig springend, bis Kollision erkannt wird
    for platform in platforms:
        platform_rect = pygame.Rect(platform['x'], platform['y'], platform['width'], platform['height'])
        if player_rect.colliderect(platform_rect) and y_velocity > 0:
            player_y = platform['y'] - player_height
            y_velocity = 0
            is_jumping = False
            break

    # Ziel-Kollision
    goal_rect = pygame.Rect(goal['x'], goal['y'], goal['width'], goal['height'])
    if player_rect.colliderect(goal_rect):
        print("Gewonnen!")
        running = False

    # Spieler am Boden halten
    if player_y > SCREEN_HEIGHT - player_height:
        player_y = SCREEN_HEIGHT - player_height
        y_velocity = 0
        is_jumping = False

    # Bildschirmgrenzen
    player_x = max(0, min(SCREEN_WIDTH - player_width, player_x))

    # Zeichnen
    screen.fill(BLACK)
    for platform in platforms:
        pygame.draw.rect(screen, WHITE, (platform['x'], platform['y'], platform['width'], platform['height']))
    pygame.draw.rect(screen, RED, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, GREEN, (goal['x'], goal['y'], goal['width'], goal['height']))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

