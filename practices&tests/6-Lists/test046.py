integers = list()

for c in range(0, 5):
    integer = int(input("Enter an integer: "))

    # if the list is empty or if the integer is already greater than the greatest
    if not integers or integer > integers[-1]:
        integers.append(integer)
        print(f"{integer} inserted in the head of the list...")
    else:
        index = 0
        lenght = len(integers)

        while index < lenght:
            if integer <= integers[index]:
                integers.insert(index, integer)
                print(f"{integer} inserted in index {index} of the list...")
                break
            index += 1

print(f"The sorted integers entered is {integers}")
