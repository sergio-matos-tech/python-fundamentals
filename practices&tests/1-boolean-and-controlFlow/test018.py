import random
import time

print("\n===== I'm gonna think of a number between 1 and 5. Try guessing it. =====")
time.sleep(1)
print("Generating number...")
time.sleep(2)

generated_number = random.randint(1, 5)
cont = 0
while True:
    cont += 1
    while True:
        try:
            num_user = int(input("Make your guess: "))
            if isinstance(num_user, int):
                break
        except ValueError:
            print("ERROR>>> Try again!")
    if generated_number > num_user:
        print(f"I've generated a number GREATER than {num_user}")
    elif generated_number < num_user:
        print(f"I've generated a number LESS than {num_user}")
    else:
        break
print(f"Congrats!!! You've guest it in {cont} tries. I've generated the number {generated_number}")
