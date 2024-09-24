from objects import Enemy
from parameters import Parameters
import os


class MysteryShip(Enemy.Enemy):
    def __init__(self):
        path = os.path.join(Parameters.IMAGES_FOLDER, 'mystery_ship.png')
        super().__init__(path, Parameters.WIDTH, 100, 3, 40)
        self.is_moving = False

    def draw(self, screen):
        if self.x + self.width > 0:
            self.x -= self.speed
            screen.blit(self.scaled_image, (int(self.x), int(self.y)))
        else:
            self.is_moving = False
