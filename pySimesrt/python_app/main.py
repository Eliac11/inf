class game:
    def __init__(self,startpos=(1,1)):
        self.Rpos = startpos
        self.PoleSize = (100,100)


    def setRpos(self,x,y):
        self.Rpos = (x,y)

    def updateRpos(self,dx,dy):
        x,y = self.getRpos()
        self.SetRpos(x+dx, y+dy)

    def getRpos(self) -> tuple:
        return self.Rpos

    def ChekCanStatePos(self,x,y) -> bool:
        return not (x < 1 or y < 1 or x > self.PoleSize[0] or y > self.PoleSize[1])

    def inputChekXY(self) -> bool:
        x, y = map(int, input("input new 'x,y':").split(","))

        if not self.ChekCanStatePos(x, y):
            print("coordinates outside the field, enter correct data\n\n")
            return 1

        self.setRpos(x,y)
        return 0

    def inputChekSide(self) -> bool:
        c,k = map(str, input("input step '(L/R/U/D),k':").split(","))

        k = int(k)

        nx, ny = self.getRpos()
        if c in "LR":
            nx += k * ( 1 if c == "R" else -1)
        elif c in "UD":
            ny += k * (1 if c == "D" else -1)
        else:
            print("input is invalid")
            return 1

        if not self.ChekCanStatePos(nx,ny):
            print("The robot goes out of the field")
            return 1

        self.setRpos(nx,ny)
        return 0


    def run(self, inputmode:int):

        if inputmode == 1:
            maininput = self.inputChekXY
        else:
            maininput = self.inputChekSide

        while 1:
            try:
                while maininput():
                    pass
            except Exception as e:
                print(str(e))
            print("The robot is now in position: ", *self.getRpos())


if __name__ == "__main__":
    game().run(2)