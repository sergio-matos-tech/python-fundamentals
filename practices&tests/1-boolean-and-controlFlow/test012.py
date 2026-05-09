import random

alunos = list()

c = 0
for c in range(0, 3):
    aluno = str(input(f"Digite o nome do {c + 1}º aluno: "))
    alunos.append(aluno)

alunos_escolhidos = random.sample(alunos, 3)

print(f"A ordem dos Alunos escolhidos foi {alunos_escolhidos}")
