from ctypes import *

cal = CDLL('./libtest.so')
m = [0]*int(input("Input N: "))

c_m = (c_int * len(m))(*m)
cal.calculate_primes(c_m, len(m))

for i,r in enumerate(c_m):
    if r:
        print(i)
