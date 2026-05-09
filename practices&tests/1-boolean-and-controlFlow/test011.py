number = float(input("Enter a number: "))

part_int = int(number)
part_float = number - part_int

print(f"{number} is {part_int} + {part_float:.3f}")
