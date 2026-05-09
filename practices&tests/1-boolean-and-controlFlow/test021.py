import random

names = [
    "Alice",
    "Bob",
    "Charlie",
    "Diana",
    "Edward",
    "Fiona",
    "George",
    "Hannah",
    "Isaac",
    "Jasmine",
    "Kevin",
    "Lily",
    "Michael",
    "Nina",
    "Oliver",
    "Paula",
    "Quincy",
    "Rachel",
    "Sam",
    "Tina",
    "Ulysses",
    "Vera",
    "Walter",
    "Xena",
    "Yvonne",
    "Zachary"
]

len_list = len(names)
index_selected = random.randint(0, len_list - 1)

print(f"The person selected was {names[index_selected]}")

