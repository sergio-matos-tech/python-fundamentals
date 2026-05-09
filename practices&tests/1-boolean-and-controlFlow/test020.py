import random

player = str(input("Heads or Tails? ")).lower()

computer = random.choice(["heads", "tails"])


print(f"Player gamble: {player}")
print(f"Computer gamble: {computer}")

if player == computer:
    print("You got it right!")
else:
    print("You lost!")
