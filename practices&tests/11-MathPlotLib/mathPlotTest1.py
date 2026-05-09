import numpy as np
import matplotlib.pyplot as plt

# Definir o intervalo de x
x = np.linspace(-2, 2, 400)  # Gera 400 pontos entre -2 e 2

# Definir as funções
g_x = 4 * np.cos(x)
h_x = np.exp(2 * x)

# Plotar as funções
plt.plot(x, g_x, label='g(x) = 4 cos(x)')
plt.plot(x, h_x, label='h(x) = e^(2x)')

# Adicionar título e labels
plt.title('Gráfico de g(x) e h(x)')
plt.xlabel('x')
plt.ylabel('y')

# Adicionar uma grade para melhor visualização
plt.grid(True)

# Adicionar uma legenda
plt.legend()

# Mostrar o gráfico
plt.show()