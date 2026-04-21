frase = " Python é uma linguagem poderosa e estou aprendendo com a DSA "
print(len(frase))
frase = frase.strip()
print(len(frase))

frase = frase.split()
print(frase)
print(frase[0])


ingredientes = ['Arroz', 'Feijão', 'Macarrão', 'Ovo']
ingredientes.remove('Macarrão')
print(ingredientes)


dias_da_semana = ('Segunda', 'Terça', 'Quarta')

filme = {
    'titulo': "O Poderoso Chefão",
    'ano': 1972,
    'diretor': "Francis Ford Coppola"
}

print(filme.get('ano'))
filme['gênero'] = 'Drama'
print(filme)
filme['ano'] = 1973
print(filme)


numbers = [1, 2, 2, 3, 4, 4, 5, 1]
numbers_withou_duplicates = set(numbers)
print(numbers_withou_duplicates)

set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}

print(set.intersection(set_a, set_b))
