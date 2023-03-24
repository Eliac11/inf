import pygame
pygame.init()
import classOther
import classMyUI


class Game:
    def __init__(self,win_size=(800,1000), pole_size=(10, 10)):
        self.winsize = win_size
        self.mainscreen = pygame.display.set_mode(self.winsize)
        self.blocksize = (win_size[0] - 20) // (pole_size[0])

        self.pole = classOther.Pole(pole_size)
        self.convertor = self.pole.convertor


        self.buttons = [
            classMyUI.Button((20, self.winsize[1] - 50), "New Game",(100,50),self.RestartGame),
            classMyUI.Button((self.winsize[0] - 90, self.winsize[1] - 50), "Quite", (100, 50), self.quitGame)
        ]

    def __drawPole(self):

        for x in range(self.pole.size[0]):
            for y in range(self.pole.size[1]):
                b = self.pole.blocks[x][y]
                self.__drawblock(x*self.blocksize + 10,y*self.blocksize + 10, b)

    def RestartGame(self):
        self.pole.regeneratePole()
    def quitGame(self):
        quit()

    def __drawblock(self,x,y,b):
        siz = self.blocksize
        x = x
        y = y
        siz = siz
        color = (200,0,200) if b["light"] else (100, 100, 100)
        pygame.draw.rect(self.mainscreen, (0, 0, 0), [x, y, siz, siz])
        coord = self.convertor.counvertcoord(x, y, siz, b["type"], b["orin"])
        pygame.draw.lines(self.mainscreen, color, False, coord, 4)

    def __drawUI(self):
        for i in self.buttons:
            i.draw(self.mainscreen)

    def __clickUpdate(self,pos):

        for i in self.buttons:
            if i.click(pos[0], pos[1]):
                return

        try:
            self.pole.clickblock((pos[0] - 5) // self.blocksize, (pos[1] - 5) // self.blocksize)

        except Exception as e:
            print(str(e))

    def run(self):

        running = True
        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.__clickUpdate(event.pos)

            # Fill the background with white
            self.mainscreen.fill((255, 255, 255))

            self.__drawPole()
            self.__drawUI()
            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()

if __name__ == "__main__":
    Game().run()