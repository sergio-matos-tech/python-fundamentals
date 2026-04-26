def max_magnitude(numbers):
    return max([abs(n) for n in numbers])



print(max_magnitude([300, 20, -900]))
print(max_magnitude([10, 11, 12]))
print(max_magnitude([-5, -1, -89]))



def sum_even_values(*numbers):
    return sum([n for n in numbers if n % 2 == 0])


print(sum_even_values(1,2,3,4,5,6))
print(sum_even_values(4,2,1,10))
print(sum_even_values(1))

test = list(map(lambda x: x * 2, [1, 2, 3]))
print(test)



def sum_floats(*data):
    return sum([d for d in data if type(d) == float])

print(sum_floats(1.5, 2.4, 'awesome', [], 1))
print(sum_floats(1,2,3,4,5))
