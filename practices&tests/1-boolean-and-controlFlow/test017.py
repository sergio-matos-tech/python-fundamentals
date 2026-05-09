name = str(input("Enter a full name: ")).strip()

qtd_names = name.count(' ')
first_name = name.split(' ')[0]
last_name = name.split(' ')[qtd_names]

print(f"Your first name is {first_name} and your last name is {last_name}")
