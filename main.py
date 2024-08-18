import pygame
from Object import Objects


WIDTH = 700
HEIGHT = 500
FPS = 30
SCALE = 4

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

icon = pygame.image.load('images/icon.png').convert_alpha()
ship = Objects.Ship()
bullet = Objects.Bullet()
bunkers = [Objects.Bunker(60), Objects.Bunker(308), Objects.Bunker(640 - Objects.Bunker(0).width)]
enemies = []
x = 40
y = 140
for i in range(2):
    for j in range(8):
        enemies.append(Objects.Enemy('images/enemy_first_type.png', x, y, 10))
        x += 45
    x = 40
    y += 50

pygame.display.set_icon(icon)

font = pygame.font.Font('fonts/font.ttf', 20)

running = True
clock = pygame.time.Clock()
enemy_clock = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_clock, 700)

global_direction = 1

text_surface = font.render('SCORE', True, 'white')

while running:
    screen.fill((0, 0, 0))
    bullet.rect = bullet.scaled_image.get_rect(topleft=(bullet.x, bullet.y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        leftmost_enemy = min(enemies, key=lambda e: e.x)
        rightmost_enemy = max(enemies, key=lambda e: e.x + e.width)
        if rightmost_enemy.x > 640 - rightmost_enemy.width:
            global_direction = -1
        elif leftmost_enemy.x < 60:
            global_direction = 1
        if event.type == enemy_clock:
            for enemy in enemies:
                enemy.x += enemy.speed * global_direction

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship.x > 20:
        ship.x -= ship.speed
    if keys[pygame.K_RIGHT] and ship.x < WIDTH - 20 - ship.width:
        ship.x += ship.speed
    if keys[pygame.K_SPACE] and not bullet.is_shutting:
        bullet.x = ship.x + 26 - 2
        bullet.draw(screen)
        bullet.is_shutting = True

    if bullet.is_shutting:
        bullet.y -= bullet.speed
        bullet.draw(screen)
        if bullet.y < 0:
            bullet.is_shutting = False
            bullet.y = ship.y - bullet.height

    ship.draw(screen)
    for bunker in bunkers:
        bunker.draw(screen)
    for enemy in enemies:
        enemy.rect = enemy.scaled_image.get_rect(topleft=(enemy.x, enemy.y))
        if bullet.rect.colliderect(enemy.rect):
            enemies.remove(enemy)
            bullet.is_shutting = False
            bullet.y = ship.y - bullet.height
        else:
            enemy.draw(screen)
    screen.blit(text_surface, (40, 20))
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
