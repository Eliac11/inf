#ifndef RATIONAL_H
#define RATIONAL_H

struct rational_t{
    int num;
    unsigned int denom;
} ;

/*
 * Возвращает рациональное число, получаемое как результат деления
 * n на d.
 */
struct rational_t rational(int n, int d);

/*
 * Возвращает числитель рационального числа r.
 */
int rat_num(struct rational_t r);

/*
 * Возвращает знаменатель рационального числа r.
 */
int rat_denom(struct rational_t r);

struct rational_t rat_sum(struct rational_t a, struct rational_t b);
struct rational_t rat_sub(struct rational_t a, struct rational_t b);
struct rational_t rat_mul(struct rational_t a, struct rational_t b);
struct rational_t rat_div(struct rational_t a, struct rational_t b);

#endif