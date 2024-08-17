import pygame

WIDTH = 700
HEIGHT = 500
FPS = 30
SCALE = 4


class Object:
    def __init__(self, image_path: str, speed: int):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (self.image.get_width() * SCALE,
                                                                self.image.get_height() * SCALE))
        self.width = self.scaled_image.get_width()
        self.height = self.scaled_image.get_height()
        self.speed = speed
        self.x = 0
        self.y = 0

    def draw(self, screen):
        screen.blit(self.scaled_image, (int(self.x), int(self.y)))


class Ship(Object):
    def __init__(self):
        super().__init__('images/ship.png', 5)
        self.x = WIDTH / 2 - self.width / 2
        self.y = 400


class Bullet(Object):
    def __init__(self):
        super().__init__('images/bullet.png', 15)
        self.x = 0
        self.y = 400 - self.height
        self.is_shutting = False


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

icon = pygame.image.load('images/icon.png').convert_alpha()
ship = Ship()
bullet = Bullet()

pygame.display.set_icon(icon)

font = pygame.font.Font('fonts/font.ttf', 20)

running = True
clock = pygame.time.Clock()

text_surface = font.render('SCORE', True, 'white')

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    screen.blit(text_surface, (40, 20))
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
