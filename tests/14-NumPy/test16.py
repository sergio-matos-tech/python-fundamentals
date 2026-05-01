import numpy as np

A = np.array([[2, 1],
              [1, 3]])

b = np.array([8, 7])

x = np.linalg.solve(A, b)
print(x)

