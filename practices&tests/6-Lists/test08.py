import timeit

setup = """
names = ["Elie", "Tim", "Matt"] * 100000
numbers = list(range(1, 100000))
"""

# for loop + append
loop_test = """
answer = []
for name in names:
    answer.append(name[0])
"""

# list comprehension
list_comp_test = """
answer = [name[0] for name in names]
"""

# even numbers with loop
loop_even = """
answer = []
for n in numbers:
    if n % 2 == 0:
        answer.append(n)
"""

# even numbers with comprehension
comp_even = """
answer = [n for n in numbers if n % 2 == 0]
"""

print("Loop (names):", timeit.timeit(loop_test, setup=setup, number=100))
print("List comprehension (names):", timeit.timeit(list_comp_test, setup=setup, number=100))

print("Loop (even numbers):", timeit.timeit(loop_even, setup=setup, number=100))
print("List comprehension (even numbers):", timeit.timeit(comp_even, setup=setup, number=100))

print(min(timeit.repeat(loop_test, setup=setup, number=100, repeat=5)))
print(min(timeit.repeat(list_comp_test, setup=setup, number=100, repeat=5)))

