CC = gcc
INC = -I"./SDL2/include/SDL2"
LIB = -L"./SDL2/lib"
FLAGS = -c -mwindows

all: spacexplore.o
	$(CC) spacexplore.o $(LIB) -lSDL2.dll -o app 

spacexplore.o: spacexplore.c
	$(CC) $(FLAGS) $(INC) spacexplore.c