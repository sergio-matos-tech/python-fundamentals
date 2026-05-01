import numpy as np

matriz = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print(type(matriz))
print(matriz.shape)

vetor = np.array([10, 20, 30])
print(type(vetor))
print(vetor.shape)

resultado = matriz + vetor

print("\nMatriz original:\n", matriz)
print("\nVetor:\n", vetor)
print("\nResultado com broadcasting:\n", resultado)

# Matriz com faturamento de 3 produtos em 4 meses
faturamento = np.array([
    [100, 110, 120, 130], # Produto A
    [200, 210, 220, 230], # Produto B
    [300, 310, 320, 330]  # Produto C
])

bonus_por_produto = np.array([5, 10, 15])

print("Faturamento:\n")
print(faturamento)

print("Bônus por Produto:\n")
print(bonus_por_produto)
