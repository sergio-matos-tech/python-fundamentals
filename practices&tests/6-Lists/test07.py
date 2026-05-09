names = ["Elie", "Tim", "Matt"]
numbers = [1,2,3,4,5,6]

answer = list()

for name in names:
    answer.append(name[0])
    
print(answer)

answer2 = list()
for n in numbers:
    if n % 2 == 0:
        answer2.append(n)

print(answer2)

# list comprehensions
answer_test = [person[0] for person in ["Elie", "Tim", "Matt"]]
answer2_test = [val for val in [1, 2, 3, 4, 5, 6] if val % 2 == 0]
