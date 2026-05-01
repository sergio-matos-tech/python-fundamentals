import numpy as np

array = np.array([[1, 2, 3, 4, 55], [99, 234, 3, 23, 34], [993, 232, 2, 0, 0]])
print(array)
print()
print(array.shape)
print(array.ndim)

print(array[1][2])
print(array[1][::])
print(array[2][3])
print(array[::][-1])

print(array[:, 4])