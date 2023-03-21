# переменные с именем файла, список строк, копия текста
filename = ""
maintext = []
tmptext = []

#загрузка нового файла
def loadtext():
    global filename,maintext,tmptext
    with open(filename, "r") as f:
        t = f.read()
        if t[-1] == "\n":
            t = t[:-1]

        maintext = converttexttoList(t)
        tmptext = maintext.copy()

# конвертация его в список по строкам
def converttexttoList( text) -> list:
    global filename, maintext, tmptext
    return list(map(lambda x: list(x.replace("\n", "")), text.split("\n")))

# Реализация команды добавления
def insert( text, num_row=None, num_col=None):
    global filename, maintext, tmptext
    tmptext = maintext.copy()

    text = text[1:-1]
    num_col = None if num_row == None else num_col

    if num_row != None:
        ds = maintext[num_row]
        if num_col == None:
            ds += list(text)
        else:
            maintext[num_row] = ds[:num_col] + list(text) + ds[num_col:]
    else:
        maintext += [list(text)]

# реализация удаления всего
def delall():
    global filename, maintext, tmptext
    tmptext = maintext.copy()
    maintext = []

# реализация удаления строки
def delrow( num_row):
    global filename, maintext, tmptext
    tmptext = maintext.copy()
    del maintext[num_row]
# реализация смена местами 2 строки
def swap( num_row_1, num_row_2):
    global filename, maintext, tmptext
    tmptext = maintext.copy()
    maintext[num_row_2], maintext[num_row_1] = maintext[num_row_1], maintext[num_row_2]
# реализация команды отмены последнего действия
def undo():
    global filename, maintext, tmptext
    maintext = tmptext.copy()
# реализация сохранения
def save():
    global filename, maintext, tmptext
    with open(filename, "w") as f:
        for i in maintext:
            f.write("".join(i) + "\n")
# реализация выхода
def exitEditor():
    global filename, maintext, tmptext
    print("Bye")
    quit()
# реализация ввода
def filenameInput():
    global filename, maintext, tmptext
    filename = input("Input file name: ")
    try:
        open(filename, "r")
        loadtext()
    except Exception as e:
        open(filename,"w").close()


# Загрузка файла
filenameInput()
# Список доступных команд
listcommand = {"insert": insert, "del": delall, "delrow": delrow, "swap": swap, "undo": undo, "save": save,
               "exit": exitEditor}

# Вечный цикл
while 1:
    # блок с обработкой ошибки
    try:
        # Ввод команды с параметрами
        c, *par = input("input command: ").split()
        # преобразование всех параметров в int если это возможно
        par = map(lambda x: int(x) if x.isdigit() else x, par)
        # вызов команды из списка
        listcommand[c](*par)
        print("ok")
    # Если ошибка
    except Exception as e:
        print(e,"not exit")