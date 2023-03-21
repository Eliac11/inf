from ctypes import *
# импорт библиотеки из лабы на плюсах
cal = CDLL('./libtest.so')

# ввод количества чисел для вывода и создания массива этой длины
m = [0]*int(input("Input N: "))

#  Создание Си подобного массива
c_m = (c_int * len(m))(*m)

# Поиск чисел
cal.calculate_primes(c_m, len(m))

# вывод всех простых чисел
for i,r in enumerate(c_m):
    if r:
        print(i)
