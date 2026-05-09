people = []
data = list()

go_on = True
c = 0

weighted = 0
lightest = 0

while go_on:
    name = str(input("Name: ")).strip()
    weight = float(input("Weight (kg): "))
    if c == 0:
        weighted = weight
        lightest = weight
    else:
        if weight > weighted:
            weighted = weight
        elif weight < lightest:
            lightest = weight

    data.append(name)
    data.append(weight)
    people.append(data[:])
    data.clear()
    c += 1

    conti = input("Do you want to go on? [Y/N]: ").lower().strip()
    if conti == 'n':
        go_on = False

print("-=" * 50)
print(f"You have inserted {c} people ")
print(f"The weighted was {weighted}.", end='')

for p in people:
    if p[1] == weighted:
        print(f" {p[0]}")

print(f"The lightest was {lightest}.", end='')
for p in people:
    if p[1] == lightest:
        print(f"{p[0]}")
