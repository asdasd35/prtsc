import pygame
import random

# Kezdeti beállítások
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Runner")
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 24)

# Színek
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Játékos osztály
class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 70))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(midbottom=(100, HEIGHT-50))
        self.gravity = 0
        self.jump_speed = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= HEIGHT-50:
            self.rect.bottom = HEIGHT-50

    def jump(self):
        self.gravity = self.jump_speed

    def update(self):
        self.apply_gravity()

# Tárgyak osztályai
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((40, 40))
        colors = {'oil': BLACK, 'spark': RED, 'bug': YELLOW}
        self.image.fill(colors[type])
        self.rect = self.image.get_rect(midbottom=(random.randint(WIDTH+100, WIDTH+300), HEIGHT-50))
        
    def update(self):
        self.rect.x -= 7
        if self.rect.right < 0:
            self.kill()

class Collectible(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((30, 30))
        colors = {'screw': GREEN, 'sensor': WHITE, 'chip': YELLOW}
        self.image.fill(colors[type])
        self.rect = self.image.get_rect(midbottom=(random.randint(WIDTH+100, WIDTH+300), HEIGHT-100))
        
    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# Játékállapot kezelése
def main():
    robot = Robot()
    all_sprites = pygame.sprite.Group(robot)
    obstacles = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    
    score = 0
    info_text = ""
    info_timer = 0
    
    timer = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and robot.rect.bottom == HEIGHT-50:
                    robot.jump()

        # Tárgyak generálása
        timer += 1
        if timer > 50:
            timer = 0
            if random.random() < 0.3:
                type = random.choice(['oil', 'spark', 'bug'])
                obstacles.add(Obstacle(type))
            else:
                type = random.choice(['screw', 'sensor', 'chip'])
                collectibles.add(Collectible(type))
        
        # Ütközések vizsgálata
        if pygame.sprite.spritecollide(robot, obstacles, False):
            running = False
        
        for collectible in pygame.sprite.spritecollide(robot, collectibles, True):
            score += 10
            info_text = {
                'screw': "Csavar: Erősítsd meg a szerkezetet!",
                'sensor': "Szenzor: Távolságérzékelés aktiválva!",
                'chip': "Mikrochip: Processzor teljesítmény növelve!"
            }[collectible.type]
            info_timer = 30

        # Frissítések
        all_sprites.update()
        obstacles.update()
        collectibles.update()
        
        # Kirajzolás
        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, (0, HEIGHT-50), (WIDTH, HEIGHT-50), 3)
        
        obstacles.draw(screen)
        collectibles.draw(screen)
        all_sprites.draw(screen)
        
        # Infó és pontszám
        score_text = FONT.render(f"Pontok: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if info_timer > 0:
            info_display = FONT.render(info_text, True, GREEN)
            screen.blit(info_display, (WIDTH//2 - 150, 50))
            info_timer -= 1
        
        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
