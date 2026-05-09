aluno = dict()

aluno['nome'] = str(input("Informe o nome do aluno: "))
aluno['media'] = float(input(f"Informe a média do aluno {aluno['nome']}: "))
aluno['situacao'] = 'aprovado' if aluno['media'] >= 7 else 'reprovado' if aluno['media'] < 6 else 'recuperação'

print('-=' * 50)

for k, v in aluno.items():
    print(f"  - {k} = {v}")
