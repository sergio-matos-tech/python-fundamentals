'''
triple_and_filter
Write a function called triple_and_filter. This function should accept a list of numbers, filter out every number that is not evenly divisible by 4 (i.e., filter out numbers that do not divide by 4 with a remainder of zero), and return a new list where every remaining number is tripled.

'''



def triple_and_filter(numbers):
    not_divisible_by_four = list(filter(lambda x: x % 4 == 0, numbers))
    # not_divisible_by_four = [n for n in numbers if n % 4 != 0]
    return [n * 3 for n in not_divisible_by_four]



print(triple_and_filter([1,2,3,4]))
print(triple_and_filter([6,8,10,12]))
