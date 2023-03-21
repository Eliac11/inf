import sys
import csv
import statistics as stat

# Подключение модуля
from csvsplitmodule import split_data


# чтение данных из файла
def read_data_from_file(path):
    # открытие файла
    with open(path, 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',',)

        # Преобразование всех знчений в строковые
        return list(map(lambda x: list(map(float, x)), list(spamreader)[1:]))
# Просчет статистики
def calculate_statistics(data):
    ndata = []
    for i in data:
        d = [*map(lambda x: x[1], i)]
        ndata += [[len(i), stat.mean(d), stat.mode(d), stat.median(d)]]
    return ndata


# Чтение имени файла из параметров запуска
fname = sys.argv[1]

# чтение данных из файла
d = read_data_from_file(fname)
# Деление данных на пятиминутные отрезки
d = split_data(d)
# подсчет статистики по каждому отрезку
result = calculate_statistics(d)

# Вывод имен столбцов
for j in ["(Длина)", "(среднее)", "(мода)", "(медиана)"]:
    print(j, end=" " * (25 - len(j)))
print()


# Вывод значений каждого столбца
for i in result[int(sys.argv[2]):int(sys.argv[3])]:
    for j in i:
        s = str(j)
        print(s, end=" "*(25-len(s)))
    print()
