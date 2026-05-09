import numpy as np
import matplotlib.pyplot as plt



import matplotlib.pyplot as plt
import numpy as np

plt.subplot(1, 3, 1)

pi = np.pi

x1 = np.arange( -4 * pi, 4 * pi, 0.1)
y1 = np.sin(x1)
plt.title('seno')
plt.plot(x1, y1, 'b--')

plt.subplot(1, 3, 2)
x2 = x1
y2 = np.cos(x2)
plt.title('cosseno')
plt.plot(x2, y2, 'go')

plt.subplot(1,3, 3)
x3 = x1
y3 = np.tan(x3)
plt.plot(x3, y3, 'r')
plt.title('tangente')
plt.show()
