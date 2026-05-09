def factorial_recursive(num):
    if num == 0 or num == 1:
        return 1
    else:
        return num * factorial_recursive(num - 1)


def factorial_loop(num):
    c = num
    factorial = 1
    while c > 0:
        factorial *= c
        c -= 1
    return factorial


def main():
    number = int(input("Enter an integer >= 0: "))
    if number >= 0:
        print(f"{factorial_recursive(number)}")
        print(f"{factorial_loop(number)}")


if __name__ == "__main__":
    main()
