from PIL import Image, ImageDraw

CELULA = 16
COLUNAS, LINHAS = 4, 3

PELE = (240, 200, 160, 255)
CABELO = (90, 55, 30, 255)
CAMISA = (50, 110, 220, 255)
BRACO = (35, 80, 170, 255)
CALCA = (60, 60, 90, 255)
SAPATO = (40, 25, 15, 255)

img = Image.new("RGBA", (COLUNAS * CELULA, LINHAS * CELULA), (0, 0, 0, 0))
d = ImageDraw.Draw(img)


def retangulo(col, lin, x0, y0, x1, y1, cor):
    ox, oy = col * CELULA, lin * CELULA
    d.rectangle([ox + x0, oy + y0, ox + x1, oy + y1], fill=cor)


def elipse(col, lin, x0, y0, x1, y1, cor):
    ox, oy = col * CELULA, lin * CELULA
    d.ellipse([ox + x0, oy + y0, ox + x1, oy + y1], fill=cor)


# linha 0: personagem andando (4 quadros)
# posicao x das duas pernas e do braco em cada quadro
pernas = [(6, 8), (4, 8), (6, 8), (6, 10)]
bracos = [7, 6, 7, 8]

for quadro in range(4):
    retangulo(quadro, 0, 5, 2, 10, 3, CABELO)
    retangulo(quadro, 0, 5, 4, 10, 6, PELE)
    retangulo(quadro, 0, 9, 4, 9, 4, (0, 0, 0, 255))
    retangulo(quadro, 0, 5, 7, 10, 11, CAMISA)
    retangulo(quadro, 0, bracos[quadro], 7, bracos[quadro] + 1, 10, BRACO)

    perna_a, perna_b = pernas[quadro]
    fim_a = 14 if quadro == 2 else 15
    retangulo(quadro, 0, perna_a, 12, perna_a + 1, fim_a, CALCA)
    retangulo(quadro, 0, perna_b, 12, perna_b + 1, 15, CALCA)
    retangulo(quadro, 0, perna_a, fim_a, perna_a + 1, fim_a, SAPATO)
    retangulo(quadro, 0, perna_b, 15, perna_b + 1, 15, SAPATO)

# linha 1: grama, terra, nuvem e arbusto
retangulo(0, 1, 0, 0, 15, 15, (120, 80, 45, 255))
retangulo(0, 1, 0, 0, 15, 3, (60, 170, 70, 255))
for x in (1, 5, 9, 13):
    retangulo(0, 1, x, 4, x, 4, (40, 130, 50, 255))

retangulo(1, 1, 0, 0, 15, 15, (120, 80, 45, 255))
for x, y in ((2, 3), (9, 2), (5, 8), (13, 10), (3, 13), (10, 14)):
    retangulo(1, 1, x, y, x + 1, y, (90, 58, 30, 255))

BRANCO = (255, 255, 255, 255)
elipse(2, 1, 0, 6, 7, 12, BRANCO)
elipse(2, 1, 4, 3, 11, 11, BRANCO)
elipse(2, 1, 8, 6, 15, 12, BRANCO)

elipse(3, 1, 0, 8, 8, 15, (35, 130, 55, 255))
elipse(3, 1, 6, 5, 15, 15, (35, 130, 55, 255))
retangulo(3, 1, 8, 7, 9, 8, (80, 190, 90, 255))


def bloco(col, cor, borda):
    retangulo(col, 2, 0, 0, 15, 15, borda)
    retangulo(col, 2, 1, 1, 14, 14, cor)
    for x, y in ((2, 2), (13, 2), (2, 13), (13, 13)):
        retangulo(col, 2, x, y, x, y, borda)


# linha 2: bloco, bloco usado e moeda
bloco(0, (235, 175, 45, 255), (140, 85, 20, 255))
CLARO = (255, 240, 170, 255)
for x0, y0, x1, y1 in ((5, 3, 10, 3), (4, 4, 5, 5), (10, 4, 11, 6),
                       (8, 7, 10, 7), (7, 8, 8, 9), (7, 11, 8, 12)):
    retangulo(0, 2, x0, y0, x1, y1, CLARO)

bloco(1, (150, 120, 90, 255), (95, 70, 50, 255))

elipse(2, 2, 4, 1, 11, 14, (140, 85, 20, 255))
elipse(2, 2, 5, 2, 10, 13, (250, 205, 40, 255))
retangulo(2, 2, 7, 4, 8, 11, (255, 240, 150, 255))

img.save("spritesheet.png")
