print("\n ----- Leap Year Check -----\n")

check_year = int(input("Enter the year you want to check: "))

if check_year % 4 == 0:
    if check_year % 100 == 0 and check_year % 400 == 0:
        print(f"{check_year} is a leap year (; !!!")
    print(f"{check_year} IS NOT a leap year ):")
else:
    print(f"{check_year} IS NOT a leap year ):")
