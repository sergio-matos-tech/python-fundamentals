student_heights = input("Enter the heights in meters: ").split()  # student_heights will become type list

sum_heights = 0

for student in student_heights:
    sum_heights += int(student)

average_height = sum_heights / len(student_heights)
print(average_height)
