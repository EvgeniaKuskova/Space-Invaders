from objects import Object
from parameters import Parameters


class Ship(Object.Object):
    def __init__(self):
        super().__init__(Parameters.PATH_TO_IMAGES + 'ship.png', Parameters.SCALE, 76, 430)
        self.speed = 5

    def reset(self, clock):
        self.x = 76
        self.y = 430
        clock.tick(10)
