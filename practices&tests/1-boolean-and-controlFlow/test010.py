number = int(input("Enter a number for me to show its the multiplication table: "))

c = 0
print("=============")
for c in range(1, 11):
    print(f"{number} X {c} = {number * c}")
print("=============")
