import random

print("Jogo do par ou ímpar".center(50))

score_player = 0
score_computer = 0

option_player = ''
while True:
    num_player = int(input("Enter an integer between 0 and 10: [-1 to stop] "))
    if num_player < 0:
        break
    num_computer = random.randint(0, 11)
    option_player = input("Even or Odd? [E/O] ").lower().strip()
    if option_player == 'e':
        if (num_player + num_computer) % 2 == 0:
            print(f"You played {num_player}\nThe Computer played {num_computer}")
            print(f"The sum is {num_player + num_computer}. You WON!!!!")
        else:
            print(f"You played {num_player}\nThe Computer played {num_computer}")
            print(f"The sum is {num_player + num_computer}. You LOSE!!!!")
    elif option_player == 'o':
        if (num_player + num_computer) % 2 == 0:
            print(f"You played {num_player}\nThe Computer played {num_computer}")
            print(f"The sum is {num_player + num_computer}. You LOSE!!!!")
        else:
            print(f"You played {num_player}\nThe Computer played {num_computer}")
            print(f"The sum is {num_player + num_computer}. You WON!!!!")
