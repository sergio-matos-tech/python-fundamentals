def progressao_aritimetica(primeiro_termo, razao, qtd_termos):
    cont = 0
    termo = primeiro_termo
    while True:
        termo += razao
        print(f"{termo}", end=' -> ')
        cont += 1
        if cont == qtd_termos:
            print(" Pausa")
            break
    return termo


print("Gerador de P.A")

primeiro_termo = int(input("Primeiro Termo: "))
razao = int(input("Razão da P.A: "))
ultimo_termo = progressao_aritimetica(primeiro_termo, razao, 10)

while True:
    qtd_termos_mais = int(input("Quantos termos deseja mostrar a mais? "))
    if qtd_termos_mais == 0:
        break
    ultimo_termo = progressao_aritimetica(ultimo_termo, razao, qtd_termos_mais)

print("Programa Finalizado")
