import numpy as np

dados = np.arange(16).reshape(4, 4)
print(type(dados))

nova_matriz = dados.copy()

nova_matriz[nova_matriz > 8] = -1

print("Original:\n", dados)
print("\nModificada:\n", nova_matriz)

