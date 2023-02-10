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


    def convertcommtoxy(self):

        print("Input Robot Code(press empty enter for stop):")

        listcomm = []
        listxy = []
        try:
            while 1:
                d = input()
                if d == "":
                    break
                c, k = map(str, d.split(","))

                listcomm += [(c, int(k))]
        except Exception as e:
            print(str(e))
            return 1

        nx, ny = self.getRpos()
        for codeline, com in enumerate(listcomm):
            c, k = com
            dx, dy = 0, 0
            if c in "LR":
                dx = k * (1 if c == "R" else -1)
            elif c in "UD":
                dy = k * (1 if c == "D" else -1)
            else:
                print(f"In LIne {codeline+1} sintacsis is invalid")
                return 1


            while dx != 0 or dy != 0:
                if dx > 0:
                    nx += 1
                    dx -= 1
                elif dx < 0:
                    nx -= 1
                    dx += 1

                if dy > 0:
                    ny += 1
                    dy -= 1
                elif dy < 0:
                    ny -= 1
                    dy += 1

                if not self.ChekCanStatePos(nx, ny):
                    print(f"Error In line {codeline+1} robot goes out of the field")
                    return 1

                listxy += [[nx, ny]]

        print("Robot code:")
        for i in listxy:
            print(",".join(map(str,i)))

        return 0

    def run(self, inputmode:int):

        if inputmode == 1:
            maininput = self.inputChekXY
        elif inputmode == 2:
            maininput = self.inputChekSide
        else:
            maininput = self.convertcommtoxy

        while 1:
            try:
                while maininput():
                    pass
            except Exception as e:
                print(str(e))

            if inputmode != 3:
                print("The robot is now in position: ", *self.getRpos())


if __name__ == "__main__":
    game().run(3)