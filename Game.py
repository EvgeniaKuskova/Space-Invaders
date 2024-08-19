import pygame
from Objects import Objects
import random

WIDTH = 700
HEIGHT = 500
FPS = 30
SCALE = 4


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load('images/icon.png').convert_alpha()
        pygame.display.set_icon(icon)

        self.ship = Objects.Ship()
        self.bullet = Objects.Bullet()
        self.bunkers = [Objects.Bunker(60), Objects.Bunker(308),
                        Objects.Bunker(640 - Objects.Bunker(0).width)]
        self.enemies = []
        self.enemy_direction = 1
        self.initialize_enemies(2, 8)
        self.enemy_bullet = Objects.Bullet()

        self.font = pygame.font.Font('fonts/font.ttf', 20)
        self.text_score = self.font.render('SCORE', True, 'white')

        self.clock = pygame.time.Clock()
        self.enemy_timer = pygame.USEREVENT + 1
        self.enemy_bullet_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, 700)
        pygame.time.set_timer(self.enemy_bullet_timer, 1500)

        self.score = 0

    def initialize_enemies(self, rows: int, cols: int):
        x = 40
        y = 140
        for i in range(rows):
            for j in range(cols):
                self.enemies.append(Objects.Enemy('images/enemy_first_type.png',
                                                  x, y, 10, 10))
                x += 45
            x = 40
            y += 50

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.bullet.get_rect()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.check_enemy_direction()
                if event.type == self.enemy_timer:
                    if self.enemies:
                        for enemy in self.enemies:
                            enemy.x += enemy.speed * self.enemy_direction
                    else:
                        print("You win")
                        running = False
                if event.type == self.enemy_bullet_timer and not self.enemy_bullet.is_shutting:
                    self.enemy_bullet.is_shutting = True
                    number = random.randint(0, len(self.enemies) - 1)
                    self.enemy_bullet.x = self.enemies[number].x + self.enemies[number].width / 2
                    self.enemy_bullet.y = self.enemies[number].y

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.ship.x > 20:
                self.ship.x -= self.ship.speed
            if keys[pygame.K_RIGHT] and self.ship.x < WIDTH - 20 - self.ship.width:
                self.ship.x += self.ship.speed
            if keys[pygame.K_SPACE] and not self.bullet.is_shutting:
                self.bullet.x = self.ship.x + self.ship.width / 2 - self.bullet.width / 2
                self.bullet.draw(self.screen)
                self.bullet.is_shutting = True

            if self.bullet.is_shutting:
                self.bullet.y -= self.bullet.speed
                self.bullet.draw(self.screen)
                if self.bullet.y < 0:
                    self.bullet.reset(self.ship)

            if self.enemy_bullet.is_shutting:
                self.enemy_bullet.draw(self.screen)
                if self.enemy_bullet.y > HEIGHT:
                    self.enemy_bullet.is_shutting = False
                else:
                    self.enemy_bullet.y += 10

            self.ship.draw(self.screen)

            for bunker in self.bunkers:
                bunker.draw(self.screen)

            self.check_defeat_enemy()

            self.screen.blit(self.text_score, (40, 20))
            text_score = self.font.render(str(self.score), True, 'white')
            self.screen.blit(text_score, (165, 20))

            pygame.display.update()
            self.clock.tick(FPS)

    def check_enemy_direction(self):
        leftmost_enemy = min(self.enemies, key=lambda e: e.x)
        rightmost_enemy = max(self.enemies, key=lambda e: e.x + e.width)
        if rightmost_enemy.x > 640 - rightmost_enemy.width:
            self.enemy_direction = -1
        elif leftmost_enemy.x < 60:
            self.enemy_direction = 1

    def check_defeat_enemy(self):
        enemies_to_remove = []
        for i, enemy in enumerate(self.enemies):
            enemy.rect = enemy.scaled_image.get_rect(topleft=(enemy.x, enemy.y))
            if self.bullet.rect.colliderect(enemy.rect):
                enemies_to_remove.append(i)
                self.bullet.reset(self.ship)
                self.score += enemy.cost
            else:
                enemy.draw(self.screen)

        for index in sorted(enemies_to_remove, reverse=True):
            del self.enemies[index]

