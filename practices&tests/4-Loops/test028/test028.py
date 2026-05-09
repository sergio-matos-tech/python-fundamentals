from time import sleep

qtd_termos = int(input("Quantos termos tem a P.A? "))
primeiro_termo = int(input("Qual é o primeiro termo? "))
razao = int(input("Qual é a razão da P.A? "))

for c in range(primeiro_termo, qtd_termos + 1):
    print(f"{c * razao}", end=' -> ')
    sleep(0.3)
print("End")
