import pygame
import Game


class Object:
    def __init__(self, image_path: str, scale: int, x: int, y: int):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (self.image.get_width() * scale,
                                                                self.image.get_height() * scale))
        self.width = self.scaled_image.get_width()
        self.height = self.scaled_image.get_height()
        self.x = x
        self.y = y
        self.rect = None

    def draw(self, screen):
        screen.blit(self.scaled_image, (int(self.x), int(self.y)))

    def get_rect(self):
        self.rect = self.scaled_image.get_rect(topleft=(self.x, self.y))


class Ship(Object):
    def __init__(self):
        super().__init__(Game.PATH_TO_IMAGES + 'ship.png', Game.SCALE, 76, 450)
        self.speed = 5

    def reset(self, clock):
        self.x = 76
        self.y = 450
        clock.tick(10)


class Bullet(Object):
    def __init__(self):
        super().__init__(Game.PATH_TO_IMAGES + 'bullet.png', Game.SCALE, 0, 0)
        self.y = 400 - self.height
        self.is_shooting = False
        self.speed = 15

    def reset_ship_bullet(self, ship):
        self.is_shooting = False
        self.y = ship.y - self.height

    def reset_enemy_bullet(self):
        self.is_shooting = False
        self.y = 0


class Bunker(Object):
    def __init__(self, x: int):
        super().__init__(Game.PATH_TO_IMAGES + 'bunker.png', 5, x, 350)
        self.condition = 0

    def destroy(self):
        self.condition += 1
        if self.condition < 5:
            image_path = f"bunker_{self.condition}.png"
            self.image = pygame.image.load(Game.PATH_TO_IMAGES + image_path).convert_alpha()
            self.scaled_image = pygame.transform.scale(self.image, (self.image.get_width() * 5,
                                                                    self.image.get_height() * 5))
        return self.condition > 4


class Enemy(Object):
    def __init__(self, path: str, x: int, y: int, speed: int, cost: int):
        super().__init__(path, Game.SCALE, x, y)
        self.speed = speed
        self.rect = self.scaled_image.get_rect(topleft=(self.x, self.y))
        self.cost = cost
        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, 600)


class MysteryShip(Enemy):
    def __init__(self):
        super().__init__(Game.PATH_TO_IMAGES + 'mystery_ship.png', Game.WIDTH, 100, 3, 40)
        self.is_moving = False

    def draw(self, screen):
        if self.x + self.width > 0:
            self.x -= self.speed
            screen.blit(self.scaled_image, (int(self.x), int(self.y)))
        else:
            self.is_moving = False


class Text:
    def __init__(self, font, text, color, y, screen, x=None):
        self.text = font.render(text, True, color)
        if x is None:
            self.x = (Game.WIDTH - self.text.get_width()) // 2
        else:
            self.x = x
        self.y = y
        screen.blit(self.text, (self.x, self.y))
        self.rect = self.text.get_rect(topleft=(self.x, self.y))
