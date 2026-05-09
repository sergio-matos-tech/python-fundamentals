import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#%matplotlib inline


linear_subplot = plt.subplot()

x = np.arange(0, 10)
y = np.arange(0, 20, 2)

linear_subplot.plot(x, y)
linear_subplot.plot(y, x)

linear_subplot.set_xlabel('X')
linear_subplot.set_ylabel('Y')
linear_subplot.set_title('Linear Graph')

plt.show()



