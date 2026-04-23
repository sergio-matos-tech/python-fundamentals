def classify_triangle(side1, side2, side3):
    if (side1 <= 0 or side2 <= 0 or side3 <= 0):
        return None
    
    if side1 == side2 and side1 == side3:
        return 'Equilátero'
    
    if side1 != side2 and side1 != side3:
        return 'Escaleno'
    
    if (side1 == side2 and side1 == side3) or (side2 == side3 and side2 != side1) or (side3 == side1 and side3 != side2):
        return 'Isóceles'



print(classify_triangle(2, 2, 3))
    
    
def tabuada(num):
    for c in range(1, 10):
        print(f'{c} * {num} = {c * num}')


print(tabuada(7))



def alunos_acima_da_media(dictionary):
    
    if not dictionary:
        return []
    
    alunos_acima_da_media = list()
    media_notas = 0
    
    media_notas = sum(dictionary.values()) / len(dictionary)
    
    for k, v in dictionary.items():
        if v > media_notas:
            alunos_acima_da_media.append(k)
    
    return [k for k, v in dictionary.items() if v > media_notas]


def emails_validos(emails, dominio='gmail.com'):
    return [s for s in emails if dominio in s]

print(emails_validos(['carione@gmail.com', 'jubilar@hotmail.com', 'jultion@gmail.com']))


def retorna_upper_e_python(string_list):
    return [s.upper() + ' Python' for s in string_list]



print(retorna_upper_e_python(['Joao', 'Maior', 'Carr ']))