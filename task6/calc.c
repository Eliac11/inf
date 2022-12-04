/**
 * main.c -- программа "Hello, students!"
 *
 * Copyright (c) 2022, Posti Ilya <posti.ilya@mail.ru>
 *
 * This code is licensed under MIT license.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


#include "rational.h"
#include "rat_io.h"

struct rational_t strtorat(char val[],struct rational_t last){

    if (strstr(val,"last") != NULL){
        // printf(" ch ----- \n");
        return last;
    }
    else if(strstr(val,"/") != NULL){
        int n,d;
        sscanf(val,"%d/%d",&n,&d);
        // printf(" ch %s  %d %d\n",val,n,d);
        return rational(n,d);
    }
    else{
        return rational(atoi(val),1);
    }
}

int main()
{
    struct rational_t last = rational(10,100);

    char value1[1024],value2[1024],value3[1024];
    
    printf(":\n");

    while(1){

        scanf("%s %s %s",&value1,&value2,&value3);
        
        struct rational_t a = strtorat(value1, last);
        struct rational_t b = strtorat(value3, last);

        struct rational_t ch = rat_sum(a,b);

        if (value2[0] == '+'){
            struct rational_t ch = rat_sum(a,b);
        }
        else if (value2[0] ==  '-'){
            struct rational_t ch = rat_sub(a,b);
        }
        else if (value2[0] == '*'){
            struct rational_t ch = rat_mul(a,b);
        }
        else if (value2[0] == '/'){
            struct rational_t ch = rat_div(a,b);
        }
            
        
        last.num = rat_num(ch);
        last.denom = rat_denom(ch);

        printf("=  ");
        printrat(last);
        printf("\n");
    }

    return 0;
}