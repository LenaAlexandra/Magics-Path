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

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0)
    
    run = False

time.sleep(5)

pygame.quit()
