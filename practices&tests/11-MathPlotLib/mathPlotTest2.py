
import numpy as np
import matplotlib.pyplot as plt

# Definir o intervalo de x
x = np.linspace(-2, 2, 400)  # Gera 400 pontos entre -2 e 2

# Definir as funções
g_x = x / 2
h_x = np.tan(g_x)

h_x[np.abs(np.cos(x)) < 1e-10] = np.nan  # Evita divisão por zero

# Plotar as funções
plt.plot(x, g_x, label='g(x) = x/2')
plt.plot(x, h_x, label='h(x) = tang(x)')

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