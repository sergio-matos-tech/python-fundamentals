import cv2
import matplotlib.pyplot as plt
from PIL import Image


image_path = "relogio.tif"

img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
pil_img = Image.open(image_path)

if img is None:
    raise FileNotFoundError(f"Could not load {image_path}")

plt.imshow(img, cmap="gray", vmin=0, vmax=255)
plt.title(f"Original DPI: 1250 - {img.shape}")
plt.axis("off")
plt.show()

print("Tamanho da imagem:", img.shape)
print(f"DPI original de relogio: {pil_img.info['dpi']}")

dpi_original = pil_img.info["dpi"][0]
largura_original, altura_original = pil_img.size

# Convertendo a resolucao e o metadado de DPI para 300, 150 e 72 DPI
for dpi in [300, 150, 72]:
    escala = dpi / dpi_original
    nova_largura = int(largura_original * escala)
    nova_altura = int(altura_original * escala)

    resized_img = pil_img.resize((nova_largura, nova_altura))

    output_path = f"relogio_{dpi}dpi.tif"
    resized_img.save(output_path, dpi=(dpi, dpi))

    converted_img = Image.open(output_path)

    print(f"\nArquivo: {output_path}")
    print(f"Resolucao: {converted_img.size}")
    print(f"DPI: {converted_img.info['dpi']}")

    plt.imshow(converted_img, cmap="gray", vmin=0, vmax=255)
    plt.title(f"{dpi} DPI - {converted_img.size[0]} x {converted_img.size[1]} px")
    plt.axis("off")
    plt.show()
