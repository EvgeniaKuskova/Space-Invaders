import pygame
import random
import json
import datetime
from objects import Ship, Bullet, Bunker, Enemy, MysteryShip, Text, Object
from parameters import Parameters
import os


class Game:
    def __init__(self, score: int, level: int, restart=False, open_menu=True):
        pygame.init()
        self.screen = pygame.display.set_mode((Parameters.WIDTH, Parameters.HEIGHT))
        pygame.display.set_caption("Space Invaders")

        icon_path = os.path.join(Parameters.IMAGES_FOLDER, 'icon.png')
        icon = pygame.image.load(icon_path).convert_alpha()
        pygame.display.set_icon(icon)

        if level > 4:
            speed = Parameters.LEVEL[4]["speed"] - 50 * (level - 4)
            if level > 22:
                speed = 100
            level = 4
        else:
            speed = Parameters.LEVEL[level]["speed"]

        self.level = level

        self.ship = Ship.Ship()
        self.bullet = Bullet.Bullet()
        self.bunkers = [Bunker.Bunker(60), Bunker.Bunker(308),
                        Bunker.Bunker(640 - Bunker.Bunker(0).width)]
        self.enemies = []
        self.enemy_direction = 1
        self.initialize_enemies(Parameters.LEVEL[level]["rows"], Parameters.LEVEL[level]["cols"])
        self.enemy_bullet = Bullet.Bullet()
        self.mystery_ship = MysteryShip.MysteryShip()

        font_path = os.path.join(Parameters.FONTS_FOLDER, 'font.ttf')
        self.font = pygame.font.Font(font_path, 20)
        self.big_font = pygame.font.Font(font_path, 40)

        self.clock = pygame.time.Clock()
        self.enemy_timer = pygame.USEREVENT + 1
        self.enemy_bullet_timer = pygame.USEREVENT + 2
        self.mystery_ship_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.mystery_ship_timer, 15000)
        pygame.time.set_timer(self.enemy_timer, 1000)
        pygame.time.set_timer(self.enemy_bullet_timer, speed)

        self.score = score
        self.gameplay = restart
        self.menu = open_menu
        self.lose = False
        self.statistic = False
        self.pause = False

        self.hearts = []
        for i in range(3):
            heart_image_path = os.path.join(Parameters.IMAGES_FOLDER, 'heart.png')
            self.hearts.append(Object.Object(heart_image_path, 2, 530 + 40 * i, 30))

    def initialize_enemies(self, rows: int, cols: int):
        x = 40
        y = 160
        for i in range(rows):
            for j in range(cols):
                if i == 0 and rows > 2:
                    enemy_image_path = os.path.join(Parameters.IMAGES_FOLDER, 'enemy_second_type.png')
                    cost = 20
                else:
                    enemy_image_path = os.path.join(Parameters.IMAGES_FOLDER, 'enemy_first_type.png')
                    cost = 10
                self.enemies.append(Enemy.Enemy(enemy_image_path, x, y, 10, cost))
                x += 45
            x = 40
            y += 50

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))

            if self.menu:
                self.draw_menu()

            elif self.statistic:
                self.draw_statistic()

            elif self.gameplay:
                self.enemy_bullet.get_rect()
                self.bullet.get_rect()
                self.ship.get_rect()
                self.check_keys()
                self.move_bullet()
                self.bullet.get_rect()
                self.check_conflict_bullet_and_bunker()
                self.check_kill_ship()
                self.check_enemy_direction()
                self.check_kill_enemy()
                self.check_kill_mystery_ship()
                self.draw_game()

            elif self.lose:
                self.draw_lose_screen()
                if self.score > 0:
                    self.update_high_scores()

            elif self.pause:
                self.draw_pause_screen()

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
                        self.mystery_ship.x = Parameters.WIDTH
            pygame.display.update()
            self.clock.tick(Parameters.FPS)
        pygame.quit()

    def draw_menu(self):
        text_start = Text.Text(self.font, 'CLICK TO START', 'white', 440, self.screen)
        text_high_score = Text.Text(self.font, 'HIGH SCORES', 'green', 360, self.screen)
        Text.Text(self.big_font, "SPACE INVADERS", "red", 25, self.screen)
        mouse = pygame.mouse.get_pos()
        if text_start.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            self.gameplay = True
            self.menu = False
        elif text_high_score.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            self.statistic = True
            self.menu = False
        picture = pygame.image.load(os.path.join(Parameters.IMAGES_FOLDER, "menu.png")).convert_alpha()
        scaled_picture = pygame.transform.scale(picture, (picture.get_width() * 3,
                                                          picture.get_height() * 3))
        self.screen.blit(scaled_picture, ((Parameters.WIDTH - scaled_picture.get_width()) // 2, 115))

    def draw_statistic(self):
        Text.Text(self.big_font, "TOP 3", "green", 40, self.screen)
        text_return = Text.Text(self.font, "CLICK TO RETURN MENU", "green",
                                400, self.screen)
        mouse = pygame.mouse.get_pos()
        if text_return.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            self.menu = True
            self.statistic = False
            return
        high_scores = self.load_high_scores()
        high_scores.sort(key=lambda x: x['score'], reverse=True)
        high_scores = high_scores[:3]
        y = 150
        for score in high_scores:
            score_text = f"{score['score']} - {score['date']}"
            Text.Text(self.font, score_text, "white", y, self.screen)
            y += 70

    def draw_game(self):
        Text.Text(self.font, 'SCORE', 'white', 20, self.screen, 40)
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
        Text.Text(self.big_font, 'YOU LOSE', 'red', 150, self.screen)
        text_restart = Text.Text(self.font, 'CLICK TO TRY AGAIN', 'white',
                                250, self.screen)
        text_return = Text.Text(self.font, "CLICK TO RETURN MENU", "green",
                                380, self.screen)
        mouse = pygame.mouse.get_pos()
        a = text_restart.rect.collidepoint(mouse)
        b = pygame.mouse.get_pressed()[0] == 1
        if a and b:
            self.reset_game(0, 0, restart=True, open_menu=False)
        if text_return.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            self.reset_game(0, 0)

    def draw_pause_screen(self):
        Text.Text(self.big_font, 'PAUSE', 'white', 50, self.screen)
        text_continue = Text.Text(self.big_font, 'CLICK TO CONTINUE', 'green',
                                  200, self.screen)
        text_return = Text.Text(self.font, "CLICK TO RETURN MENU", "white",
                                400, self.screen)
        mouse = pygame.mouse.get_pos()
        if text_continue.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            self.gameplay = True
            self.pause = False
        if text_return.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            self.update_high_scores()
            self.reset_game(0, 0)

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
            self.reset_game(self.score, self.level + 1, restart=True, open_menu=False)

    def check_conflict_bullet_and_bunker(self):
        for bullet, bunkers in [(self.enemy_bullet, self.bunkers), (self.bullet, self.bunkers)]:
            for bunker in bunkers:
                bunker.get_rect()
                if bullet.rect.colliderect(bunker.rect):
                    bullet.reset() if bullet == self.enemy_bullet else bullet.reset(self.ship)
                    if bunker.destroy():
                        bunkers.remove(bunker)

    def check_kill_ship(self):
        if self.enemy_bullet.rect.colliderect(self.ship.rect):
            if len(self.hearts) > 1:
                self.hearts.pop(0)
                self.enemy_bullet.reset()
                self.ship.reset()
            else:
                self.gameplay = False
                self.lose = True

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.ship.x > 20:
            self.ship.x -= self.ship.speed
        if keys[pygame.K_RIGHT] and self.ship.x < Parameters.WIDTH - 20 - self.ship.width:
            self.ship.x += self.ship.speed
        if keys[pygame.K_SPACE] and not self.bullet.is_shooting:
            self.bullet.x = self.ship.x + self.ship.width / 2 - self.bullet.width / 2
            self.bullet.draw(self.screen)
            self.bullet.is_shooting = True
        if keys[pygame.K_ESCAPE]:
            self.gameplay = False
            self.pause = True

    def move_bullet(self):
        if self.bullet.is_shooting:
            self.bullet.y -= self.bullet.speed
            self.bullet.draw(self.screen)
            if self.bullet.y < 0:
                self.bullet.reset(self.ship)

        if self.enemy_bullet.is_shooting:
            self.enemy_bullet.draw(self.screen)
            if self.enemy_bullet.y > Parameters.HEIGHT:
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
            self.mystery_ship.x = Parameters.WIDTH

    @staticmethod
    def save_scores(high_scores):
        with open(os.path.join(Parameters.DATA_FOLDER, 'high_scores.json'), 'w') as file:
            json.dump(high_scores, file, indent=4)

    @staticmethod
    def load_high_scores():
        try:
            with open(os.path.join(Parameters.DATA_FOLDER, 'high_scores.json'), 'r') as file:
                return json.load(file)
        except OSError:
            return []

    def update_high_scores(self):
        if self.score == 0:
            return
        scores = self.load_high_scores()
        if scores is None:
            scores = []
        scores.append({'score': self.score, 'date': datetime.datetime.now().strftime("%Y-%m-%d")})
        self.score = 0
        self.save_scores(scores)

    def reset_game(self, score: int, level: int, restart=False, open_menu=True):
        if level > 4:
            speed = Parameters.LEVEL[4]["speed"] - 50 * (level - 4)
            if level > 22:
                speed = 100
            level = 4
        else:
            speed = Parameters.LEVEL[level]["speed"]

        self.level = level

        self.ship.reset()
        self.bullet.reset(self.ship)
        self.enemies = []
        self.enemy_direction = 1
        self.initialize_enemies(Parameters.LEVEL[level]["rows"], Parameters.LEVEL[level]["cols"])
        self.enemy_bullet.reset()
        self.mystery_ship.is_moving = False

        self.score = score
        self.gameplay = restart
        self.menu = open_menu
        self.lose = False
        self.statistic = False
        self.pause = False

        self.hearts = []
        for i in range(3):
            heart_image_path = os.path.join(Parameters.IMAGES_FOLDER, 'heart.png')
            self.hearts.append(Object.Object(heart_image_path, 2, 530 + 40 * i, 30))
        self.bunkers = [Bunker.Bunker(60), Bunker.Bunker(308),
                        Bunker.Bunker(640 - Bunker.Bunker(0).width)]
        pygame.time.set_timer(self.enemy_bullet_timer, speed)
