def is_all_strings(iterable):
    return all(type(i) == str for i in iterable)


print(is_all_strings(['a', 'b', 'c']))
print(is_all_strings([2,'a', 'b', 'c']))
print(is_all_strings([2,'a', 'b', 'c']))



'''


Extremes Exercise - Using Min and Max
Write a function called extremes  which accepts an iterable. It should return a tuple containing the minimum and maximum elements.  For example:

extremes([1,2,3,4,5])  # (1, 5)

extremes((99,25,30,-7))  # (-7, 99)

extremes("alcatraz")  #( 'a', 'z')

REMEMBER, RETURN A TUPLE!!!



'''


def extremes(iterable):
    if not iterable:
        return None
    return (min(iterable), max(iterable))

print(extremes([1,2,3,4,5]))
print(extremes((99,25,30,-7)))
print(extremes("alcatraz"))



