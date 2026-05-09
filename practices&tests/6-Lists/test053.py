import random
import time

print("-" * 40)
print("JOGO DA MEGA SENA".center(40))
print("-" * 40)

qtd_jogos = int(input("Quantos jogos deseja sortear? "))
jogo_sorteado = list()
jogos_sorteados = list()

print(f"\n===== SORTEANDO {qtd_jogos} JOGOS =====".center(40))
for c in range(0, qtd_jogos):
    for k in range(0, 6):
        num_sorteado = random.randint(1, 61)
        if num_sorteado not in jogo_sorteado:
            jogo_sorteado.append(num_sorteado)
    print(f"Jogo {c + 1}: {jogo_sorteado}")
    time.sleep(0.5)
    jogos_sorteados.append(jogo_sorteado[:])
    jogo_sorteado.clear()

print(f"Lista de todos os jogos sorteados: {jogos_sorteados}")
