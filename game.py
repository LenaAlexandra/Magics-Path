import pygame
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = pygame.Rect((300, 250, 50, 50))

run = True

while run:
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 0, 0), player)
    player.y = 550

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0)
    if key[pygame.K_d] == True:
        player.move_ip(1, 0)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
    
    

time.sleep(5)

pygame.quit()
