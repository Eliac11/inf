import random
import pygame

import PoleGenerator
# касс с прописаными типами блоков
class TypesBlocks:
    def __init__(self):

        # ключевые точки в блоке
        self.points = {
                "D": (1, 2),
                "U": (1, 0),
                "R": (2, 1),
                "L": (0, 1),
                "C": (1, 1)
        }
        # Переход из одной точки в другую при повороте
        self.transition = {"U": "R",
                           "R": "D",
                           "D": "L",
                           "L": "U",
                           "C": "C"}
        # типы блоков
        self.types = {
            0: ("C", "C", "U"), # начальный тип
            1: ("D", "C", "U"), # прямая клетка
            2: ("L", "C", "U"), # поворотная клетка
            # 3: ("L", "U", "D", "R")
        }

        # Логика соедениения соседних клеток (Верхняя сторона одной клетки соеденина с нижней сотороной другой и т.д.)
        self.connection = {
            self.points["U"]: self.points["D"],
            self.points["D"]: self.points["U"],
            self.points["R"]: self.points["L"],
            self.points["L"]: self.points["R"],
            self.points["C"]: self.points["C"],
        }
        # какой тип и орентация клетки дожены быть при  переходе из нее в следующуу клетку
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

    # Трансляция стороны клетки при повороте
    def convpoints(self,nap,orin):
        nap = nap
        for i in range(orin):
            nap = self.transition[nap]

        return nap

    # высчитывать точки линии внутри одной клетки с учетом ее поворота
    def GetValidPoints(self,type,orintation):

        poses = list(self.types[type])
        poses = list(map(lambda j: self.convpoints(j, orintation), poses))
        points = list(map(lambda j: self.points[j], poses))

        return points

    # Конвертация локальных координат внутри клетки в глобальные на поле для отрисовки
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
            self.solvedPole, self.blocks = PoleGenerator.PGenerator.getL3(self.convertor, self.blocks.copy())

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

    def checkPoleAssembled(self):
        fullcount = self.size[0]*self.size[1]
        count = 0

        for i in self.blocks:
            for j in i:
                if j["light"]:
                    count += 1
        if fullcount == count:
            return 1
        else:
            return 0

    def clickblock(self, x, y):
        self.blocks[x][y]["orin"] = (self.blocks[x][y]["orin"] + 1) % 4

        self.__updatelight()
