#define SDL_MAIN_HANDLED
#include "SDL.h"
#include "SDL_ttf.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
 

const int SCREEN_WIDTH = 1280;
const int SCREEN_HEIGHT = 960;

const int SHIP_SPEED = 20;
const int GAME_DURATION = 60;

int GLOBAL_Points = 0;

SDL_Window *win = NULL;
SDL_Surface *scr = NULL;
SDL_Renderer* renderer = NULL;

SDL_Surface *john = NULL;
SDL_Surface *sky = NULL;
SDL_Surface *gold = NULL;

SDL_Surface* numbs[10];
SDL_Surface* asteroidSurface[8];



/// ALL STRUCTIRS
struct Coordinate{
    float x;
    float y;
};
struct SpaceShip{
    struct Coordinate pos;
    int lives;
};
struct Asteroid{
    struct Coordinate pos;
    int type;
    float speed;
};
struct Coin{
    struct Coordinate pos;
    int type;
    float speed;
};
struct Result{
    int hours, minutes, seconds, day, month, year;
    int points;
};
/////

///ALL INIT STRUCTURS
struct Asteroid aster_init(int type,int x,int y,int speed){
    struct Coordinate w;
    w.x = x;
    w.y = y;
    struct Asteroid astt = {w,type,speed};
    return astt;
}
struct Coin Coin_init(int type,int x,int y,int speed){
    struct Coordinate w;
    w.x = x;
    w.y = y;
    struct Coin c = {w,type,speed};
    return c;
}
struct Result Result_init(struct tm* local,int pnt){

    struct Result r = {local->tm_hour, local->tm_min, local->tm_sec,
                        local->tm_mday, local->tm_mon + 1, local->tm_year + 1900,
                        pnt
                    };
    return r;
}
///

///
struct Asteroid ListAsteroid[100];
struct Coin ListCoin[100];

struct SpaceShip Ship;
///


