numeros_por_extenso = (
    'Zero', 'Um', 'Dois', 'Três', 'Quatro', 'Cinco', 'Seis', 'Sete', 'Oito', 'Nove', 'Dez',
    'Onze', 'Doze', 'Treze', 'Catorze', 'Quinze', 'Dezesseis', 'Dezessete', 'Dezoito',
    'Dezenove', 'Vinte'
)

while True:
    num = int(input("Digite um número entre 0 e 20: "))
    if 0 <= num <= 20:
        break
    else:
        print("ERRO! Tente novamente!")
print(numeros_por_extenso[num])
