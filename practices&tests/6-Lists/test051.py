matriz = [[0 for _ in range(3)] for _ in range(3)]

for c in range(0, 3):
    for k in range(0, 3):
        num = int(input(f"Digite um número inteiro para a posição [{c}][{k}] da matriz: "))
        matriz[c][k] = num

print("#" * 50)
for row in range(0, 3):
    for column in range(0, 3):
        print(f"[ {matriz[row][column]:^5} ] ", end='')
    print()
