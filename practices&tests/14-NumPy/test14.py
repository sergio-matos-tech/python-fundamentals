import numpy as np

matriz = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])
print(f'{matriz}\n')

media_dos_elementos_da_matriz = matriz.mean()
desvio_padrao = matriz.std()

print(f'Soma dos elementos da matriz: {matriz.sum()}')
print(f'Média: {media_dos_elementos_da_matriz}')
print(f'Desvio Padrão: {desvio_padrao}\n')

nova_matriz = (matriz - media_dos_elementos_da_matriz) / desvio_padrao
print(nova_matriz)

