clubes_brasileiros = (
    'Flamengo', 'Palmeiras', 'São Paulo', 'Santos', 'Corinthians',
    'Grêmio', 'Internacional', 'Atlético Mineiro', 'Cruzeiro', 'Botafogo',
    'Fluminense', 'Vasco da Gama', 'Bahia', 'Sport Recife', 'Ceará',
    'Fortaleza', 'Atlético Paranaense', 'Coritiba', 'Chapecoense', 'Goiás'
)

print("------ CLUBES BRASILEIROS ------".center(20))
for clubes in clubes_brasileiros:
    print(clubes, end=' ')

print("\nOs cinco primeiros são: ")
print(clubes_brasileiros[0:5])

print("Os 4 últimos são: ")
print(clubes_brasileiros[-4:])

print("Times em ordem alfabética")
print(sorted(clubes_brasileiros))

print(f"A Chapecoente está na {clubes_brasileiros.index('Chapecoense')}ª posição")
