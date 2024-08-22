import pygame
from Objects import Objects
import random
import json
import datetime

WIDTH = 700
HEIGHT = 500
FPS = 30
SCALE = 4
LEVEL = {0: [2500, 2, 8],
         1: [2500, 2, 10],
         2: [2000, 3, 10],
         3: [1500, 3, 10],
         4: [1000, 3, 10]}


class Game:
    def __init__(self, score: int, level: int):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load('images/icon.png').convert_alpha()
        pygame.display.set_icon(icon)

        if level > 4:
            speed = LEVEL[4][0] - 50 * (level - 4)
            if level > 22:
                speed = 100
            level = 4
        else:
            speed = LEVEL[level][0]

        self.level = level

        self.ship = Objects.Ship()
        self.bullet = Objects.Bullet()
        self.bunkers = [Objects.Bunker(60), Objects.Bunker(308),
                        Objects.Bunker(640 - Objects.Bunker(0).width)]
        self.enemies = []
        self.enemy_direction = 1
        self.initialize_enemies(LEVEL[level][1], LEVEL[level][2])
        self.enemy_bullet = Objects.Bullet()
        self.mystery_ship = Objects.MysteryShip()

        self.font = pygame.font.Font('fonts/font.ttf', 20)
        self.big_font = pygame.font.Font('fonts/font.ttf', 40)

        self.clock = pygame.time.Clock()
        self.enemy_timer = pygame.USEREVENT + 1
        self.enemy_bullet_timer = pygame.USEREVENT + 2
        self.mystery_ship_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.mystery_ship_timer, 15000)
        pygame.time.set_timer(self.enemy_timer, 1000)
        pygame.time.set_timer(self.enemy_bullet_timer, speed)

        self.score = score
        self.gameplay = True
        self.menu = False
        self.statistic = False

        self.hearts = []
        for i in range(3):
            self.hearts.append(Objects.Object('images/heart.png',
                                              2, 530 + 40 * i, 30))

    def initialize_enemies(self, rows: int, cols: int):
        x = 40
        y = 160
        for i in range(rows):
            for j in range(cols):
                if i == 0 and rows > 2:
                    self.enemies.append(Objects.Enemy('images/enemy_second_type.png',
                                                      x, y, 10, 20))
                else:
                    self.enemies.append(Objects.Enemy('images/enemy_first_type.png',
                                                      x, y, 10, 10))
                x += 45
            x = 40
            y += 50

    def run(self):
        self.menu = True
        running = True
        while running:
            self.screen.fill((0, 0, 0))

            if self.menu:
                self.draw_menu()

            elif self.statistic:
                self.draw_statistic()

            elif self.gameplay:
                self.check_keys()
                self.move_bullet()
                self.bullet.get_rect()
                self.check_conflict_bullet_and_bunker()
                self.check_kill_ship()
                self.check_enemy_direction()
                self.check_kill_enemy()
                self.check_kill_mystery_ship()
                self.draw_game()

            else:
                self.draw_lose_screen()
                if self.score > 0:
                    self.update_high_scores()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.update_high_scores()
                    running = False
                if self.gameplay and not self.menu:
                    if event.type == self.enemy_timer:
                        for enemy in self.enemies:
                            enemy.x += enemy.speed * self.enemy_direction
                    if event.type == self.enemy_bullet_timer:
                        self.enemy_bullet.is_shooting = True
                        number = random.randint(0, len(self.enemies) - 1)
                        self.enemy_bullet.x = self.enemies[number].x + self.enemies[number].width / 2
                        self.enemy_bullet.y = self.enemies[number].y
                    if event.type == self.mystery_ship_timer:
                        self.mystery_ship.is_moving = True
                        self.mystery_ship.x = WIDTH
            pygame.display.update()
            self.clock.tick(FPS)

    def draw_menu(self):
        text_start = Objects.Text(self.font, 'CLICK TO START', 'white', 420, self.screen)
        text_high_score = Objects.Text(self.font, 'HIGH SCORES', 'green', 360, self.screen)
        Objects.Text(self.big_font, "SPACE INVADERS", "red", 50, self.screen)
        mouse = pygame.mouse.get_pos()
        if text_start.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            self.gameplay = True
            self.menu = False
        if text_high_score.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            self.statistic = True
            self.menu = False
        picture = pygame.image.load("images/menu.png").convert_alpha()
        scaled_picture = pygame.transform.scale(picture, (picture.get_width() * 3,
                                                          picture.get_height() * 3))
        self.screen.blit(scaled_picture, ((WIDTH - scaled_picture.get_width()) // 2, 150))

    def draw_statistic(self):
        Objects.Text(self.big_font, "TOP 3", "green", 40, self.screen)
        text_return = Objects.Text(self.font, "CLICK TO RETURN MENU", "green",
                                   400, self.screen)
        mouse = pygame.mouse.get_pos()
        if text_return.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            self.menu = True
            self.statistic = False
        high_scores = self.load_high_scores()
        high_scores.sort(key=lambda x: x['score'], reverse=True)
        high_scores = high_scores[:3]
        y = 150
        for score in high_scores:
            score_text = f"{score['score']} - {score['date']}"
            Objects.Text(self.font, score_text, "white", y, self.screen)
            y += 70

    def draw_game(self):
        Objects.Text(self.font, 'SCORE', 'white', 20, self.screen, 40)
        self.screen.blit(self.font.render(str(self.score), True, 'white'),
                         (165, 20))
        for bunker in self.bunkers:
            bunker.draw(self.screen)
        for heart in self.hearts:
            heart.draw(self.screen)
        self.ship.draw(self.screen)
        if self.mystery_ship.is_moving:
            self.mystery_ship.draw(self.screen)

    def draw_lose_screen(self):
        Objects.Text(self.big_font, 'YOU LOSE', 'red', 150, self.screen)
        text_restart = Objects.Text(self.big_font, 'CLICK TO TRY AGAIN', 'white',
                                    250, self.screen)
        text_return = Objects.Text(self.font, "CLICK TO RETURN MENU", "green",
                                   420, self.screen)
        mouse = pygame.mouse.get_pos()
        if text_restart.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            self.__init__(0, 0)
        if text_return.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            self.__init__(0, 0)
            self.menu = True

    def check_enemy_direction(self):
        leftmost_enemy = min(self.enemies, key=lambda e: e.x)
        rightmost_enemy = max(self.enemies, key=lambda e: e.x + e.width)
        if rightmost_enemy.x > 640 - rightmost_enemy.width:
            self.enemy_direction = -1
        elif leftmost_enemy.x < 60:
            self.enemy_direction = 1

    def check_kill_enemy(self):
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

        if not self.enemies:
            self.__init__(self.score, self.level + 1)

    def check_conflict_bullet_and_bunker(self):
        self.enemy_bullet.get_rect()
        for bunker in self.bunkers:
            bunker.get_rect()
            if self.enemy_bullet.rect.colliderect(bunker.rect):
                self.enemy_bullet.is_shooting = False

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
        if keys[pygame.K_SPACE] and not self.bullet.is_shooting:
            self.bullet.x = self.ship.x + self.ship.width / 2 - self.bullet.width / 2
            self.bullet.draw(self.screen)
            self.bullet.is_shooting = True

    def move_bullet(self):
        if self.bullet.is_shooting:
            self.bullet.y -= self.bullet.speed
            self.bullet.draw(self.screen)
            if self.bullet.y < 0:
                self.bullet.reset(self.ship)

        if self.enemy_bullet.is_shooting:
            self.enemy_bullet.draw(self.screen)
            if self.enemy_bullet.y > HEIGHT:
                self.enemy_bullet.is_shooting = False
            else:
                self.enemy_bullet.y += 10

    def check_kill_mystery_ship(self):
        self.bullet.get_rect()
        self.mystery_ship.get_rect()
        if self.mystery_ship.rect.colliderect(self.bullet.rect):
            self.score += self.mystery_ship.cost
            self.bullet.reset(self.ship)
            self.mystery_ship.is_moving = False
            self.mystery_ship.x = WIDTH

    @staticmethod
    def save_scores(high_scores):
        with open('high_scores.json', 'w') as file:
            json.dump(high_scores, file, indent=4)

    @staticmethod
    def load_high_scores():
        try:
            with open('high_scores.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def update_high_scores(self):
        scores = self.load_high_scores()
        scores.append({'score': self.score, 'date': datetime.datetime.now().strftime("%Y-%m-%d")})
        self.score = 0
        self.save_scores(scores)

