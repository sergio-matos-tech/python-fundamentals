from random import choice
food = choice(['apple','grape', 'bacon', 'steak', 'worm', 'dirt'])

print(f"Chosen food -> {food}")
if food == 'apple' or food == 'grape':
    print(f"{food} is fruit!")
elif food == 'bacon' or food == 'steak':
    print(f"{food} is meat!")
else:
    print(f"{food} is yuck")