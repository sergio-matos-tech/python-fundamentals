import calculos

preco = float(input("Digite o preço: R$"))

print(f"A metade de R${preco} é R${calculos.metade(preco)}")
print(f"O dobro de R${preco} é R${calculos.dobro(preco)}")
print(f"Aumentando 10% de R${preco}, temos R${calculos.aumento(preco, 10) + preco}")
