import sys

print("\n***** PYTHON PIZZA DELIVERY *****\n")
bill = 0

size_pizza = str(input("Enter the size of the pizza: (S) Small | (M) Medium | (L) Large: "))
if size_pizza == 'S':
    bill = 15
elif size_pizza == 'M':
    bill = 20
elif size_pizza == 'L':
    bill = 25
else:
    print("Error! Enter a valid character.")
    sys.exit()

add_pepperoni = str(input("Would you like to add pepperoni? (Y) Yes | (N) No: "))
if add_pepperoni == 'Y' and size_pizza == 'S':
    bill += 2
elif add_pepperoni == 'Y' and (size_pizza == 'M' or size_pizza == 'L'):
    bill += 3
elif add_pepperoni == 'N':
    bill += 0
else:
    print("Error! Enter a valid character.")
    sys.exit()

add_extra_cheese = str(input("Would you like to add extra cheese? (Y) Yes | (N) No: "))
if add_extra_cheese == 'Y':
    bill += 1
elif add_extra_cheese == 'N':
    bill += 0
else:
    print("Error! Enter a valid character.")
    sys.exit()

print(f"Your final bill is ${bill}")
