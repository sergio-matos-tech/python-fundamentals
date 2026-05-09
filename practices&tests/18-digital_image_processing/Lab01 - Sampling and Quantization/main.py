import cv2
import matplotlib.pyplot as plt
from PIL import Image


image_path = "relogio.tif"

img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
pil_img = Image.open(image_path)

if img is None:
    raise FileNotFoundError(f"Could not load {image_path}")

plt.imshow(img, cmap="gray", vmin=0, vmax=255)
plt.axis("off")
plt.show()

print("Tamanho da imagem:", img.shape)
print(f"DPI original de relogio: {pil_img.info['dpi']}")

# Convertendo para 300, 150 e 72 DPI
for dpi in [300, 150, 72]:
    output_path = f"relogio_{dpi}dpi.tif"
    pil_img.save(output_path, dpi=(dpi, dpi))

    converted_img = Image.open(output_path)
    print(f"\nArquivo: {output_path}")
    print(f"Tamanho: {converted_img.size}")
    print(f"DPI: {converted_img.info['dpi']}")
