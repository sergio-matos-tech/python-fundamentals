import matplotlib.pyplot as plt
import numpy as np

# Example data
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([2, 4, 5, 7, 8, 10, 12, 14, 18, 20])

# Scatter plot
plt.scatter(x, y)

plt.xlabel('Hours Studied')
plt.ylabel('Exam Score')
plt.title('Positive Correlation')

plt.show()