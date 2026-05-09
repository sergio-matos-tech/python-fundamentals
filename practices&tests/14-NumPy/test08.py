from PIL import Image
import numpy as np

img = Image.open('../14-NumPy/102-Cap08/imagem2.png')

array_img = np.array(img)

print("\nFormato do array:\n", array_img.shape)  
# (altura, largura, 3) → 3 canais = R, G, B

altura, largura, canais = array_img.shape
print(f"\nAltura: {altura}, Largura: {largura}, Canais: {canais}")

R = array_img[:, :, 0]  # Canal vermelho
G = array_img[:, :, 1]  # Canal verde
B = array_img[:, :, 2]  # Canal azul

print("\nExtraindo um dos pixels:\n", array_img[590, 1287])  

pixel = array_img[590, 1287]
r, g, b = pixel
print(f"\nPixel [617,1287] → R={r}, G={g}, B={b}")