name = str(input("Enter your full name: "))
print(f"You name in uppercase is [{name.upper()}]\nYour name in lowercase is [{name.lower()}] ")
print(f"Your full name has [{len(name) - name.count(' ')} letters]")

# split is used to split the string whenever there's space
# and [0] is used to take  the first one of this split
first_word = name.split(' ')[0]

print(f"Your first name is [{first_word}] and its got [{len(first_word)} letters]")
