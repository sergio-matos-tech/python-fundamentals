import numpy as np

notas = np.array([
    [8.5, 7.0, 9.2, 6.5],  # Aluno 1
    [5.5, 6.8, 7.5, 8.0],  # Aluno 2
    [9.5, 9.0, 8.8, 10.0]  # Aluno 3
])

print("Matriz de Notas:\n")
print(notas)
print(type(notas))

print(f"\nMédia geral da turma:    {notas.mean():.2f}")
print(f"Nota máxima da turma:    {notas.max()}")
print(f"Nota mínima da turma:    {notas.min()}")
print(f"Soma de todas as notas:  {notas.sum()}\n")

media_por_aluno = notas.mean(axis = 1).round(2)
print(f"Média de cada aluno: {media_por_aluno}\n")

media_por_prova = notas.mean(axis = 0).round(2)
print(f"Média de cada prova: {media_por_prova}")