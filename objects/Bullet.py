from objects import Object
from parameters import Parameters


class Bullet(Object.Object):
    def __init__(self):
        super().__init__(Parameters.PATH_TO_IMAGES + 'bullet.png', Parameters.SCALE, 0, 0)
        self.y = 400 - self.height
        self.is_shooting = False
        self.speed = 15

    def reset(self, ship=None):
        self.is_shooting = False
        if ship:
            self.y = ship.y - self.height
        else:
            self.y = 0
