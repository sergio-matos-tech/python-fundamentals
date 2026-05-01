import numpy as np



# Criando um array de 1 dimensão (vetor) a partir de uma lista Python
vetor = np.array([17, 21, 100, 34])
print("\nVetor (Array 1D):\n")
print(vetor)

print("Formato (shape) do vetor:", vetor.shape) 
print("Número de dimensões (ndim) do vetor:", vetor.ndim)
print("Número total de elementos (size) do vetor:", vetor.size)


# Criando um array de 2 dimensões (matriz) a partir de uma lista de listas
matriz = np.array([[1, 2, 3], [4, 5, 6]])
print("\nMatriz (Array 2D):\n")
print(matriz)

print("Formato (shape) da matriz:", matriz.shape)  # (linhas, colunas)
print("Número de dimensões (ndim) da matriz:", matriz.ndim)
print("Número total de elementos (size) da matriz:", matriz.size)

arr = np.arange(24).reshape(4, 3, 2)
print("\nArray (Array 3D):\n")
print(arr)

print("Formato (shape) do array:", arr.shape) 
print("Número de dimensões (ndim) do array:", arr.ndim)
print("Número total de elementos (size) do array:", arr.size)


# Array 4D com valores sequenciais de 0 a 119 organizado em 2x3x4x5 (2 blocos, 3 "planos", 4 linhas, 5 colunas)
tensor_4d = np.arange(120).reshape(2, 3, 4, 5)
print(tensor_4d)  

print("Formato (shape) do array:", tensor_4d.shape) 
print("Número de dimensões (ndim) do array:", tensor_4d.ndim)
print("Número total de elementos (size) do array:", tensor_4d.size)