values = list()

for c in range(0, 5):
    value = int(input(f"Enter an integer for the index {c}: "))
    values.append(value)

print(f"\nYou've entered {values}")
print(f"The max integer was {max(values)} in index {values.index(max(values))}")
print(f"The min integer was {min(values)} in index {values.index(min(values))}")
