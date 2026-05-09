frase = str(input("Enter a frase: ")).lower().replace(" ", "")
# the method replace is used to replace a string with

first_letter = frase[0]
qtd_first_letter = frase.count(first_letter)
print(f"The first letter is '{first_letter}' and this letter was shown '{qtd_first_letter} times' in this frase ")

c = 0
pos = 0
len_string = len(frase)
for c in range(0, len_string):
    if first_letter == frase[c]:
        pos = c

print(f"And '{first_letter}' appeared for the last time in position {pos}")
