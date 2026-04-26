'''

extract_full_name
Write a function called extract_full_name. This function should accept a list of dictionaries and return a new list of strings with the first and last name keys in each dictionary concatenated.

'''

names = [{'first': 'Elie', 'last': 'Schoppik'}, {'first': 'Colt', 'last': 'Steele'}]
# extract_full_name(names) # ['Elie Schoppik', 'Colt Steele']

# def extract_full_name(names):
#     full_names = []
#     for k, v in names.items():
#         full_names.append(v)
    
#     return full_names


# print(extract_full_name(names))


def decrement_elements_in_a_list(lst):
    return list(map(lambda x: x-1, lst))
    # return [n - 1 for n in lst]


print(decrement_elements_in_a_list([1, 2, 3]))
