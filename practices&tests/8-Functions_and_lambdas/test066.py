def jogador(nome_jogador, num_gols):
    if nome_jogador.strip() == "":
        nome_jogador = "<desconhecido>"
    if num_gols == "":
        num_gols = 0
    else:
        num_gols = int(num_gols)
    return f"O jogador {nome_jogador} fez {num_gols} gol(s) no campeonato"


nome_jogador = input("Nome do jogador: ")
qtd_gols = input("Quantidade de gols: ")

print(jogador(nome_jogador, qtd_gols))
