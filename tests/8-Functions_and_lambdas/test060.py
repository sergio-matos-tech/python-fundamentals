def area(lenght, width):
    return lenght * width


print("Area Control".center(40))
length = float(input("LENGTH: (M) "))
width = float(input("WIDTH: (M) "))
area = area(length, width)

print(f"The area of the land of {length}m x {width}m is {area}m²")
