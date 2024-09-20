from parameters import Parameters


class Text:
    def __init__(self, font, text, color, y, screen, x=None):
        self.text = font.render(text, True, color)
        if x is None:
            self.x = (Parameters.WIDTH - self.text.get_width()) // 2
        else:
            self.x = x
        self.y = y
        screen.blit(self.text, (self.x, self.y))
        self.rect = self.text.get_rect(topleft=(self.x, self.y))
