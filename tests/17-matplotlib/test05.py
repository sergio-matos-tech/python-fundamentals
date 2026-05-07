import matplotlib.pyplot as plt
import numpy as np

languages = ['Python', 'Java', 'C++', 'JavaScript']
students = [45, 30, 15, 40]

plt.bar(languages, students)

plt.xlabel('Programming Languages')
plt.ylabel('Number of Students')
plt.title('Students per Language')

plt.show()