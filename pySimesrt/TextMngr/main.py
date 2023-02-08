class myTextEditor:
    def __init__(self):
        self.filename = ""
        self.maintext = []
        self.tmptext = []


        self.listcommand = {"insert":self.insert,
                            "del":self.delall,
                            "delrow":self.delrow,
                            "swap":self.swap,
                            "undo":self.undo,
                            "save":self.save,
                            "exit":self.exitEditor
                            }

    def loadtext(self):

        with open(self.filename, "r") as f:
            t = f.read()
            if t[-1] == "\n":
                t = t[:-1]

            self.maintext = self.converttexttoList(t)
            self.tmptext = self.maintext.copy()

    def converttexttoList(self, text) -> list:
        return list(map(lambda x: list(x.replace("\n", "")), text.split("\n")))

    def insert(self, text, num_row=None, num_col=None):
        self.tmptext = self.maintext.copy()

        text = text[1:-1]
        num_col = None if num_row == None else num_col

        if num_row != None:
            ds = self.maintext[num_row]
            if num_col == None:
                ds += list(text)
            else:
                self.maintext[num_row] = ds[:num_col] + list(text) + ds[num_col:]
        else:
            self.maintext += [list(text)]

    def delall(self):
        self.tmptext = self.maintext.copy()
        self.maintext = []

    def delrow(self, num_row):
        self.tmptext = self.maintext.copy()
        del self.maintext[num_row]

    def swap(self, num_row_1, num_row_2):
        self.tmptext = self.maintext.copy()
        self.maintext[num_row_2], self.maintext[num_row_1] = self.maintext[num_row_1], self.maintext[num_row_2]

    def undo(self):
        self.maintext = self.tmptext.copy()

    def save(self):
        with open(self.filename, "w") as f:
            for i in self.maintext:
                f.write("".join(i) + "\n")

    def exitEditor(self):
        print("Bye")
        quit()

    def filenameInput(self) -> bool:
        self.filename = input("Input file name: ")
        try:
            open(self.filename, "r")
            self.loadtext()
        except Exception as e:
            open(self.filename,"w").close()

    def run(self):

        self.filenameInput()

        while 1:
            # print(self.maintext)
            try:
                c, *par = input("input command: ").split()
                par = map(lambda x: int(x) if x.isdigit() else x, par)
                self.listcommand[c](*par)
            except Exception as e:
                print(e,"not exit")


if __name__ == "__main__":
    myTextEditor().run()