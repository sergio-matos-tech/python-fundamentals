max_num = 0
min_num = 0

num = int(input("Enter an integer: "))
max_num = num
min_num = num
soma = num
cont = 1

while True:
    option = input("Do you want to go on? [Y/N] ").lower().strip()
    if option == 'n':
        break

    num = int(input("Enter an integer: "))
    soma += num
    cont += 1
    if num > max_num:
        max_num = num
    if num < min_num:
        min_num = num

print(f"Maior valor: {max_num}")
print(f"Menor valor: {min_num}")
print(f"Media: {soma / cont}")
