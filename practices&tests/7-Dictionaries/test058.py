lista_pessoas = list()
mulheres = list()

continuar = True
while continuar:
    pessoa = dict()
    pessoa['nome'] = str(input("Nome: "))
    while True:
        sexo = input("Sexo: [M/F] ").lower().strip()
        if sexo == 'm' or sexo == 'f':
            pessoa['sexo'] = sexo
            if sexo == 'f':
                mulheres.append(pessoa['nome'])
            break
        else:
            print("ERRO! Insira um sexo válido! ")
    while True:
        idade = int(input("Idade: "))
        if idade > 0:
            pessoa['idade'] = idade
            break
        else:
            print("ERRO! Insira uma idade válida")
    lista_pessoas.append(pessoa)
    while True:
        opcao = input("Deseja continuar? [S/N] ").lower().strip()

        if opcao != 'n' and opcao != 's':
            print("Erro! Digite uma opção válida!!!")
        else:
            if opcao == 'n':
                continuar = False
            break

print(lista_pessoas)
soma_idades = sum(pessoa['idade'] for pessoa in lista_pessoas)
qtd_pessoas = len(lista_pessoas)
media_idade = soma_idades / qtd_pessoas

print("-=" * 30)
print(f"\nA) Quantidade de pessoas cadastradas: {qtd_pessoas}")
print(f"B) A média de idade é {media_idade}")
print(f"C) Mulheres cadastradas: {mulheres}")
print(f"D) Lista de pessoas que têm idade acima da média: ")

for pessoa in lista_pessoas:
    if pessoa['idade'] > media_idade:
        print(f"Nome: {pessoa}")
