import math

while True:
    try:
        number = int(input("Enter an integer number: "))
        if isinstance(number, int):
            break
        else:
            print("Please enter an integer number. ")
    except ValueError:
        print("Invalid input: Please enter an integer number. ")

print(f"The double of {number} is {number * 2}\nThe triple of {number} is {number * 3}\n"
      f"The square root of {number} is {math.sqrt(number)}")
