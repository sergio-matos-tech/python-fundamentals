jogador = dict()
gols = list()

jogador['nome'] = str(input("Nome do Jogador: "))
qtd_partidas = int(input(f"Quantas partidas o {jogador['nome']} jogou? "))

for c in range(qtd_partidas):
    qtd_gols = int(input(f"Quantos gols ele fez na {c + 1}ª partida? "))
    gols.append(qtd_gols)
jogador['gols'] = gols[:]
jogador['total'] = sum(gols)

print("+=+=" * 20)
print(jogador)
print("+=+=" * 20)
for k, v in jogador.items():
    print(f"O campo {k} tem o valor {v}")

print("+=+=" * 20)
print(f"O jogador {jogador['nome']} fez {qtd_partidas} partidas")
cont = 1
for gol in gols:
    print(f"Na {cont}ª partida, fez {gol}")
    cont += 1

print(f"Total de gols: {jogador['total']}")
