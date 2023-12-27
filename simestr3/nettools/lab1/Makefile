# Настройки компилятора
CC = gcc
CFLAGS = -Wall -Wextra

# Имя исполняемого файла
TARGET = my_project.exe

# Исходные файлы
SRCS = main.c

# Объектные файлы
OBJS = $(SRCS:.c=.o)

# Путь для установки
INSTALL_DIR = install



# Цели сборки
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

# Тестовый запуск проекта
test: $(TARGET)
	./$(TARGET)

# Установка скомпилированного проекта
install: $(TARGET)
	mkdir $(INSTALL_DIR)
	copy $(TARGET) $(INSTALL_DIR)

# Создание дистрибутива проекта
dist: $(SRCS) Makefile
	tar -czvf my_project.tar.gz $^

# Создание документации
doc:
	copy main.c manual.txt

# Очистка проекта
clean:
	del $(TARGET) $(OBJS)

# Полная очистка проекта
distclean: clean
	del $(INSTALL_DIR) my_project.tar.gz manual.txt

# Справка об использовании
help:
	@echo "Usage: make [all|test|install|dist|doc|clean|distclean|help]"

lalala:
	@echo "lalala"

.DEFAULT:
	@echo "lalallalalala"

.PHONY: all test install dist doc clean distclean help 