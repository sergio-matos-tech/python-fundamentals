soma = 0
while True:
    num = int(input("Digite um número [999 para parar]: "))
    if num != 999:
        soma += num
    else:
        break

print(f"A soma foi {soma}")
