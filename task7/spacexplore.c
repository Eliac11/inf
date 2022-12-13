#define SDL_MAIN_HANDLED
#include "SDL.h"


#include <stdio.h>
#include <stdlib.h>
#include <math.h>
 
const int SCREEN_WIDTH = 1280;
const int SCREEN_HEIGHT = 960;

const int SHIP_SPEED = 20;

SDL_Window *win = NULL;
SDL_Surface *scr = NULL;
SDL_Renderer* renderer = NULL;

SDL_Surface *john = NULL;
SDL_Surface *sky = NULL;

SDL_Surface* numbs[10];
SDL_Surface *asteroidSurface;

struct SpaceShip{
    SDL_Rect pos;
    int lives;
};

struct SpaceShip Ship;

struct Asteroid{
    SDL_Rect pos;
    int type;
    int speed;
};


struct Asteroid aster_init(int type,int x,int y,int speed){
    SDL_Rect w;
    w.x = x;
    w.y = y;
    struct Asteroid astt = {w,type,speed};
    return astt;
}

struct Asteroid ListAsteroid[100];

void init() {
    win = SDL_CreateWindow("GAME", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    scr = SDL_GetWindowSurface(win);


    for(int i = 0; i < 100; i++){
        ListAsteroid[i] = aster_init(rand()%16,rand()%SCREEN_WIDTH,-rand()%100000,1+rand()%2);
    }
}

void load() {

    john = SDL_LoadBMP("ship.bmp");
    sky = SDL_LoadBMP("sky.bmp");

    asteroidSurface = SDL_LoadBMP("Asteroids.bmp");

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

void drawAsteroid(struct Asteroid astr){
    SDL_Rect A_obr;
    A_obr.x = 100 * astr.type;
    A_obr.y = 0;
    A_obr.w = 100;
    A_obr.h = 100;

    SDL_BlitSurface(asteroidSurface, &A_obr, scr, &(astr.pos));
}


void drawAsteroidALL(){
    for(int i = 0; i < 100; i++){
        drawAsteroid(ListAsteroid[i]);
    }
}

void update(int dt){
    for(int i = 0; i < 100; i++){

        ListAsteroid[i].pos.y = ListAsteroid[i].pos.y + ListAsteroid[i].speed * dt;

        if (ListAsteroid[i].pos.y - 100 > SCREEN_HEIGHT){
            ListAsteroid[i].pos.y = -rand()%100000;
        }

        // for(int j = 0; j < 100; j++){
        //     if(i == j){continue;}

        //     float d = sqrt(powf(ListAsteroid[i].pos.y-ListAsteroid[j].pos.y)+powf(ListAsteroid[i].pos.x-ListAsteroid[j].pos.x))

        //     if ()
        // }
    }
}


int main (int argc, char ** args) {

    init();
    load();

    int run = 1;
    SDL_Event e;

    SDL_Rect r;
    SDL_Rect sky_r;

    Ship.pos.x = SCREEN_WIDTH/2;
    Ship.pos.y = 960 - john->h - 100;


    while (run) {
        while(SDL_PollEvent(&e) != NULL) {
            if (e.type == SDL_QUIT) {
                run = 0;
            }

            if (e.type == SDL_KEYDOWN) {
                if (e.key.keysym.sym == SDLK_UP) {
                    if(ChekCanMove(Ship.pos.x ,Ship.pos.y - SHIP_SPEED)){
                        Ship.pos.y -= SHIP_SPEED;
                    }
                }
                if (e.key.keysym.sym == SDLK_DOWN) {
                    if(ChekCanMove(Ship.pos.x ,Ship.pos.y + SHIP_SPEED)){
                        Ship.pos.y += SHIP_SPEED;
                    }
                }
                if (e.key.keysym.sym == SDLK_RIGHT) {
                    if(ChekCanMove(Ship.pos.x + SHIP_SPEED,Ship.pos.y)){
                        Ship.pos.x += SHIP_SPEED;
                    }
                }
                if (e.key.keysym.sym == SDLK_LEFT) {
                    if(ChekCanMove(Ship.pos.x - SHIP_SPEED,Ship.pos.y)){
                        Ship.pos.x -= SHIP_SPEED;
                    }
                }
            }
        }

        sky_r.x = ((SCREEN_WIDTH - Ship.pos.x) - sky->w)/10;
        sky_r.y = ((SCREEN_HEIGHT - Ship.pos.y) - sky->h)/10;

        update(1);

        // SDL_FillRect(scr, NULL, SDL_MapRGBA(scr -> format, 255, 255, 255,1));


        SDL_BlitSurface(sky, NULL, scr, &sky_r);
        
        SDL_BlitSurface(john, NULL, scr, &(Ship.pos));

        drawAsteroidALL();



        drawTimer(SDL_GetTicks()/1000,100,20);
        if(SDL_GetTicks()/1000 == 60){

            printf("WIN!!!!!!!!");
            return quit();
        }
        
        //////////////////
        SDL_UpdateWindowSurface(win);
    }

    return quit();
}