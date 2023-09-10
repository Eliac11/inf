#include <stdio.h>
#include <string.h>

#include "rational.h"
// #include "rational.c"
void printrat(struct rational_t ch){

    if (rat_denom(ch) == 1){
        printf("%d",rat_num(ch));
    }
    else{
        printf("%d/%d",rat_num(ch),rat_denom(ch));
    }

}