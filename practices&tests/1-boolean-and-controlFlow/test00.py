from random import randint
from sympy import isprime



def is_even(n):
    if n % 2 == 0:
        return True
    return False




computerChoice = randint(1, 50)
print(f"Generated number: {computerChoice}")

if isprime(computerChoice):
    print(f"{computerChoice} is a prime number!")

else:
    print(f"{computerChoice} is NOT prime!")

if is_even(computerChoice):
    print(f"{computerChoice} is even!")
else:
    print(f"{computerChoice} is odd!")

