def menu(num1, num2):
    option = 0
    while option not in {1, 2, 3, 4, 5}:
        print("[ 1 ] To sum")
        print("[ 2 ] To multiply")
        print("[ 3 ] To check the max number")
        print("[ 4 ] To check the min number")
        print("[ 5 ] Exit")
        option = int(input("<<<< Choose your option >>>> "))
        if option == 5:
            break
        elif option == 1:
            return num1 + num2
        elif option == 2:
            return num1 * num2
        elif option == 3:
            return max(num1, num2)
        elif option == 4:
            return min(num1, num2)


def main():
    number1 = int(input("Enter the first number: "))
    number2 = int(input("Enter the second number: "))

    result = menu(number1, number2)
    if result is not None:
        print(f"Result: {result}")
    else:
        print("Exited the menu.")


if __name__ == "__main__":
    main()
