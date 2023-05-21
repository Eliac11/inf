import os

import hashlib


def myhash(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


class FileContainer:
    def __init__(self,root,name,contenthash):

        self.root = root
        self.name = name
        self.contenthash = contenthash

class DirsChecker:
    def __init__(self,path = "."):

        self.commns = {"del": self.__delite,
                       "skip": self.__skip,
                       "keep": self.__keep
                       }

        self.path = path
        self.files = []
        self.dublicates = {}

        self.dubcount = 0

    def __scanDir(self):
        for root, dirs, files in os.walk("."):
            for filename in files:

                content = open(root + "/" + filename).read()
                cont_hash = myhash(content)
                self.files.append(FileContainer(root, filename, cont_hash))


    def __serchDublic(self):

        for file in self.files:
            file: FileContainer = file

            if file.contenthash not in self.dublicates:
                self.dublicates[file.contenthash] = [file]
            else:
                self.dublicates[file.contenthash].append(file)
                self.dubcount += 1

    def __delite(self, suit, *args) -> None:

        for i in args[0]:
            f: FileContainer = suit[i]
            os.remove(f.root + "//" + f.name)

    def __skip(self, suit, *args) -> None:
        pass

    def __keep(self, suit, *args) -> None:

        for i, f in enumerate(suit):
            if i != args[0][0]:
                f: FileContainer = f
                os.remove(f.root + "//" + f.name)

    def runSurvay(self):

        self.__scanDir()
        self.__serchDublic()

        # if self.dubcount == 0:
        #     print("Dont have dublicate")
        #     return

        print("This files have dublicate")
        for suit in self.dublicates.values():
            if len(suit) == 1:
                continue

            for i, file in enumerate(suit):
                print(f"{i}) {file.name} {' '* (20 - len(file.name) )} lacalpath: {file.root}")


            while 1:
                try:
                    command = list(map(lambda x: int(x) if x.isdigit() else x, input("Enter action:  ").split()))
                    self.commns[command[0]](suit, command[1:])
                    print("Ok")
                    break
                except Exception as e:
                    raise e

            print()

if __name__ == "__main__":
    d = DirsChecker()
    d.runSurvay()

