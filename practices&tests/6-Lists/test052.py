matrix = [[0 for _ in range(3)] for _ in range(3)]

sum_even = 0
sum_third_column = 0
highest_second_row = 0

for row in range(3):
    for column in range(3):
        num = int(input(f"Enter an integer for [{row}][{column}]: "))
        matrix[row][column] = num
        if num % 2 == 0:
            sum_even += num
        if column == 2:
            sum_third_column += num
        if row == 1:
            if num > highest_second_row:
                highest_second_row = num

print("#" * 50)
for row in range(3):
    for column in range(3):
        print(f"[ {matrix[row][column]:^5} ] ", end='')
        if row == 0 or row == 1 or row == 2:
            print("", end='    ')
    print()

print("#" * 50)
print(f"Sum of even numbers: {sum_even}")
print(f"Sum of the third column: {sum_third_column}")
print(f"Highest integer of second row: {highest_second_row}")
