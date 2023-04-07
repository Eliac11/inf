import random


class PGenerator:
    def randowzer(self,pole):
        pass
    def _getL1(self, emptypole):



        for indx, i in enumerate(emptypole):
            for indy, j in enumerate(i):
                if indx == 0 or indx + 1 == self.size[0]:
                    j["type"] = 2
                else:
                    j["type"] = 1

        self.blocks[0][0]["type"] = 0