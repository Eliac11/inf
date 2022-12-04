
#include <stdio.h>
struct rational_t{
    int num;
    unsigned int denom;
};

struct rational_t rational(int n, int d){
    int a,b;
    a = n;
    b = d;
    // printf("%d %d\n",n,d);
    while(a != 0 && b != 0){
        
        if(a > b){
            a = a % b;
        }
        else{
            b = b % a;
        }
        // printf("%d %d\n",a,b);
    }
    n /= (a+b);
    d /= (a+b);
    // printf("-----%d %d\n",n,d);
    struct rational_t r = {n,d};
    return r;
}


long rat_num(struct rational_t r){
    return r.num;
}

long rat_denom(struct rational_t r){
    return r.denom;
}

struct rational_t rat_sum(struct rational_t a, struct rational_t b) {
    // printf("%d %d %d %d\n",a.num,a.denom,b.num,a.denom);
    return rational(rat_num(a) * rat_denom(b) + rat_num(b) * rat_denom(a),
                    rat_denom(a) * rat_denom(b));
}

struct rational_t rat_sub(struct rational_t a, struct rational_t b) {
    return rational(rat_num(a) * rat_denom(b) - rat_num(b) * rat_denom(a),
                    rat_denom(a) * rat_denom(b));
}

struct rational_t rat_mul(struct rational_t a, struct rational_t b) {
    return rational(rat_num(a) * rat_num(b),
                    rat_denom(a) * rat_denom(b));
}

struct rational_t rat_div(struct rational_t a, struct rational_t b) {
    return rational(rat_num(a) * rat_denom(b), 
                    rat_num(b) * rat_denom(a));
}