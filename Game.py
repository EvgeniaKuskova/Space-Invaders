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
        self.big_font = pygame.font.Font('fonts/font.ttf', 40)
        self.text_lose = self.big_font.render('YOU LOSE', True, 'red')
        self.text_restart = self.font.render('CLICK TO TRY AGAIN', True, 'white')

        self.clock = pygame.time.Clock()
        self.enemy_timer = pygame.USEREVENT + 1
        self.enemy_bullet_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, 700)
        pygame.time.set_timer(self.enemy_bullet_timer, 2000)

        self.score = 0
        self.gameplay = True

        self.hearts = []
        for i in range(3):
            self.hearts.append(Objects.Object('images/heart.png',
                                              2, 530 + 40 * i, 30))

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

            if self.gameplay:
                self.check_keys()
                self.move_bullet()
                self.bullet.get_rect()
                self.check_defeat_enemy()
                self.check_conflict_bullet_and_bunker()
                self.check_kill_ship()
                self.check_enemy_direction()

                self.screen.blit(self.text_score, (40, 20))
                self.screen.blit(self.font.render(str(self.score), True, 'white'),
                                 (165, 20))

                for bunker in self.bunkers:
                    bunker.draw(self.screen)

                for heart in self.hearts:
                    heart.draw(self.screen)

                self.ship.draw(self.screen)

            else:
                self.screen.blit(self.text_lose, (200, 180))
                self.screen.blit(self.text_restart, (195, 400))
                text_restart_rect = self.text_restart.get_rect(topleft=(195, 400))
                mouse = pygame.mouse.get_pos()
                if text_restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
                    self.__init__()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.gameplay:
                    if event.type == self.enemy_timer:
                        if self.enemies:
                            for enemy in self.enemies:
                                enemy.x += enemy.speed * self.enemy_direction
                        else:
                            print("You win")
                            running = False
                    if event.type == self.enemy_bullet_timer:
                        self.enemy_bullet.is_shutting = True
                        number = random.randint(0, len(self.enemies) - 1)
                        self.enemy_bullet.x = self.enemies[number].x + self.enemies[number].width / 2
                        self.enemy_bullet.y = self.enemies[number].y
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
            enemy.get_rect()
            if self.bullet.rect.colliderect(enemy.rect):
                enemies_to_remove.append(i)
                self.bullet.reset(self.ship)
                self.score += enemy.cost
            else:
                enemy.draw(self.screen)

        for index in sorted(enemies_to_remove, reverse=True):
            del self.enemies[index]

    def check_conflict_bullet_and_bunker(self):
        self.enemy_bullet.get_rect()
        for bunker in self.bunkers:
            bunker.get_rect()
            if self.enemy_bullet.rect.colliderect(bunker.rect):
                self.enemy_bullet.is_shutting = False

            if self.bullet.y >= bunker.y and bunker.check_bullet_in_bunker(self.bullet):
                self.bullet.reset(self.ship)

    def check_kill_ship(self):
        self.ship.get_rect()
        if self.enemy_bullet.rect.colliderect(self.ship.rect):
            if len(self.hearts) > 1:
                self.hearts.pop(0)
                self.ship.reset(self.clock)
            else:
                self.gameplay = False

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.ship.x > 20:
            self.ship.x -= self.ship.speed
        if keys[pygame.K_RIGHT] and self.ship.x < WIDTH - 20 - self.ship.width:
            self.ship.x += self.ship.speed
        if keys[pygame.K_SPACE] and not self.bullet.is_shutting:
            self.bullet.x = self.ship.x + self.ship.width / 2 - self.bullet.width / 2
            self.bullet.draw(self.screen)
            self.bullet.is_shutting = True

    def move_bullet(self):
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
