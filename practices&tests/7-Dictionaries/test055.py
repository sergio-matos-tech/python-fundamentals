import random
import time

valores_sorteados = dict()

print("==== Valores Sorteados ====\n".center(40))
for c in range(4):
    time.sleep(0.3)
    valores_sorteados[f'jogador{c + 1}'] = random.randint(1, 6)

for k, v in valores_sorteados.items():
    print(f"O [{k}] obteve o valor [{v}]")

print()
print("¨¨" * 40)
print("== RANKING DOS JOGADORES ==".center(30))

sorted_valores_sorteados = sorted(valores_sorteados.items(), key=lambda item: item[1], reverse=True)
cont = 1
for k, v in sorted_valores_sorteados:
    time.sleep(0.3)
    print(f"{cont}º lugar: {k} com o valor {v}".center(30))
    cont += 1
