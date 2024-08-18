import pygame


WIDTH = 700
HEIGHT = 500
FPS = 30
SCALE = 4


class Object:
    def __init__(self, image_path: str, scale: int):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (self.image.get_width() * scale,
                                                                self.image.get_height() * scale))
        self.width = self.scaled_image.get_width()
        self.height = self.scaled_image.get_height()
        self.x = 0
        self.y = 0

    def draw(self, screen):
        screen.blit(self.scaled_image, (int(self.x), int(self.y)))


class Ship(Object):
    def __init__(self):
        super().__init__('images/ship.png', SCALE)
        self.x = WIDTH / 2 - self.width / 2
        self.y = 400
        self.speed = 5


class Bullet(Object):
    def __init__(self):
        super().__init__('images/bullet.png', SCALE)
        self.x = 0
        self.y = 400 - self.height
        self.is_shutting = False
        self.speed = 15

    def reset(self, ship):
        self.is_shutting = False
        self.y = ship.y - self.height


class Bunker(Object):
    def __init__(self, x: int):
        super().__init__('images/bunker.png', 5)
        self.x = x
        self.y = 350


class Enemy(Object):
    def __init__(self, path: str, x: int, y: int, speed: int):
        super().__init__(path, SCALE)
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = self.scaled_image.get_rect(topleft=(self.x, self.y))
