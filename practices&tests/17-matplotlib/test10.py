import matplotlib.pyplot as plt
import numpy as np

# Example data
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([15, 12, 11, 9, 8, 7, 5, 2, 1, 0])

# Scatter plot
plt.scatter(x, y)

plt.xlabel('Hours Studied')
plt.ylabel('Exam Score')
plt.title('Positive Correlation')

plt.show()