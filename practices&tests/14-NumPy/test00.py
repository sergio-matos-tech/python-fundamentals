import numpy as np
import math
import time

precos_np = np.random.rand(10_000_000)
print(type(precos_np))

precos_list = list(precos_np)
print(type(precos_list))


# Operação com NumPy
t0 = time.time()
desc = precos_np * 0.90
final = desc + 5
raiz = np.sqrt(precos_np)
print("NumPy:", time.time() - t0, "segundos")


# Mesma operação com Python puro
t0 = time.time()
desc = [p * 0.90 for p in precos_list]
final = [p + 5 for p in desc]
raiz = [math.sqrt(p) for p in precos_list]
print("Python puro:", time.time() - t0, "segundos")


# Python puro com for loops
t0 = time.time()

desc = []
for p in precos_list:
    desc.append(p * 0.90)

final = []
for p in desc:
    final.append(p + 5)

raiz = []
for p in precos_list:
    raiz.append(math.sqrt(p))

print("Python puro (for loop):", time.time() - t0, "segundos")