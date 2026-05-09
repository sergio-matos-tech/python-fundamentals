import random

numeros = list()

for c in range(0, 4):
    num = int(input(f"Digite o {c + 1}º número: "))
    numeros.append(num)

print(f"Você digitou os valores {numeros}")
valor_gerado = random.randint(0, 4)
valor_gerado2 = random.randint(0, 4)

print(f"O valor {valor_gerado} apareceu {numeros.count(valor_gerado)} vezes")
