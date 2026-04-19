from random import choice
food = choice(['apple','grape', 'bacon', 'steak', 'worm', 'dirt'])

print(f'Choice: {food}')
if food in ('apple', 'grape'):
    print('Fuit')
elif food in ('bacon', 'steak'):
    print('Meat')
elif food in ('dirt', 'worm'):
    print('Yuck')
