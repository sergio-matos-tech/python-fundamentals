import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#%matplotlib inline


x = np.linspace(0, 10, 100)
y = np.sin(x)


plt.plot(x, y)
plt.xlabel('X')
plt.ylabel('Sin')

plt.title('Sin Wave')

plt.grid(True)
plt.show()