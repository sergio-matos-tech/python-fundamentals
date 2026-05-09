dados_trabalhador = dict()

dados_trabalhador['nome'] = str(input("Nome: "))
dados_trabalhador['ano_nascimento'] = int(input("Ano de nascimento: "))
dados_trabalhador['carteira_de_trabalho'] = str(input("Nº carteira de trabalho: (0 para não tem) "))

if dados_trabalhador['carteira_de_trabalho'] != '0':
    dados_trabalhador['ano_contratacao'] = int(input("Ano de Contratação: "))
    dados_trabalhador['salario'] = float(input("Salário R$"))
    dados_trabalhador['ano_de_aposentadoria'] = dados_trabalhador['ano_contratacao'] + 30

print('-=-' * 30)

for k, v in dados_trabalhador.items():
    print(f"  - {k} = {v}")
