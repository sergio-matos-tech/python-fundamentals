from collections import Counter
from functools import reduce
import operator




def last_element_of_list(list):
    return list[-1]



def single_letter_count(letters, letter):
    if letters and letter:
        return letters.count(letter)
    return None
    


def multiple_letter_count(string):
    dict_string = dict()
    
    for s in string:
        dict_string[s] = single_letter_count(string, s)
    
    return dict_string



def multiple_letter_count1(string):
    return {letter: string.count(letter) for letter in string}



def list_manipulation(lst, command, location, value=0):
    command = command.lower()
    location = location.lower()

    if command == 'remove':
        if location == 'end':
            return lst.pop()
        elif location == 'beginning':
            return lst.pop(0)

    elif command == 'add':
        if location == 'beginning':
            lst.insert(0, value)
        elif location == 'end':
            lst.append(value)
        return lst

    return None



# 1. Remove from end
lst = [1, 2, 3, 4]
result = list_manipulation(lst, "remove", "end")
assert result == 4
assert lst == [1, 2, 3]

# 2. Remove from beginning
lst = [10, 20, 30]
result = list_manipulation(lst, "remove", "beginning")
assert result == 10
assert lst == [20, 30]

# 3. Add to beginning
lst = [2, 3, 4]
result = list_manipulation(lst, "add", "beginning", 1)
assert result == [1, 2, 3, 4]
assert lst == [1, 2, 3, 4]

# 4. Add to end
lst = [5, 6]
result = list_manipulation(lst, "add", "end", 7)
assert result == [5, 6, 7]
assert lst == [5, 6, 7]




def is_palindrome(string):
    if not string:
        return None
    
    lower_string = string.lower().replace(' ', '')
    lower_string_inverted = lower_string[::-1]
    
    return lower_string == lower_string_inverted
    
    

def is_palindrome1(string):
    return string == string[::-1]




def frequency(lst, search_term):
    return lst.count(search_term)

def frequency1(lst, search_term):
    freq = Counter(lst)
    print(freq)
    return freq[search_term]


print(frequency(['a', 'b', 'a', 'a', 'b'], 'a'))
print(frequency([23, 32, 2, 2, 3, 2, 22, 234, 2], 2))

print(frequency1(['a', 'b', 'a', 'a', 'b'], 'a'))
print(frequency1([23, 32, 2, 2, 3, 2, 22, 234, 2], 2))


def multiply_even_numbers(lst):
    even_numbers = [x for x in lst if x % 2 == 0]
    return reduce(operator.mul, even_numbers)


print(multiply_even_numbers([2, 3, 4, 5, 67, 8, 99, 9, 1, 66, 2, 4]))


def intersection(lst1, lst2):
    return [obj for obj in lst1 if obj in lst2]



print(intersection([1, 2, 3, 4], [1, 3, 5, 7]))

