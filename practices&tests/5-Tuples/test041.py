import random

valores_sorteados = (random.randint(1, 10), random.randint(1, 10), random.randint(1, 10),
                     random.randint(1, 10), random.randint(1, 10), random.randint(1, 10))

print("Valores sorteados")
for valor in valores_sorteados:
    print(valor, end=' ')

print(f"\nMaior valor: {max(valores_sorteados)}")
print(f"Menor valor: {min(valores_sorteados)}")
