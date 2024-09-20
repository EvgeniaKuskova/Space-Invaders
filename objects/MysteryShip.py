from objects import Enemy
from parameters import Parameters


class MysteryShip(Enemy.Enemy):
    def __init__(self):
        super().__init__(Parameters.PATH_TO_IMAGES + 'mystery_ship.png', Parameters.WIDTH, 100, 3, 40)
        self.is_moving = False

    def draw(self, screen):
        if self.x + self.width > 0:
            self.x -= self.speed
            screen.blit(self.scaled_image, (int(self.x), int(self.y)))
        else:
            self.is_moving = False
