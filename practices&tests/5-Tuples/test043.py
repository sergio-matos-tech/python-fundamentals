palavras = ("Python", "Coding", "Bicicleta", "Corinthians", "Manel")
vogais = ('A', 'E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u')

tam_palavras = len(palavras)
for c in range(0, tam_palavras):
    print(f"Na palavra [{palavras[c]}] temos as vogais: ", end='')
    for letra in palavras[c]:
        if letra in vogais:
            print(letra, end=' ')
    print()
