import pygame
pygame.init()

Screen_width = 800  # Breite des Fensters
Screen_Height = 600  # Höhe des Fensters
screen = pygame.display.set_mode((Screen_width, Screen_Height))
player = pygame.Rect((300, 250, 50, 50))

# Bewegungsvariablen
velocity_y = 0
jump_power = -15
gravity = 0.8
is_jumping = False
on_ground = True

run = True
while run:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), player)
    
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player.move_ip(-5, 0)
    elif key[pygame.K_d]:
        player.move_ip(5, 0)
    
    # Sprungmechanik
    if key[pygame.K_SPACE] and on_ground:
        velocity_y = jump_power
        on_ground = False
        is_jumping = True

    # Schwerkraft anwenden
    velocity_y += gravity
    player.y += velocity_y

    # Boden-Kollision prüfen
    if player.y > Screen_Height - player.height:
        player.y = Screen_Height - player.height
        velocity_y = 0
        on_ground = True
        is_jumping = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()
    pygame.time.Clock().tick(60)  # 60 FPS

pygame.quit()