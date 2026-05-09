student_scores = list()
amount_scores = int(input("How much scores do you want to add? "))

c = 0
highest_score = 0
for c in range(0, amount_scores):
    student_score = int(input(f"Enter the {c + 1}º score: "))
    if student_score >= 0:
        student_scores.append(student_score)
        if student_score > highest_score:
            highest_score = student_score

    c += 1

print(f"highest score was {highest_score}")
