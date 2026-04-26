from datetime import datetime


def voto(idade):
    if idade < 16:
        return 'NEGADO'
    elif 16 <= idade <= 18 or idade > 70:
        return 'FACULTATIVO'
    else:
        return 'OBRIGATÓRIO'


print()

ano_de_nasc = int(input("Ano de nascimento: "))
idade = datetime.now().year - ano_de_nasc
print(f"Com {idade} anos: VOTO {voto(idade)}")
