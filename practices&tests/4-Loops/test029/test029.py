num = int(input("Digite um número maior que 0: "))

qtd_divisoes = 2  # começa em 2, pois um número inteiro sempre será divisível por 1 e por ele mesmo
if num > 0:
    for c in range(2, num):
        if num % c == 0:
            qtd_divisoes += 1
        # if qtd_divisoes > 2:  # linha para otimizar o código quando já houver mais que 2 divisões
        # poderia ser utilizado caso não mostrasse para o usuário a quantidade de múltiplos
if qtd_divisoes > 2:
    print(f"{num} é divisível por {qtd_divisoes} números. Logo, ele NÃO É PRIMO")
elif qtd_divisoes == 2:
    print(f"{num} é divisível por apenas 2 números. Logo, ele É PRIMO")
