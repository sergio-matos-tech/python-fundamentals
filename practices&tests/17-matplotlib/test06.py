import matplotlib.pyplot as plt
import numpy as np

data = np.random.normal(70, 10, 1000)

plt.hist(data, bins=20)

plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram Example')

plt.show()