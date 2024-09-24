from objects import Object
from parameters import Parameters
import pygame


class Enemy(Object.Object):
    def __init__(self, path: str, x: int, y: int, speed: int, cost: int):
        super().__init__(path, Parameters.SCALE, x, y)
        self.speed = speed
        self.rect = self.scaled_image.get_rect(topleft=(self.x, self.y))
        self.cost = cost
        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, 600)
