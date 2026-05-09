target = int(input("Enter a number between 0 and 1000: "))

sum_even = 0
if 0 <= target <= 1000:
    for c in range(2, target + 1):
        if c % 2 == 0:
            sum_even += c

print(sum_even)
