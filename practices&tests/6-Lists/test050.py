numbers = list()
even_list = list()
odd_list = list()

for c in range(0, 5):
    num = int(input("Enter an integer number: "))

    if num % 2 == 0:
        even_list.append(num)
    else:
        odd_list.append(num)

even_list.sort()
odd_list.sort()

numbers.append(even_list[:])
numbers.append(odd_list[:])

print("*" * 50)
print(f"List of numbers: {numbers}")
print(f"List of even numbers: {even_list}")
print(f"List of odd numbers: {odd_list}")
