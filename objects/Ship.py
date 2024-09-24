from objects import Object
from parameters import Parameters
import os


class Ship(Object.Object):
    def __init__(self):
        path = os.path.join(Parameters.IMAGES_FOLDER, 'ship.png')
        super().__init__(path, Parameters.SCALE, 76, 430)
        self.speed = 5

    def reset(self):
        self.x = 76
        self.y = 430
