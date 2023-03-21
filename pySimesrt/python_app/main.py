# Задаем начальные координаты для робота
botxy = (1, 1)

#Обевляем функцию с обработкой программы
def F():

        print("Введите код робота :")
        #Лист для того чтобы запомнить все ккоманды
        listcomm = []

        # Блок кода где может возникнуть ошибка
        try:
            # Вечный цикл до того пока юзер не введет пустую строку
            while 1:
                d = input()
                if d == "":
                    break
                c, k = map(str, d.split(","))
                # запомиаем команду
                listcomm += [(c, int(k))]
        #Если возникла ошибка то выводи ее и выходим из функции
        except Exception as e:
            print(str(e))
            return 1

        # Лист для того чтобы запомнить все координаты
        listxy = []
        # создаем 2 переменные с новыми координатыми
        nx, ny = botxy

        # цикл в котором проходимся по всем командам в списке
        for codeline, com in enumerate(listcomm):
            c, k = com
            dx, dy = 0, 0
            if c in "LR":
                dx = k * (1 if c == "R" else -1)
            elif c in "UD":
                dy = k * (1 if c == "D" else -1)
            else:
                print(f"в линии {codeline+1} неверный ввод")
                return 1

            # Цикл в которой двигаем робота и проверяем выход за границы
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
                # если выходим выводим ошибку
                if not (1 <= nx <= 100 and 1 <= ny <= 100):
                    print(f"Error в линии {codeline+1} робот выходит за поле")
                    return 1
                # добовляем координату в список
                listxy += [[nx, ny]]

        # выводим список координат
        print("Код для робота:")
        for i in listxy:
            print(",".join(map(str,i)))
        print()
        return 0
# вечный цикл
while 1:
    # блок если в нем возникает ошибка мы ее выводим
    try:
        # вызываем функцию вечно пока в ней не возникнет ошибка
        while F():
            pass

    # слли возникает ошибка то выводим ее
    except Exception as e:
        print(str(e))