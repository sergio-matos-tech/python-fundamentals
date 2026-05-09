two_digit_number = ''

while len(two_digit_number) != 2:
    two_digit_number = input("Write a two digit number: ")

num1 = int(two_digit_number[0])
num2 = int(two_digit_number[1])

print(f"{num1} + {num2} is {num1 + num2}")
