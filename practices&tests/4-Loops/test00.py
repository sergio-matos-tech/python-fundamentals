

initial_value = int(input())
end_value = int(input())

even_sum_between_i_and_e = 0
for c in range(initial_value, end_value + 1):
    if c % 2 == 0:
        print(c)
        even_sum_between_i_and_e += c
    
print(even_sum_between_i_and_e)
