sex = ''
while sex not in {'M', 'm', 'F', 'f'}:
    sex = str(input("Enter your sex: ")).strip()
print(f"Sex {sex} registered successfully")
