import pygame


WIDTH = 700
HEIGHT = 500
FPS = 30
SCALE = 4


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
        super().__init__('images/ship.png', SCALE, 76, 392)
        self.speed = 5

    def reset(self, clock):
        self.x = 76
        self.y = 392
        clock.tick(10)


class Bullet(Object):
    def __init__(self):
        super().__init__('images/bullet.png', SCALE, 0, 0)
        self.y = 400 - self.height
        self.is_shutting = False
        self.speed = 15

    def reset(self, ship):
        self.is_shutting = False
        self.y = ship.y - self.height


class Bunker(Object):
    def __init__(self, x: int):
        super().__init__('images/bunker.png', 5, x, 350)

    def check_bullet_in_bunker(self, bullet):
        return self.x <= bullet.x < self.x + self.width


class Enemy(Object):
    def __init__(self, path: str, x: int, y: int, speed: int, cost: int):
        super().__init__(path, SCALE, x, y)
        self.speed = speed
        self.rect = self.scaled_image.get_rect(topleft=(self.x, self.y))
        self.cost = cost
        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, 600)


class MysteryShip(Enemy):
    def __init__(self):
        super().__init__('images/mystery_ship.png', WIDTH, 100, 3, 40)
        self.is_moving = False

    def draw(self, screen):
        if self.x + self.width > 0:
            self.x -= self.speed
            screen.blit(self.scaled_image, (int(self.x), int(self.y)))
        else:
            self.is_moving = False

