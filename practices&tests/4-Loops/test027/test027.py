valor_compra = float(input("Qual é o valor da compra? R$"))


def print_compra(float):
    print(f"Valor total da compra é R${float}")


opcao = 0
while True:
    print("FORMAS DE PAGAMENTO")
    print("[1] -> à vista no pix")
    print("[2] -> à vista no cartão")
    print("[3] -> 2x no cartão")
    print("[4] -> 3x no cartão")
    opcao = int(input("Qual opção? "))
    if 1 <= opcao <= 4:
        break

if opcao == 1:
    print("Desconto de 10% aplicado")
    print_compra(valor_compra * 0.9)
elif opcao == 2:
    print("Desconto de 5% aplicado")
    print_compra(valor_compra * 0.95)
elif opcao == 3:
    print(f"O valor da parcela é: {valor_compra / 2}")
    print_compra(valor_compra)
else:
    print(f"O valor da parcela é: {(valor_compra * 1.2) / 3}")
    print(valor_compra * 1.2)
