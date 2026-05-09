

age = int(input("Enter your age: "))

if 21 > age >= 18:
    print("Wristband")
elif age >= 21:
    print("Normal entry")
else:
    print("Too young")