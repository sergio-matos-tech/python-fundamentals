while True:
    try:
        num = int(input("Enter an integer number: "))
        if isinstance(num, int):
            break
        else:
            print("ERROR")
    except ValueError:
        print("Please enter an integer number")

len_num = len(str(num))
c = 0
fator = 1
print(f"Os algarismos de {num}, a partir da unidade, são: ")
for c in range(0, len_num):
    print(f"{(num // fator) % 10}")
    fator *= 10

# unidade = num % 10
# dezena = (num // 10) % 10
# centena = (num // 100) % 10
# milhar = (num // 1000) % 10
# ......
