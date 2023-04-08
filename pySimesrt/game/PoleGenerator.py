import random
import copy

class Slider:
    def __init__(self, pole, convertor):
        self.pole = pole
        self.convertor = convertor
        self.laststep = None

        self.nowpose = [0, 0]

        self.path = []
        self.count = 0
        self.fullcount = len(pole)*len(pole[0])

    def mathXY(self, nap):

        pose = self.nowpose.copy()
        if nap == "D":
            pose[1] += 1
        elif nap == "U":
            pose[1] -= 1
        elif nap == "R":
            pose[0] += 1
        elif nap == "L":
            pose[0] -= 1

        return pose

    def move(self, nap):

        info = self.convertor.moving[self.laststep][nap]
        self.pole[self.nowpose[0]][self.nowpose[1]]["type"] = info["type"]
        self.pole[self.nowpose[0]][self.nowpose[1]]["orin"] = info["orin"]

        self.path += [self.nowpose.copy()]
        self.count += 1
        self.nowpose = self.mathXY(nap)
        self.laststep = nap

    def canstep(self, nap):
        pose = self.mathXY(nap)
        if pose[0] < 0 or pose[1] < 0 or pose[0] >= len(self.pole) or pose[1] >= len(self.pole[0]):
            return 0
        return 1

    def visited(self, nap):
        pose = self.mathXY(nap)
        if pose in self.path:
            return 1
        return 0


class PGenerator:
    def randowzer(pole):

        pole = copy.deepcopy(pole)
        for i in pole:
            for j in i:
                j["orin"] = random.randint(0, 3)
        return pole

    def getL1(convertor, emptypole):
        slid = Slider(emptypole, convertor)

        slid.laststep = "R"
        slid.nowpose = [1, 0]
        emptypole[0][0]["type"] = 0
        emptypole[0][0]["orin"] = 1

        nownap = 1
        while 1:
            if nownap == 1:
                if slid.canstep("R"):
                    slid.move("R")
                else:
                    nownap = -1
                    if slid.canstep("D"):
                        slid.move("D")
                    else:
                        break
            elif nownap == -1:
                if slid.canstep("L"):
                    slid.move("L")
                else:
                    nownap = 1
                    if slid.canstep("D"):
                        slid.move("D")
                    else:
                        break

            # if slid.count > 6:
            #     break
        emptypole[slid.nowpose[0]][slid.nowpose[1]]["type"] = 0

        return emptypole.copy(), PGenerator.randowzer(emptypole.copy())

    def getL2(convertor, emptypole):
        slid = Slider(emptypole, convertor)

        slid.laststep = "D"
        slid.nowpose = [0, 1]
        emptypole[0][0]["type"] = 0
        emptypole[0][0]["orin"] = 2

        nownap = 1
        while 1:
            if nownap == 1:
                if slid.canstep("D"):
                    slid.move("D")
                else:
                    nownap = -1
                    if slid.canstep("R"):
                        slid.move("R")
                    else:
                        break
            elif nownap == -1:
                if slid.canstep("U"):
                    slid.move("U")
                else:
                    nownap = 1
                    if slid.canstep("R"):
                        slid.move("R")
                    else:
                        break

            # if slid.count > 6:
            #     break
        emptypole[slid.nowpose[0]][slid.nowpose[1]]["type"] = 0

        return emptypole.copy(), PGenerator.randowzer(emptypole.copy())

    def getL3(convertor, emptypole):
        slid = Slider(emptypole, convertor)

        slid.laststep = "R"
        slid.nowpose = [1, 0]
        emptypole[0][0]["type"] = 0
        emptypole[0][0]["orin"] = 1

        nownap = 1
        while 1:
            if slid.count - 100 == slid.fullcount:
                break

            if nownap == 1:
                if slid.canstep("R"):
                    slid.move("R")
                else:
                    nownap = 2
                    if slid.canstep("D"):
                        slid.move("D")
                    else:
                        break


            elif nownap == 2:
                if slid.canstep("L") and not slid.visited("L"):
                    slid.move("L")
                else:
                    nownap = 3

            elif nownap == 3:
                if slid.canstep("D"):
                    slid.move("D")
                else:
                    nownap = 4
                    if slid.canstep("R") and slid.laststep != "L":
                        slid.move("R")
                    else:
                        break
            elif nownap == 4:
                if slid.canstep("U") and not slid.visited("U"):
                    slid.move("U")
                else:
                    nownap = 1

        emptypole[slid.nowpose[0]][slid.nowpose[1]]["type"] = 0

        return emptypole.copy(), PGenerator.randowzer(emptypole.copy())
