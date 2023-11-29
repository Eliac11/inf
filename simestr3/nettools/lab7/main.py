def factorial(n):
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел.")
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)

def is_palindrome(s):
    s = s.replace(" ", "").lower()
    return s == s[::-1]