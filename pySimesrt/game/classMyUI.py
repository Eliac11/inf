import pygame


FONT = pygame.font.SysFont("chalkduster.ttf", 29)

class Button:

    def __init__(self,pos, text, size, callback):
        self.pos = pos
        self.size = size

        self.text = text
        self.rendertext = FONT.render(self.text, True, (0, 0, 0))

        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 0, 0), self.pos + self.size)
        screen.blit(self.rendertext, self.pos)

    def click(self, x, y):
        if self.pos[0] <= x and self.pos[1] <= y and self.pos[0] + self.size[0] >= x and self.pos[1] + self.size[1] >= y:
            self.callback()
            return 1
        return 0


class TimeLabel:
    def __init__(self, pos, size, backgroundcolor=(100, 0, 0)):
        self.pos = pos
        self.size = size

        self.bgcolor = backgroundcolor

    def draw(self, screen, time=0):
        self.rendertext = FONT.render(str(time), True, (0, 0, 0))
        pygame.draw.rect(screen, self.bgcolor, self.pos + self.size)
        screen.blit(self.rendertext, self.pos)
