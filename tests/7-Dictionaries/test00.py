user_info = dict()

user_info = [{'Name': 'Goku', 'HP': 99.5},
             {'Name': 'Vegeta', 'HP': 98.6}]

print(user_info)
print(user_info[0]['Name'])


donations = dict(sam=25.0, lena=88.99, chuck=13.0, linus=99.5, stan=150.0, lisa=50.25, harrison=10.0)

total_donations = 0
for key, value in donations.items():
    total_donations += value


print(total_donations)
