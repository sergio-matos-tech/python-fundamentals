while True:
    try:
        integer = int(input("Enter a integer number: "))
    except ValueError:
        print(f"Try again.")
    else:
        print(f"You've entered {integer}")
        break
