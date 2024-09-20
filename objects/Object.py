import pygame


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
