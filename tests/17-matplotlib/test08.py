import matplotlib.pyplot as plt


labels = ['Python', 'Java', 'JavaScript']
sizes = [40, 25, 35]

plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('Programming Language Popularity')

plt.show()