import numpy as np

matriz = np.arange(25).reshape(5, 5)
print(f'{matriz}\n')

temp1 = matriz[0, :]
temp2 = matriz[1:, -1]
temp3 = matriz[-1, -2::-1]
temp4 = matriz[-2::-1, 0]

print(temp1)
print(temp2)
print(temp3)
print(temp4)

array = np.concatenate([temp1, temp2, temp3, temp4])

print(array)