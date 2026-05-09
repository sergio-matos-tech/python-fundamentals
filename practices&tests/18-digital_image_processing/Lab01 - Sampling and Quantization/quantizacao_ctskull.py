from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


IMAGE_PATH = "ctskull-256.tif"
OUTPUT_DIR = Path("ctskull_quantizada")


def quantizar_imagem(img_array, bits):
    niveis = 2**bits
    passo = 256 / niveis

    indices = np.floor(img_array / passo)
    indices = np.clip(indices, 0, niveis - 1)

    img_quantizada = np.round(indices * (255 / (niveis - 1)))
    return img_quantizada.astype(np.uint8)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    img = Image.open(IMAGE_PATH).convert("L")
    img_array = np.array(img)

    print(f"Imagem original: {IMAGE_PATH}")
    print(f"Tamanho: {img_array.shape}")
    print("Bits original: 8")

    imagens = [(8, img_array)]

    for bits in range(7, 0, -1):
        img_quantizada = quantizar_imagem(img_array, bits)
        imagens.append((bits, img_quantizada))

        output_path = OUTPUT_DIR / f"ctskull_{bits}bits.tif"
        Image.fromarray(img_quantizada).save(output_path)

        print(f"{bits} bit(s): {2**bits} niveis -> {output_path}")

    fig, axes = plt.subplots(2, 4, figsize=(10, 6))
    axes = axes.ravel()

    for ax, (bits, imagem) in zip(axes, imagens):
        ax.imshow(imagem, cmap="gray", vmin=0, vmax=255)
        ax.set_title(f"{bits} bits")
        ax.axis("off")

    plt.tight_layout()

    comparison_path = OUTPUT_DIR / "comparacao_8a1bits.png"
    plt.savefig(comparison_path, dpi=150)

    if matplotlib.get_backend().lower() != "agg":
        plt.show()

    print(f"Comparacao salva em: {comparison_path}")


if __name__ == "__main__":
    main()
