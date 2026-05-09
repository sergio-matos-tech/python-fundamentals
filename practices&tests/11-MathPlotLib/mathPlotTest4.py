import numpy as np
import matplotlib.pyplot as plt

# Definir o intervalo de x (apenas valores positivos)
x = np.linspace(-1, 10, 800)  # Gera 400 pontos entre 0.01 e 2

# Definir as funções
g_x = np.power(x, 3)
h_x = -x + 100

# Plotar as funções
plt.plot(x, g_x, label='g(x) = x³')
plt.plot(x, h_x, label='h(x) = -x + 100')

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