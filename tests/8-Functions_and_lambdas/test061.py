def escreva(text):
    tam_linha = len(text) + 4
    print("-" * tam_linha)
    print(f"{text}".center(len(text) + 4))
    print("-" * tam_linha)


escreva('Henrique Matos')
escreva('Kakaroto')
escreva('Speed')
