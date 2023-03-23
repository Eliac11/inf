import pygame
pygame.init()

import classOther

class Game:

    def __init__(self,win_size=(500,600), pole_size=(10, 10)):

        self.mainscreen = pygame.display.set_mode(win_size)
        self.blocksize = (win_size[0] - 20 )//(pole_size[0])

        self.pole = classOther.Pole(pole_size)
        self.convertor = self.pole.convertor

    def __drawPole(self):

        for x in range(self.pole.size[0]):
            for y in range(self.pole.size[1]):
                b = self.pole.blocks[x][y]
                self.__drawblock(x*self.blocksize + 10,y*self.blocksize + 10,b)
    def __drawblock(self,x,y,b):
        siz = self.blocksize
        x = x
        y = y
        siz = siz
        color = (200,0,200) if b["light"] else (100, 100, 100)
        pygame.draw.rect(self.mainscreen, (0, 0, 0), [x, y, siz, siz])
        coord = self.convertor.counvertcoord(x, y, siz, b["type"], b["orin"])
        pygame.draw.lines(self.mainscreen, color, False, coord, 4)

    def run(self):

        running = True
        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.pole.clickblock((event.pos[0]-5)//self.blocksize, (event.pos[1]-5)//self.blocksize)

            # Fill the background with white
            self.mainscreen.fill((255, 255, 255))

            self.__drawPole()

            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()

if __name__ == "__main__":
    Game().run()