def lerINT(n):
    if isinstance(n, int):
        print(f"Valor digitado: {n}")
    else:
        print("\033[91mErro! Digite um valor correto!\033[0m")


num = input("Digite um número: ")
lerINT(num)
