import numpy as np


dados = np.arange(16).reshape(4, 4)
print("\nMatriz Original:\n")
print(dados)

elemento = dados[1, 2]
print(f"\nElemento na posição [1, 2]: {elemento}\n")

primeira_linha = dados[0] 
print(f"Primeira linha:\n{primeira_linha}\n")

segunda_coluna = dados[:, 1]
print(f"Segunda coluna:\n{segunda_coluna}\n")

bloco_superior_esquerdo = dados[:2, :2]
print(f"Bloco 2x2 superior esquerdo:\n{bloco_superior_esquerdo}\n")

print("\nMatriz Original:\n")
print(dados)
maiores_que_10 = dados[dados > 10]
print(f"\nNúmeros maiores que 10:\n {maiores_que_10}")

matriz = np.arange(25).reshape(5, 5)
resultado = matriz[::2, 1::2]

print("Matriz Original:")
print(matriz)
print("\nLinhas Pares e Colunas Ímpares:")
print(resultado)