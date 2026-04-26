cube = lambda num: num **3

'''

Map Time Exercise
Write a function called decrement_list  that accepts a single list of numbers as a parameter.  It should return a copy of the list where each item has been decremented by one. Use map to do this! For example:

decrement_list([1,2,3])   #[0,1,2]

decrement_list([20,14,11])  #[19,13,10]

Tips:

 Remember map doesn't return a list on its own.  decrement_list , however, should return a list.
You can either pass map another name function or use a lambda.  A lambda is preferable, even if it is a little scary looking.

''' 


def decrement_list(lst):
    if lst:
        return list(map(lambda n: n - 1, lst))
    return None


numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(decrement_list(numbers))

def return_evens(lst):
    return list(filter(lambda even : even % 2 == 0, lst))


print(return_evens(numbers))


def first_letters(names, first_leter):
    return list(filter(lambda letter: letter[0] == first_leter, names))



names = ['ana', 'amber', 'jao', 'rosa', 'anthonty']

print(first_letters(names, 'a'))



def remove_negatives(numbers):
    return list(filter(lambda n: n < 0, numbers))



print(remove_negatives([-1,3,4,-99]))
print(remove_negatives([-7,0,1,2,3,4,5]))
print(remove_negatives([50,60,70]))