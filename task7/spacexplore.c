#define SDL_MAIN_HANDLED
#include "SDL.h"
#include <stdio.h>
 
const int SCREEN_WIDTH = 1280;
const int SCREEN_HEIGHT = 960;

const int SHIP_SPEED = 20;

SDL_Window *win = NULL;
SDL_Surface *scr = NULL;
SDL_Renderer* renderer = NULL;

SDL_Surface *john = NULL;
SDL_Surface *sky = NULL;

SDL_Surface* numbs[10];



int init() {
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        // std::cout << "Can't init: " << SDL_GetError() << std::endl;
        system("pause");
        return 1;
    }

    win = SDL_CreateWindow("События", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    if (win == NULL) {
        // std::cout << "Can't create window: " << SDL_GetError() << std::endl;
        system("pause");
        return 1;
    }

    scr = SDL_GetWindowSurface(win);


    return 0;
}

int load() {
    john = SDL_LoadBMP("ship.bmp");
    sky = SDL_LoadBMP("sky.bmp");

    if (john == NULL) {
        // std::cout << "Can't load image: " << SDL_GetError() << std::endl;
        system("pause");
        return 1;
    }

    numbs[0] = SDL_LoadBMP("numbers/0.bmp");
    numbs[1] = SDL_LoadBMP("numbers/1.bmp");
    numbs[2] = SDL_LoadBMP("numbers/2.bmp");
    numbs[3] = SDL_LoadBMP("numbers/3.bmp");
    numbs[4] = SDL_LoadBMP("numbers/4.bmp");
    numbs[5] = SDL_LoadBMP("numbers/5.bmp");
    numbs[6] = SDL_LoadBMP("numbers/6.bmp");
    numbs[7] = SDL_LoadBMP("numbers/7.bmp");
    numbs[8] = SDL_LoadBMP("numbers/8.bmp");
    numbs[9] = SDL_LoadBMP("numbers/9.bmp");

    return 0;
}

int quit() {
    SDL_FreeSurface(john);

    SDL_FreeSurface(sky);
    SDL_DestroyWindow(win);

    SDL_Quit();

    return 0;
}

int ChekCanMove(int x,int y){

    if (x > 0 && y > 0 && x < SCREEN_WIDTH - john->w && y < SCREEN_HEIGHT - john->h){
        return 1;
    }
    else{
        return 0;
    }

}

void drawTimer(int time,int x,int y){
    SDL_Rect r;
    r.x = x;
    r.y = y;

    while (1){

        SDL_BlitSurface(numbs[time % 10], NULL, scr, &r);

        time /= 10;
        r.x = r.x - 25;

        if(time == 0){
            break;
        }

    }


}


int main (int argc, char ** args) {
    if (init() == 1) {
        return 1;
        
    }

    if (load() == 1) {
        return 1;
    }

    int run = 1;
    SDL_Event e;
    SDL_Rect r;

    SDL_Rect sky_r;
    sky_r.x = 0;
    sky_r.y = 0;

    SDL_Rect UI_r;
    UI_r.x = 0;
    UI_r.y = 0;

    int x = SCREEN_WIDTH/2;
    int y = 960 - john->h - 100;

    r.x = x;
    r.y = y;

    while (run) {
        while(SDL_PollEvent(&e) != NULL) {
            if (e.type == SDL_QUIT) {
                run = 0;
            }

            if (e.type == SDL_KEYDOWN) {
                if (e.key.keysym.sym == SDLK_UP) {
                    if(ChekCanMove(x,y - SHIP_SPEED)){
                        y -= SHIP_SPEED;
                    }
                }
                if (e.key.keysym.sym == SDLK_DOWN) {
                    if(ChekCanMove(x,y + SHIP_SPEED)){
                        y += SHIP_SPEED;
                    }
                }
                if (e.key.keysym.sym == SDLK_RIGHT) {
                    if(ChekCanMove(x + SHIP_SPEED,y)){
                        x += SHIP_SPEED;
                    }
                }
                if (e.key.keysym.sym == SDLK_LEFT) {
                    if(ChekCanMove(x - SHIP_SPEED,y)){
                        x -= SHIP_SPEED;
                    }
                }
            }
        }
        r.x = x;
        r.y = y;

        sky_r.x = ((SCREEN_WIDTH - r.x) - sky->w)/10;
        sky_r.y = ((SCREEN_HEIGHT - r.y) - sky->h)/10;

        // SDL_FillRect(scr, NULL, SDL_MapRGBA(scr -> format, 255, 255, 255,1));


        SDL_BlitSurface(sky, NULL, scr, &sky_r);
        
        SDL_BlitSurface(john, NULL, scr, &r);

        drawTimer(SDL_GetTicks()/1000,100,20);

        SDL_UpdateWindowSurface(win);



        if(SDL_GetTicks()/1000 == 60){

            printf("WIN!!!!!!!!");
            return quit();
        }
    }

    return quit();
}