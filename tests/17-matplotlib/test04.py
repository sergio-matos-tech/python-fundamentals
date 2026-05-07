import matplotlib.pyplot as plt
import numpy as np

years = np.array([2022, 2023, 2024, 2025, 2026])
amount_of_students = np.array([15, 22, 25, 23, 18])
amount_of_subscriptions = np.array([0, 20, 50, 60, 30])

plt.plot(years, amount_of_students, marker='.', markersize=8, markerfacecolor='cyan', linewidth='2.5')
plt.plot(years, amount_of_subscriptions)
plt.xlabel('Year')
plt.ylabel('Amount of Students')
plt.title('Amount of students per year')
plt.grid(True)

plt.show()

