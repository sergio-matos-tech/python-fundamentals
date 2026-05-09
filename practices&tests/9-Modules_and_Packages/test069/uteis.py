def factorial(n):
    if n == 1 or n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def sum_int(n1, n2):
    return int(n1) + int(n2)
