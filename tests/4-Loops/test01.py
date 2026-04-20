from sympy import *


initial_value = int(input())
end_value = int(input())


for c in range(initial_value, end_value + 1):
    if isprime(c):
        print(f'{c} is prime')
    elif c % 2 == 0:
        print(f'{c} is even')
    else:
        print(f'{c} is odd')
        
