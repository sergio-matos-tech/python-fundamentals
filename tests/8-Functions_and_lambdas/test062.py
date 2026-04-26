from time import sleep


def contagem(inicio, fim, passo):
    """
    -> A função realiza uma contagem e mostra na tela
    :param inicio: início da contagem
    :param fim: valor do fim da contagem
    :param passo: valor do passo da contagem
    :return: não tem retorno
    """
    print("-=" * 40)
    print(f"Contagem de {inicio} até {fim} de {passo} em {passo}")
    if inicio < fim:
        for c in range(inicio, fim + 1, passo):
            print(c, end=' ->  ')
            sleep(0.3)
        print("FIM!")
    else:
        for c in range(inicio, fim - 1, -passo):
            print(c, end=' -> ')
            sleep(0.3)
        print("FIM!")


contagem(1, 10, 1)
contagem(10, 0, 2)
print("==" * 40)
print("Agora é sua vez de personalizar a contagem!")
inicio = int(input("Início: "))
fim = int(input("Fim: "))
passo = int(input("Passo: "))
contagem(inicio, fim, passo)

help(contagem)
