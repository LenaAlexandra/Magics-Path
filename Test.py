import pygame
import random
import math

# Pygame initialisieren
pygame.init()
pygame.font.init()

# Konstanten
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LEVEL_WIDTH = 3000
FPS = 60

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
DARK_BLUE = (25, 25, 112)

# Elementar-Farben
FIRE_COLOR = (255, 69, 0)
ICE_COLOR = (135, 206, 250)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Grünerer Sprite für den Magier
        self.width = 40
        self.height = 60
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        
        # Magier zeichnen
        # Robe (dunkelblau)
        pygame.draw.polygon(self.image, DARK_BLUE, 
                          [(10, 20), (30, 20), (35, 55), (5, 55)])
        # Kopf (hautfarben)
        pygame.draw.circle(self.image, (255, 218, 185), (20, 15), 10)
        # Hut (lila)
        pygame.draw.polygon(self.image, PURPLE, 
                          [(10, 10), (30, 10), (20, 0)])
        # Stab (braun)
        pygame.draw.rect(self.image, BROWN, [35, 15, 5, 40])
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0
        self.platforms = None
        
        # RPG Stats
        self.max_hp = 150
        self.hp = self.max_hp
        self.max_mana = 100
        self.mana = self.max_mana
        self.armor = 5
        self.fire_resistance = 0.2
        self.ice_resistance = 0.2
        self.weapon_damage = 20
        self.spell_power = 15
        
        # Weltposition
        self.world_x = x
        
    def update(self):
        # Schwerkraft
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
            
        # Bewegung X
        self.world_x += self.change_x
        self.world_x = max(0, min(self.world_x, LEVEL_WIDTH - self.width))
        
        # Position auf dem Bildschirm aktualisieren
        screen_x = self.world_x
        if self.world_x > SCREEN_WIDTH // 2:
            if self.world_x < LEVEL_WIDTH - SCREEN_WIDTH // 2:
                screen_x = SCREEN_WIDTH // 2
            else:
                screen_x = SCREEN_WIDTH - (LEVEL_WIDTH - self.world_x)
        self.rect.x = screen_x
        
        # Bewegung Y
        self.rect.y += self.change_y
        
        # Kollision Y
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
            
    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 2
        
        if len(platform_hit_list) > 0:
            self.change_y = -10
            
    def cast_fireball(self, projectiles):
        if self.mana >= 20:
            self.mana -= 20
            projectile = Projectile(self.rect.centerx, self.rect.centery, 10, "fire", 30)
            projectiles.add(projectile)
            return projectile
        return None

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 80
        self.height = 200
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        
        # Hauptturm
        pygame.draw.rect(self.image, BROWN, [10, 40, 60, 160])
        # Dach
        pygame.draw.polygon(self.image, RED, 
                          [(0, 40), (40, 0), (80, 40)])
        # Fenster
        for y in range(60, 160, 40):
            pygame.draw.rect(self.image, YELLOW, [20, y, 15, 20])
            pygame.draw.rect(self.image, YELLOW, [45, y, 15, 20])
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, element_type, damage):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.element_type = element_type
        
        if element_type == "fire":
            # Feuerball-Animation
            pygame.draw.circle(self.image, FIRE_COLOR, (10, 10), 8)
            pygame.draw.circle(self.image, YELLOW, (10, 10), 4)
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.world_x = x
        self.speed = speed
        self.damage = damage
        
    def update(self, camera_x):
        self.world_x += self.speed
        self.rect.x = self.world_x - camera_x
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Magier Platformer")
        
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        self.player = Player(50, SCREEN_HEIGHT - 100)
        self.player.platforms = self.platforms
        self.all_sprites.add(self.player)
        
        self.camera_x = 0
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.generate_level()
        
    def generate_level(self):
        # Boden
        floor = Platform(0, SCREEN_HEIGHT - 40, LEVEL_WIDTH, 40)
        self.platforms.add(floor)
        self.all_sprites.add(floor)
        
        # Plattformen und Monster generieren
        for i in range(20):
            x = random.randint(300, LEVEL_WIDTH - 300)
            y = random.randint(100, SCREEN_HEIGHT - 100)
            width = random.randint(100, 200)
            platform = Platform(x, y, width, 20)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
            
        # Turm am Ende erstellen
        self.tower = Tower(LEVEL_WIDTH - 150, SCREEN_HEIGHT - 240)
        self.all_sprites.add(self.tower)
        
    def update_camera(self):
        # Kamera folgt dem Spieler
        if self.player.world_x < SCREEN_WIDTH // 2:
            self.camera_x = 0
        elif self.player.world_x > LEVEL_WIDTH - SCREEN_WIDTH // 2:
            self.camera_x = LEVEL_WIDTH - SCREEN_WIDTH
        else:
            self.camera_x = self.player.world_x - SCREEN_WIDTH // 2
            
    def draw_status_bars(self):
        # HP Bar
        pygame.draw.rect(self.screen, RED, [10, 10, 200, 20])
        pygame.draw.rect(self.screen, GREEN, 
                        [10, 10, 200 * (self.player.hp/self.player.max_hp), 20])
        
        # Mana Bar
        pygame.draw.rect(self.screen, BLACK, [10, 40, 200, 20])
        pygame.draw.rect(self.screen, BLUE, 
                        [10, 40, 200 * (self.player.mana/self.player.max_mana), 20])
        
        # Text
        hp_text = self.font.render(f"HP: {int(self.player.hp)}/{self.player.max_hp}", 
                                 True, WHITE)
        mana_text = self.font.render(f"Mana: {int(self.player.mana)}/{self.player.max_mana}", 
                                   True, WHITE)
        self.screen.blit(hp_text, (220, 10))
        self.screen.blit(mana_text, (220, 40))
        
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    elif event.key == pygame.K_f:  # Feuerball
                        self.player.cast_fireball(self.projectiles)
                        
            # Spieler-Bewegung
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.change_x = -5
            elif keys[pygame.K_RIGHT]:
                self.player.change_x = 5
            else:
                self.player.change_x = 0
                
            # Mana-Regeneration
            self.player.mana = min(self.player.max_mana, self.player.mana + 0.1)
                
            # Updates
            self.all_sprites.update()
            self.update_camera()
            
            # Projektile mit Kamera-Offset updaten
            for projectile in self.projectiles:
                projectile.update(self.camera_x)
                
            # Zeichnen
            self.screen.fill(BLACK)
            
            # Alle Sprites mit Kamera-Offset zeichnen
            for sprite in self.all_sprites:
                if isinstance(sprite, Player):
                    self.screen.blit(sprite.image, sprite.rect)
                else:
                    self.screen.blit(sprite.image, 
                                   (sprite.rect.x - self.camera_x, sprite.rect.y))
                
            # Projektile zeichnen
            for projectile in self.projectiles:
                self.screen.blit(projectile.image, projectile.rect)
                
            # Status Bars
            self.draw_status_bars()
            
            # Gewinnbedingung pr�fen
            if abs(self.player.world_x - (LEVEL_WIDTH - 150)) < 50:
                running = False
                self.show_victory_screen()
                
            pygame.display.flip()
            self.clock.tick(FPS)
            
    def show_victory_screen(self):
        self.screen.fill(BLACK)
        text = self.font.render("Victory! You reached the tower!", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()