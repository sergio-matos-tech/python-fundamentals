frase = str(input("Digite uma frase: ")).strip().lower()

tam_frase = len(frase)
cont_final = tam_frase
frase_inversa = str()

for c in range(0, tam_frase):
    frase_inversa += frase[cont_final - 1]
    cont_final -= 1

print(f"Frase inicial: {frase}")
print(f"Frase invertida: {frase_inversa}")
if frase == frase_inversa:
    print("É palindroma!")
else:
    print("Não é palimdroma!")
