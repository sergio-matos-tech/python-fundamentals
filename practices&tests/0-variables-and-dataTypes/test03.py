height = float(input("Enter the height in m: "))
weight = float(input("Enter the weight in kg: "))

bmi = weight / (height * height)

print(f"\nYour BMI is approximately {round(bmi)}")
if bmi < 18.5:
    print("And you are underweight.")
elif 18.5 <= bmi < 25:
    print("And you have normal weight")
elif 25 <= bmi < 30:
    print("And you are slightly overweight")
elif 30 <= bmi < 35:
    print("And you are obese")
else:
    print("You are clinically obese")
