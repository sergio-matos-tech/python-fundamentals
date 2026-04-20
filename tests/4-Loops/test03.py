from random import randint

generated_number = 0

while generated_number != 5:
    generated_number = randint(1, 10)
    print(generated_number, end=' ')
print()
