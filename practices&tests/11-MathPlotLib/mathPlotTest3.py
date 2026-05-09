import numpy as np
import matplotlib.pyplot as plt

# Definir o intervalo de x (apenas valores positivos)
x = np.linspace(0.01, 2, 400)  # Gera 400 pontos entre 0.01 e 2

# Definir as funções
g_x = np.ones_like(x)  # Função constante g(x) = 1 (array de uns)
h_x = x * np.log(x)  # Função h(x) = x * ln(x)

# Plotar as funções
plt.plot(x, g_x, label='g(x) = 1')
plt.plot(x, h_x, label='h(x) = x * ln(x)')

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