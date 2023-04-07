import random
import pygame

import PoleGenerator

class TypesBlocks:
    def __init__(self):
        self.points = {
                "D": (1, 2),
                "U": (1, 0),
                "R": (2, 1),
                "L": (0, 1),
                "C": (1, 1)
        }

        self.transition = {"U": "R",
                           "R": "D",
                           "D": "L",
                           "L": "U",
                           "C": "C"}

        self.types = {
            0: ("C", "C", "U"),
            1: ("D", "C", "U"),
            2: ("L", "C", "U"),
            # 3: ("L", "U", "D", "R")
        }
        self.connection = {
            self.points["U"]: self.points["D"],
            self.points["D"]: self.points["U"],
            self.points["R"]: self.points["L"],
            self.points["L"]: self.points["R"],
            self.points["C"]: self.points["C"],
        }

        self.moving = {
            "D": {
                "D": {"type": 1, "orin": 0},
                "R": {"type": 2, "orin": 1},
                "L": {"type": 2, "orin": 0}
            },
            "U": {
                "U": {"type": 1, "orin": 0},
                "R": {"type": 2, "orin": 2},
                "L": {"type": 2, "orin": 3}
            },
            "R": {
                "U": {"type": 2, "orin": 0},
                "D": {"type": 2, "orin": 3},
                "R": {"type": 1, "orin": 1}
            },
            "L": {
                "U": {"type": 2, "orin": 1},
                "D": {"type": 2, "orin": 2},
                "L": {"type": 1, "orin": 1}
            }
        }

    def convpoints(self,nap,orin):
        nap = nap
        for i in range(orin):
            nap = self.transition[nap]

        return nap

    def GetValidPoints(self,type,orintation):

        poses = list(self.types[type])
        poses = list(map(lambda j: self.convpoints(j, orintation), poses))
        points = list(map(lambda j: self.points[j], poses))

        return points

    def counvertcoord(self, x, y, size, ty, ori) -> list:

        points = self.GetValidPoints(ty,ori)
        coord = []

        for point in points:
            xy = [x + point[0] * size // 2, y + point[1] * size // 2]
            coord += [xy]

        return coord




class Pole:
    def __init__(self, size=(10,10), level=3):
        self.size = size
        self.level = level
        self.blocks = [[{"type": 0, "orin": 0, "light": False} for i in range(size[0])] for i in range(size[1])]

        self.solvedPole = self.blocks.copy()

        self.convertor = TypesBlocks()

        self.__fillpole()
        self.__updatelight()
    def regeneratePole(self):
        self.__fillpole()
        self.__updatelight()
    def __fillpole(self):
        if self.level == 1:
            self.solvedPole, self.blocks = PoleGenerator.PGenerator.getL1(self.convertor, self.blocks.copy())

        elif self.level == 2:
            self.solvedPole, self.blocks = PoleGenerator.PGenerator.getL2(self.convertor, self.blocks.copy())
        else:
            for i in self.blocks:
                for j in i:
                    j["type"] = random.randint(1, 2)
                    j["orin"] = random.randint(0, 3)

            self.blocks[0][0]["type"] = 0
            self.blocks[0][-1]["type"] = 0

    def clearlight(self):
        for x in self.blocks:
            for y in x:
                y["light"] = False

    def __updatelight(self):
        self.clearlight()

        self.blocks[0][0]["light"] = True

        flag = True
        lx, ly = None, None
        x, y = 0, 0
        while flag:
            b_1 = self.blocks[x][y]

            for i in self.convertor.GetValidPoints(b_1["type"],b_1["orin"]):
                if i == self.convertor.points["C"]:
                    continue

                dx_1, dy_1 = i
                nx = x + dx_1 - 1
                ny = y + dy_1 - 1

                if not (nx < self.size[0] and ny < self.size[1] and nx >= 0 and ny >= 0):
                    continue

                if lx == nx and ly == ny:
                    continue

                b_2 = self.blocks[nx][ny]
                coords = self.convertor.GetValidPoints(b_2["type"],b_2["orin"])
                coords = list(map(lambda j: self.convertor.connection[j], coords))

                if (dx_1, dy_1) in coords:
                    b_2["light"] = True
                    lx, ly = x, y
                    x, y = nx, ny
                    break
                else:
                    flag = False
            else:
                break
    def showSolution(self):
        self.blocks = self.solvedPole.copy()
        self.__updatelight()
        print("Showw")

    def clickblock(self, x, y):
        self.blocks[x][y]["orin"] = (self.blocks[x][y]["orin"] + 1) % 4

        self.__updatelight()
