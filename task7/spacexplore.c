#define SDL_MAIN_HANDLED
#include "SDL.h"
#include "SDL_TTF.h"
#include <stdio.h>
 
const int SCREEN_WIDTH = 1280;
const int SCREEN_HEIGHT = 960;

const int SHIP_SPEED = 20;

SDL_Window *win = NULL;
SDL_Surface *scr = NULL;
SDL_Surface *john = NULL;
SDL_Surface *sky = NULL;



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

    SDL_SetSurfaceAlphaMod(sky, 1);

    if (john == NULL) {
        // std::cout << "Can't load image: " << SDL_GetError() << std::endl;
        system("pause");
        return 1;
    }

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

void DrawTimer(int seconds){

TTF_Font* Sans = TTF_OpenFont("Sans.ttf", 24);
SDL_Color White = {255, 255, 255};

SDL_Surface* surfaceMessage = TTF_RenderText_Solid(Sans, "put your text here", White); 

SDL_Texture* Message = SDL_CreateTextureFromSurface(scr, surfaceMessage);

SDL_Rect Message_rect; 
Message_rect.x = 0;   
Message_rect.y = 0; 
Message_rect.w = 100; 
Message_rect.h = 100; 

SDL_RenderCopy(scr, Message, NULL, &Message_rect);
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
        
        // SDL_BlitSurface(john, NULL, scr, &r);

        DrawTimer(1212);

        SDL_UpdateWindowSurface(win);
    }

    return quit();
}