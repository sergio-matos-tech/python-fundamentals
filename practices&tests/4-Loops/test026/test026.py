price_of_the_house = float(input("What's the price of the house? R$"))
salary_buyer = float(input("What's the salary of the buyer? R$"))
years_paying = int(input("In how many years it will be paid? "))

month_cost = price_of_the_house / (years_paying * 12)

print(f"To pay a house of R${price_of_the_house} in {years_paying} years, the month cost will be R${month_cost:.3f}")
if month_cost < (salary_buyer * 0.3):
    print("Borrow accepted!")
else:
    print("Borrow rejected!")
