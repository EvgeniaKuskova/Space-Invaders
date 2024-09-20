from objects import Object
from parameters import Parameters
import pygame


class Bunker(Object.Object):
    def __init__(self, x: int):
        super().__init__(Parameters.PATH_TO_IMAGES + 'bunker.png', 5, x, 350)
        self.degree_of_destruction = 0

    def destroy(self):
        self.degree_of_destruction += 1
        if self.degree_of_destruction < 5:
            image_path = f"bunker_{self.degree_of_destruction}.png"
            self.image = pygame.image.load(Parameters.PATH_TO_IMAGES + image_path).convert_alpha()
            self.scaled_image = pygame.transform.scale(self.image, (self.image.get_width() * 5,
                                                                    self.image.get_height() * 5))
        return self.degree_of_destruction > 4
