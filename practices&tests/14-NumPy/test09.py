from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# --- Carrega a imagem ---
img = Image.open('../14-NumPy/102-Cap08/imagem2.png')
array_img = np.array(img)

# Obtendo dimensões
altura, largura, canais = array_img.shape
print(f"Altura: {altura}, Largura: {largura}, Canais: {canais}")

# --- Definindo um corte central ---
# Tamanho do recorte 
recorte_h = 280
recorte_w = 400

# Definimos o centro da matriz
centro_y = altura // 2
centro_x = largura // 2

# Calculando limites para o recorte central (operações com matrizes para fatiar a imagem)
y_inicio = centro_y - recorte_h // 2
y_fim = centro_y + recorte_h // 2
x_inicio = centro_x - recorte_w // 2
x_fim = centro_x + recorte_w // 2

# Fazendo o slice (fatiamento) no array
corte_central = array_img[y_inicio:y_fim, x_inicio:x_fim]

print(f"\nFormato do recorte: {corte_central.shape}")  

# --- Mostra a imagem original e o corte ---
plt.figure(figsize = (10,5))
plt.subplot(1,2,1)
plt.title("Imagem Original")
plt.imshow(array_img)
plt.axis("off")

plt.subplot(1,2,2)
plt.title("Corte Central")
plt.imshow(corte_central)
plt.axis("off")

plt.show()