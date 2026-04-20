numbers = [1,2,3,4]
numbers2 = [3,4,5,6]

answer = [n for n in numbers if n in numbers2]
print(answer)


words = ["Elie", "Tim", "Matt"]

answer2 = [word[::-1].lower() for word in words]
print(answer2)


numbers_one_to_100 = list(range(1, 101))
ansewr_number = [x for x in numbers_one_to_100 if x % 12 == 0]
print(ansewr_number)

string_test = 'amazing'

answer_vowels = [letter for letter in string_test if letter not in 'aeiou']
print(answer_vowels)

nested_list = [[n for n in range(0, 3)] for num in range(0, 3)]
print(nested_list)


nested_list2 = [[n1 for n1 in range(0, 9)] for n2 in range(0, 9)]
print(nested_list2)
