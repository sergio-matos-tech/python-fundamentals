rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''


import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

choices = [rock, paper, scissors]


def print_choices(player_choice, computer_choice):
    print("\nThe player's choice was:")
    print(choices[player_choice - 1])
    print("The computer's choice was:")
    print(choices[computer_choice - 1])


def define_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return 'draw'
    elif player_choice == 1:
        if computer_choice == 3:
            return 'player'
        elif computer_choice == 2:
            return 'computer'
    elif player_choice == 2:
        if computer_choice == 1:
            return 'player'
        elif computer_choice == 3:
            return 'computer'

def print_result(result):
    if result == "draw":
        print("That's a DRAW!!!")
    elif result == "player":
        print("YOU WON!!!")
    else:
        print("YOU LOSE!!!")
        
        
def print_scores(player_score, computer_score):
    print(f"| SCORES |\n-> Player = {player_score}\n-> Computer {computer_score}")


def main():
    print("\n=============== ROCK PAPER SCISSORS GAME ===============\n")

    player_score = 0
    computer_score = 0

    while True:
        print("\nMake your bet!")
        print("[1] for ROCK\n[2] for PAPER\n[3] for SCISSORS\n")

        player_choice = int(input("Enter your choice: "))
        computer_choice = random.randint(1, 3)

        print_choices(player_choice, computer_choice)

        result = define_winner(player_choice, computer_choice)
        print_result(result)

        if result == "player":
            player_score += 1
        elif result == "computer":
            computer_score += 1

        print_scores(player_score, computer_score)

        stop_game = input("Enter [stop] to stop the game or any other key to continue: ").lower().strip()
        if stop_game == "stop":
            break


if __name__ == "__main__":
    main()