void init() {

    TTF_Init();
    atexit(TTF_Quit);

    win = SDL_CreateWindow("GAME", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    scr = SDL_GetWindowSurface(win);


    for(int i = 0; i < 100; i++){
        ListAsteroid[i] = aster_init(rand()%8,rand()%SCREEN_WIDTH,-rand()%100000,1+rand()%2);
    }

    for(int i = 0; i < 100; i++){
        ListCoin[i] = Coin_init(1,rand()%SCREEN_WIDTH,-rand()%100000,1+rand()%5);
    }
}


void load() {

    john = SDL_LoadBMP("otherTexturs/ship.bmp");
    sky = SDL_LoadBMP("otherTexturs/sky.bmp");

    gold = SDL_LoadBMP("otherTexturs/gold.bmp");

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

    asteroidSurface[0] = SDL_LoadBMP("Asteroids/0.bmp");
    asteroidSurface[1] = SDL_LoadBMP("Asteroids/1.bmp");
    asteroidSurface[2] = SDL_LoadBMP("Asteroids/2.bmp");
    asteroidSurface[3] = SDL_LoadBMP("Asteroids/3.bmp");
    asteroidSurface[4] = SDL_LoadBMP("Asteroids/4.bmp");
    asteroidSurface[5] = SDL_LoadBMP("Asteroids/5.bmp");
    asteroidSurface[6] = SDL_LoadBMP("Asteroids/6.bmp");
    asteroidSurface[7] = SDL_LoadBMP("Asteroids/7.bmp");

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

int drawTimer(int time,int x,int y){
    SDL_Rect r;
    r.x = x;
    r.y = y;

    int len = 0;

    while (1){
        SDL_BlitSurface(numbs[time % 10], NULL, scr, &r);
        time /= 10;
        r.x = r.x - 25;
        len += 25;
        if(time == 0){
            break;
        }
    }
    return len;
}

void print_ttf(SDL_Surface *sDest, char* message, char* font, int size, SDL_Color color, SDL_Rect dest){
    TTF_Font *fnt = TTF_OpenFont(font, size);
    SDL_Surface *sText = TTF_RenderUTF8_Blended( fnt, message, color);

    SDL_BlitSurface(sText,NULL, sDest,&dest);
    SDL_FreeSurface(sText);

    TTF_CloseFont(fnt);
}

void drawAsteroid(struct Asteroid astr){

    SDL_Rect A_pos;
    A_pos.x = astr.pos.x;
    A_pos.y = astr.pos.y;

    A_pos.w = 50;
    A_pos.h = 10;

    SDL_BlitSurface(asteroidSurface[astr.type], NULL, scr, &A_pos);
}


void drawAsteroidALL(){
    for(int i = 0; i < 100; i++){
        drawAsteroid(ListAsteroid[i]);
    }
}

void drawCoinALL(){
    for(int i = 0; i < 100; i++){
        SDL_Rect A_pos;
        A_pos.x = ListCoin[i].pos.x;
        A_pos.y = ListCoin[i].pos.y;

        A_pos.w = 50;
        A_pos.h = 10;

        SDL_BlitSurface(gold, NULL, scr, &A_pos);
    }
}

void update(float dt){
    for(int i = 0; i < 100; i++){

        ListAsteroid[i].pos.y = ListAsteroid[i].pos.y + ListAsteroid[i].speed * dt;

        if (ListAsteroid[i].pos.y - 100 > SCREEN_HEIGHT){
            ListAsteroid[i].pos.y = -rand()%100000;
        }

        if(((int)ListAsteroid[i].pos.y) % 30 == 0){
            ListAsteroid[i].type = (ListAsteroid[i].type + 1) % 8;
        }


        float d = sqrt(powf((ListAsteroid[i].pos.y + 35)-(Ship.pos.y + john->h/2),2)+powf((ListAsteroid[i].pos.x + 35)-(Ship.pos.x + john->w/2),2));
        if (d < 50){
            Ship.lives = 0;
        }
    }

    for(int i = 0; i < 100; i++){

        ListCoin[i].pos.y = ListCoin[i].pos.y + ListCoin[i].speed * dt;

        if (ListCoin[i].pos.y - 100 > SCREEN_HEIGHT){
            ListCoin[i].pos.y = -rand()%100000;
        }

        float d = sqrt(powf((ListCoin[i].pos.y + 35)-(Ship.pos.y + john->h/2),2)+powf((ListCoin[i].pos.x + 35)-(Ship.pos.x + john->w/2),2));
        if (d < 140){
            GLOBAL_Points += 1;
            ListCoin[i].pos.y = -rand()%100000;
        }
    }
}

int FixSuccessfulTry(char * filename, struct Result st){
    FILE * fp;
    if ((fp = fopen(filename, "a")) == NULL)
    {
        perror("Error occured while opening file");
        return 1;
    }

    int n = fprintf(fp,"%d %d %d %d %d %d - %d", st.hours, st.minutes, st.seconds, st.day, st.month, st.year,st.points);
    for(int i = 0; i < 35 - n;i++){
        fprintf(fp," ");
    }
    fprintf(fp,"\n");

    fclose(fp);
    return 0;
}

void loadsResults(char * filename, struct Result *best, struct Result *last){
    FILE * fp;
    if ((fp = fopen(filename, "r")) == NULL)
    {
        perror("Error occured while opening file");
        return;
    }
    best->points = 0;
    while(!feof(fp))
    {
        fscanf(fp,"%d %d %d %d %d %d - %d", &last->hours, &last->minutes, &last->seconds, &last->day, &last->month, &last->year, &last->points);
        if(best->points <= last->points){
            best->points = last->points;
            best->hours = last->hours;
            best->minutes = last->minutes;
            best->seconds = last->seconds;
            best->day = last->day;
            best->year = last->year;
            best->month = last->month;
        }
    }

    fclose(fp);
    return;
}

void printResult(struct Result result,char text[], SDL_Rect pos, SDL_Color color){
    char str[1000];

    sprintf(str,"%s %d", text, result.points);
    print_ttf(scr, str, "beer-money12.ttf", 60, color, pos);

    pos.y = pos.y + 90;

    sprintf(str,"Был получен %d.%d.%d %d:%d:%d", result.day, result.month, result.year, result.hours, result.minutes, result.seconds);
    print_ttf(scr, str, "beer-money12.ttf", 18, color, pos);
}


void EndWinLoop(struct Result best,struct Result last){
    SDL_Event e;
    while (1) {
            while(SDL_PollEvent(&e) != NULL) {
                if (e.type == SDL_QUIT) {
                    quit();
                }
            }
            SDL_Rect sky_r = {0,0,0,0};
            SDL_BlitSurface(sky, NULL, scr, &sky_r);
            
            SDL_Rect UI_r = {SCREEN_WIDTH/2-200,SCREEN_HEIGHT/2-400,0,0};

            char str[1000];
            SDL_Color clrGold = {253,229,33,0};
            sprintf(str,"Количество очков: %d", GLOBAL_Points);
            print_ttf(scr, str, "beer-money12.ttf", 72, clrGold, UI_r);

            UI_r.y = UI_r.y + 300;
            SDL_Color clrGreen = {83,250,0,0};
            printResult(best,"Лучший результат:", UI_r,clrGreen);

            UI_r.y = UI_r.y + 200;
            SDL_Color clrWhite = {255,250,255,0};
            printResult(last,"Прошлой игры:", UI_r, clrWhite);

            SDL_UpdateWindowSurface(win);
    }
}

void EndWinLoopGameover(){
    SDL_Event e;
    while (1) {
            while(SDL_PollEvent(&e) != NULL) {
                if (e.type == SDL_QUIT) {
                    quit();
                }
            }
            SDL_FillRect(scr, NULL, SDL_MapRGBA(scr -> format, 0, 0, 0, 1));
            
            SDL_Rect UI_r = {SCREEN_WIDTH/2-300,SCREEN_HEIGHT/2,0,0};

            char str[1000];
            SDL_Color clrRed = {253,0,0,0};
            print_ttf(scr, "------GAME OVER-------", "beer-money12.ttf", 72, clrRed, UI_r);

            SDL_UpdateWindowSurface(win);
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
    Ship.lives = 100;


    struct Result bestResult = {0,0,0,0,0,0,0};
    struct Result lastResult = {0,0,0,0,0,0,0};
    loadsResults("userdata.txt",&bestResult,&lastResult);

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

        ///
        update(0.2);
        ///

        SDL_BlitSurface(sky, NULL, scr, &sky_r);

        SDL_Rect S_pos;
        S_pos.x = Ship.pos.x;
        S_pos.y = Ship.pos.y;
        SDL_BlitSurface(john, NULL, scr, &S_pos);

        drawAsteroidALL();
        drawCoinALL();

        SDL_Rect UI_r = {SCREEN_WIDTH-300,20,125,50};
        SDL_FillRect(scr, &UI_r, SDL_MapRGBA(scr -> format, 200, 200, 200,1));
        drawTimer(GLOBAL_Points,SCREEN_WIDTH-200,20);

        SDL_Rect UI2_r = {50,20,125,50};
        SDL_FillRect(scr, &UI2_r, SDL_MapRGBA(scr -> format, 255, 255, 255,1));
        drawTimer(SDL_GetTicks()/1000,100,20);

        SDL_Color clr = {255,250,240,0};
        SDL_Rect UI3_r = {180,20,0,0};
        print_ttf(scr, "Время", "beer-money12.ttf", 60, clr, UI3_r);

        if(SDL_GetTicks()/1000 == GAME_DURATION){

            printf("WIN!!!!!!!!");

            time_t now;
            time(&now);
            struct tm *local = localtime(&now);
            struct Result res = Result_init(local,GLOBAL_Points);
            FixSuccessfulTry("userdata.txt",res);
            loadsResults("userdata.txt",&bestResult,&lastResult);

            EndWinLoop(bestResult,lastResult);

            return quit();
        }

        if (Ship.lives <= 0){
            EndWinLoopGameover();
        }


        /// 
        //DEBUG_DRAW();
        ///
        //////////////////
        SDL_UpdateWindowSurface(win);
    }

    return quit();
}







void DEBUG_DRAW(){
    SDL_Rect debug_r;
        debug_r.x = (Ship.pos.x + john->w/2);
        debug_r.y = (Ship.pos.y + john->h/2);
        debug_r.w = 4;
        debug_r.h = 4;
        SDL_FillRect(scr, &debug_r, SDL_MapRGBA(scr -> format, 255, 0, 0,1));

        for(int i = 0; i < 100; i++){
            debug_r.x = (ListAsteroid[i].pos.x + 35);
            debug_r.y = (ListAsteroid[i].pos.y + 35);
            debug_r.w = 4;
            debug_r.h = 4;
            SDL_FillRect(scr, &debug_r, SDL_MapRGBA(scr -> format, 255, 0, 0,1));
        }
}