import pygame
from Object import Objects


WIDTH = 700
HEIGHT = 500
FPS = 30
SCALE = 4


def initialize_enemies(enemies: list, rows: int, cols: int):
    x = 40
    y = 140
    for i in range(rows):
        for j in range(cols):
            enemies.append(Objects.Enemy('images/enemy_first_type.png', x, y, 10))
            x += 45
        x = 40
        y += 50


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)


ship = Objects.Ship()
bullet = Objects.Bullet()
bunkers = [Objects.Bunker(60), Objects.Bunker(308), Objects.Bunker(640 - Objects.Bunker(0).width)]
enemies = []
initialize_enemies(enemies, 2, 8)

font = pygame.font.Font('fonts/font.ttf', 20)

clock = pygame.time.Clock()
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 700)

running = True

enemy_direction = 1

score = 0
text_surface = font.render('SCORE', True, 'white')

leftmost_enemy = min(enemies, key=lambda e: e.x)
rightmost_enemy = max(enemies, key=lambda e: e.x + e.width)

while running:
    screen.fill((0, 0, 0))
    bullet.rect = bullet.scaled_image.get_rect(topleft=(bullet.x, bullet.y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if rightmost_enemy.x > 640 - rightmost_enemy.width:
            enemy_direction = -1
        elif leftmost_enemy.x < 60:
            enemy_direction = 1
        if event.type == enemy_timer:
            if enemies:
                for enemy in enemies:
                    enemy.x += enemy.speed * enemy_direction
            else:
                print("You win")

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
            bullet.reset(ship)

    ship.draw(screen)

    for bunker in bunkers:
        bunker.draw(screen)

    enemies_to_remove = []
    if enemies:
        for i, enemy in enumerate(enemies):
            enemy.rect = enemy.scaled_image.get_rect(topleft=(enemy.x, enemy.y))
            if bullet.rect.colliderect(enemy.rect):
                enemies_to_remove.append(i)
                bullet.reset(ship)
                score += 10
            else:
                enemy.draw(screen)

    for index in sorted(enemies_to_remove, reverse=True):
        del enemies[index]
    screen.blit(text_surface, (40, 20))
    text_score = font.render(str(score), True, 'white')
    screen.blit(text_score, (165, 20))
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
