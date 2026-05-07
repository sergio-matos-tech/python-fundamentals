import matplotlib.pyplot as plt
import numpy as np

# Simulating heights (in cm)
# mean = 175 cm
# standard deviation = 7 cm
heights = np.random.normal(175, 7, 100000)

plt.hist(heights, bins=30)

plt.xlabel('Height (cm)')
plt.ylabel('Frequency')
plt.title('Normal Distribution of Heights')

plt.show()