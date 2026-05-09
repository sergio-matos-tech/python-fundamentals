inteiros = list()
pares = list()
impares = list()

contador = 0
continuar = True
while continuar:
    inteiro = int(input("Digite um número inteiro: "))
    inteiros.append(inteiro)
    opcao = input("Deseja continuar? [S/N] ").lower().strip()
    if opcao == 'n':
        continuar = False
        
    contador += 1
    if inteiro % 2 == 0:
        pares.append(inteiro)
    else:
        impares.append(inteiro)

inteiros.sort(reverse=True)
print(f"Você digitou {contador} elementos")
print(f"Os valores em ordem decrescente é {inteiros}")
print(f"A lista de pares é {pares}")
print(f"A lista de ímpares é {impares}")
