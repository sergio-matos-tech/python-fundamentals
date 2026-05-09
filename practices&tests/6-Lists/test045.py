values = list()

go_on = True
while go_on:
    value = int(input("Enter an integer: "))
    if value not in values:
        values.append(value)
    else:
        print(f"There is already the {value} number in this list! I can't insert it")

    opcao = input("Do you want to go on? [Y/N] ").lower()
    if opcao != 'y':
        go_on = False

values.sort()
print(f"Values entered: {values}")
