from random import choice, randint


actually_sick = choice([True, False])
kinda_sick = choice([True, False])
hate_your_job = choice([True, False])
sick_days = randint(0, 10)

calling_in_sick = None
if (actually_sick and sick_days > 0) or (kinda_sick and hate_your_job and sick_days > 0):
    calling_in_sick = True
else:
    calling_in_sick = False

print(calling_in_sick)
