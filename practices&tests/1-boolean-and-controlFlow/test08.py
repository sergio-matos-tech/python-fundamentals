print("\n===== LOVE CALCULATOR =====\n")
name1 = str(input("Enter the first name: "))
name2 = str(input("Enter the second name: "))

string = name1 + name2  # concatenating the two strings
string = string.lower()  # changing the string to lowerCase
cont1 = 0
cont2 = 0

# looping through the string to check if there are the letters we want in the string and counting it
for letras in string:
    if letras in "true":
        cont1 += 1

for letras in string:
    if letras in "love":
        cont2 += 1

# changing the data type from int into string, so that we can concatenate the strings
cont3 = str(cont1) + str(cont2)

print(f"Your score is {cont3}.")
