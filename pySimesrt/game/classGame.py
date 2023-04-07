import pygame
pygame.init()
import classOther
import classMyUI
from sittingsloader import GetSittings




class Game:
    def __init__(self,win_size=(800,1000)):


        self.CLOCK = pygame.time.Clock()

        self.winsize = win_size
        self.mainscreen = pygame.display.set_mode(self.winsize)

        self.__sittings_init()
        self.__pole_init()

        self.initTime = 0
        self.timeToEnd = 100 #2 * 60*1000

        self.timerUI = classMyUI.TimeLabel((self.winsize[0]//2 - 50, self.winsize[1] - 50), (100, 50), (0, 100, 0))
        self.buttons = [
            classMyUI.Button((20, self.winsize[1] - 50), "New Game", (100,50),self.RestartGame),
            classMyUI.Button((self.winsize[0] - 90, self.winsize[1] - 50), "Quite", (100, 50), self.quitGame)
        ]

    def __sittings_init(self):
        self.__sitt = GetSittings()
        self.pole_size = (self.__sitt["size"], self.__sitt["size"])
        self.__nowlevel = self.__sitt["level"]

    def __pole_init(self):
        self.blocksize = (self.winsize[0] - 20) // (self.pole_size[0])
        self.pole = classOther.Pole(self.pole_size, self.__nowlevel)
        self.convertor = self.pole.convertor

    def __drawPole(self):

        for x in range(self.pole.size[0]):
            for y in range(self.pole.size[1]):
                b = self.pole.blocks[x][y]
                self.__drawblock(x*self.blocksize + 10, y*self.blocksize + 10, b)

    def RestartGame(self):
        self.initTime = 0
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

        self.timerUI.draw(self.mainscreen, ((self.timeToEnd - self.initTime)//1000))
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

    def update(self):
        if self.initTime >= self.timeToEnd:
            self.pole.showSolution()

    def run(self):

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.__clickUpdate(event.pos)

            self.update()
            self.initTime += self.CLOCK.tick(60)

            self.mainscreen.fill((255, 255, 255))

            self.__drawPole()
            self.__drawUI()

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    Game().run()