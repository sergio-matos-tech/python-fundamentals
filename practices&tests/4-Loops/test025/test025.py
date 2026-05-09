for c in range(1, 101):
    if c % 3 == 0:
        if c % 5 == 0:
            print("FizzBuzz")
        else:
            print("Fizz")
    elif c % 5 == 0:
        if c % 3 == 0:
            print("FizzBuzz")
        else:
            print("Buzz")
    else:
        print(c)
