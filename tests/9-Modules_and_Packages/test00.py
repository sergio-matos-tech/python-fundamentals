import random
from math import sqrt
import keyword


print(random.choice([54, 32, 23, 23, 4, 43, 9, 98745, 982]))
shuffled = random.shuffle(['apple', 'banana', 'cherry', 'durian'])

print(shuffled)
print(random.randint(1, 20))

print(sqrt(15129))
print(123**2)


def contains_keyword(*strings):
    for s in strings:
        if keyword.iskeyword(s):
            return True
    return False


print(contains_keyword("grizzly", "ignore", "return", "False"))
print(contains_keyword("four", "for", "if"))
print(contains_keyword("def", "haha", "lol", "chicken", "alaska"))
print(contains_keyword("hello", "goodbye"))
print(contains_keyword("blah", "doggo", "crab", "anchor"))

