import random


def generate_evens():
    evens = list()
    for c in range(0, 50, 2):
        evens.append(c)
    return evens


def square_number(n):
    return n ** 2


def yell(word):
    """
    function that takes a string and return its uppercase
    :param word:
    :return the word in upper case:
    """
    if isinstance(word, str):
        return word.upper()


def exponent(num, power=1):
    return num ** power


even_list = generate_evens()
print(even_list)
print(square_number(random.randint(1, 10)))
print(yell("hill"))
print(exponent(2, 10))
print(exponent(2))

var = yell.__doc__
print(var)


def return_day(num):
    if num < 1 or num > 7:
        return None
    else:
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        return days[num - 1]


print(return_day(2))
print(return_day(0))
