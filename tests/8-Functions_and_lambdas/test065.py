def fatorial(num):
    if num == 0 or num == 1:
        return 1
    return num * fatorial(num - 1)


def fatorial_loop(n, show):
    if n >= 0:
        cont = n
        fatorial = 1
        while cont > 0:
            fatorial *= cont
            if show:
                if cont > 1:
                    print(f"{cont} X", end=' ')
                else:
                    print(f"{cont} =", end=' ')
            cont -= 1
        print(f"{fatorial}")


fatorial_loop(5, True)
print(fatorial(7))
