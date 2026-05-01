import numpy as np

matriz = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
])

array_terceira_coluna = matriz[:, 2]
print(array_terceira_coluna)

bloco_central = matriz[1:3, 1:3]
print(f'bloco_central: \n{bloco_central}')

