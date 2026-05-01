import numpy as np

matriz = np.arange(81).reshape(9, 9)

print(matriz)
print()

indice_par_coluna_impar = matriz[::2, 1:-1:2]
print(indice_par_coluna_impar)

