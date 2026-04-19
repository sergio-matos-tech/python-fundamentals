import random
import copy
from time import sleep

characters = [
    {"name": "Goku", "hp": 50, "ki": 30, "attack": 12},
    {"name": "Vegeta", "hp": 45, "ki": 35, "attack": 13},
    {"name": "Gohan", "hp": 38, "ki": 40, "attack": 11},
    {"name": "Piccolo", "hp": 35, "ki": 25, "attack": 10},
    {"name": "Frieza", "hp": 40, "ki": 45, "attack": 14},
    {"name": "Cell", "hp": 39, "ki": 35, "attack": 12},
    {"name": "Majin Buu", "hp": 42, "ki": 20, "attack": 9},
    {"name": "Trunks", "hp": 30, "ki": 30, "attack": 12}
]


def get_character_by_name(characters, name):
    for char in characters:
        if char["name"].lower() == name.lower():
            return char
    return None


def attack(attacker, defender):
    damage = attacker['attack']
    defender['hp'] -= damage
    print(f"{attacker['name']} attacks {defender['name']} for {damage} damage!")


def print_all_characters(characters):
    print("\n--- AVAILABLE CHARACTERS ---")
    for character in characters:
        for key, value in character.items():
            print(f"{key}: {value}", end=" | ")
        print()
    print()


def print_character(character):
    if character is None:
        print("Character not found.")
        return

    for key, value in character.items():
        print(f"{key}: {value}", end=" | ")
    print()


def ia_character(characters):
    return copy.deepcopy(random.choice(characters))


def chance_of_enemy_attack():
    return random.random()


def enemy_attacks():
    return chance_of_enemy_attack() < 0.5  


def play_game():
    print_all_characters(characters)

    player_character_name = input('Choose your character: ')
    player_character = get_character_by_name(characters, player_character_name)

    if player_character is None:
        print("Invalid character.")
        return

    player_character = copy.deepcopy(player_character)
    computer_character = ia_character(characters)

    print(f"\nYou chose: {player_character['name']}")
    print(f"Enemy chose: {computer_character['name']}")

    game_over = False

    while not game_over:
        print("\n--- CURRENT STATUS ---")
        print("Player:")
        print_character(player_character)
        print("Enemy:")
        print_character(computer_character)

        if enemy_attacks():
            print("\nEnemy attacks!")
            attack(computer_character, player_character)
        else:
            print("\nYou attack!")
            attack(player_character, computer_character)

        if player_character["hp"] <= 0 or computer_character["hp"] <= 0:
            game_over = True
            
        sleep(4)

    print("\n--- GAME OVER ---")
    if player_character["hp"] > 0:
        print("You win!")
    else:
        print("You lose!")


play_game()