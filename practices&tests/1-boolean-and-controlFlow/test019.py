numbers = list()

highest = 0
minimum = 0
c = 0
while True:
    try:
        num = int(input(f"Enter the {c + 1}º integer number: "))
        if isinstance(num, int):
            if c == 0:
                highest = num
                minimum = num
            c += 1
            numbers.append(num)
            if num > highest:
                highest = num
            if num < minimum:
                minimum = num
        stop = str(input("Type 'S' to stop and 'C' to continue: ")).lower()
        if stop == 's':
            break
    except ValueError:
        print("ERROR. Type a correct number")

print("You enter the following numbers")
print(numbers)
print(f"And the highest value is {highest} and the minimum value is {minimum}")
