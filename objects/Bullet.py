from objects import Object
from parameters import Parameters
import os


class Bullet(Object.Object):
    def __init__(self):
        path = os.path.join(Parameters.IMAGES_FOLDER, 'bullet.png')
        super().__init__(path, Parameters.SCALE, 0, 0)
        self.y = 400 - self.height
        self.is_shooting = False
        self.speed = 15

    def reset(self, ship=None):
        self.is_shooting = False
        if ship:
            self.y = ship.y - self.height
        else:
            self.y = 0
