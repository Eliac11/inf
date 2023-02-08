
#include "test.h"

void calculate_primes(int primes[], int n){

    primes[0] = 0;
    primes[1] = 0;
    int k = 0;
    for (int i=2;i<n;i++){
        for (int j=2;j<i;j++){
            if(i%j==0){
              k++;
            }
        }
        if(k == 0){
            primes[i] = 1;
        }
        else{
            primes[i] = 0;
            k = 0;
        }
    }
}

