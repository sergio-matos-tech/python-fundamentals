import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(f"\nMatriz A:\n{A}\n")
print(f"Matriz B:\n{B}\n")

produto_matricial = A @ B
print(f"Produto de A por B:\n\n{produto_matricial}\n")

produto_element_wise = A * B
print(f"Multiplicação Element-wise de A por B:\n{produto_element_wise}\n")