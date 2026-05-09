def sum_all_numbers(*numbers):
    print(type(numbers))
    return sum(numbers)


print(sum_all_numbers(1, 1, 1, 1, 1, 1))
print(sum_all_numbers(1, 2, 3, 5))
