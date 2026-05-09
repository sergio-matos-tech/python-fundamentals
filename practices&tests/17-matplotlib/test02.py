import numpy as np
import matplotlib.pyplot as plt


x = np.arange(1.0, 5.2, 0.1)
y = 1.2 ** x

x2 = x[:]  #gera cópia raza de x
y2 = np.log(x2)

x3 = x
y3 = np.cos(x3)

plt.title('Três funções')

plt.plot(x, y,'bo', x2, y2, x3, y3, 'r--')

plt.legend( ('exponencial', 'logaritmo', 'cosseno'), loc='lower right' )

plt.show()
