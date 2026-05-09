snacks = ('Hamburger', 'Juice', 'Pizza')
# Tuplas são imutáveis
# snacks[1] = Soda -> Dará erro!!!

print(snacks[-1])
print(snacks[-3:])
print(snacks)

for snack in snacks:
    print(f"I'm gonna eat {snack}")

for index, snack in enumerate(snacks):
    print(f"I'm gonna eat {snack} of index {index}")
