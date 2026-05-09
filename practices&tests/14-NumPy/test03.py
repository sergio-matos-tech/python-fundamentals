import numpy as np


precos = np.array([19.99, 25.50, 8.90, 43.00])
print(f"\nPreços originais: {precos}\n")

precos_com_desconto = precos * 0.90
print(f"Preços com 10% de desconto: {precos_com_desconto}\n")

precos_finais = precos_com_desconto + 5.00
print(f"Preços finais com frete: {precos_finais}\n")

raizes = np.sqrt(precos)
print(f"Raiz quadrada dos preços: {raizes}")