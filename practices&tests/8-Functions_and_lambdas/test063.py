import random
from time import sleep


def number_analysis(list_numbers):
    lenght_list = len(list_numbers)
    print(f"{lenght_list} numbers passed on the function")
    even_numbers = list()
    odd_numbers = list()
    sum_of_even = 0
    if lenght_list > 0:
        print("=-" * 30)
        print("Numbers generated")
        for number in list_numbers:
            print(f"{number}", end=' -> ')
            sleep(0.3)
            if number % 2 == 0:
                even_numbers.append(number)
                sum_of_even += number
            else:
                odd_numbers.append(number)
        print('END!\n')
    print(f"The maximum integer was {max(list_numbers)}")
    print(f"The sum of all the numbers is {sum(list_numbers)}")
    print(f"Even numbers: {even_numbers}")
    print(f"Odd numbers: {odd_numbers}")
    print(f"Sum of even numbers: {sum_of_even}")


random_amount_of_numbers = random.randint(0, 10)
random_list_of_numbers = list()

for c in range(0, random_amount_of_numbers):
    number_generated = random_number = random.randint(0, 100)
    random_list_of_numbers.append(number_generated)

number_analysis(random_list_of_numbers)
