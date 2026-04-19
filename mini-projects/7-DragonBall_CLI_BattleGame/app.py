import copy
import random
from time import sleep

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

CHARACTERS = [
    {
        "name": "Goku",
        "hp": 50,
        "ki": 30,
        "attack": 12,
        "special_name": "Kamehameha",
        "special_cost": 10,
        "special_damage": 22,
        "description": "Balanced fighter with a reliable special attack.",
    },
    {
        "name": "Vegeta",
        "hp": 45,
        "ki": 35,
        "attack": 13,
        "special_name": "Galick Gun",
        "special_cost": 12,
        "special_damage": 24,
        "description": "Aggressive and powerful, but burns more ki.",
    },
    {
        "name": "Gohan",
        "hp": 38,
        "ki": 40,
        "attack": 11,
        "special_name": "Masenko",
        "special_cost": 9,
        "special_damage": 21,
        "description": "Fast special attacker with plenty of ki.",
    },
    {
        "name": "Piccolo",
        "hp": 35,
        "ki": 25,
        "attack": 10,
        "special_name": "Special Beam Cannon",
        "special_cost": 8,
        "special_damage": 20,
        "description": "Technical fighter who can heal more than others.",
    },
    {
        "name": "Frieza",
        "hp": 40,
        "ki": 45,
        "attack": 14,
        "special_name": "Death Beam",
        "special_cost": 13,
        "special_damage": 25,
        "description": "High damage dealer with dangerous specials.",
    },
    {
        "name": "Cell",
        "hp": 39,
        "ki": 35,
        "attack": 12,
        "special_name": "Solar Kamehameha",
        "special_cost": 11,
        "special_damage": 23,
        "description": "Well-rounded fighter with strong pressure.",
    },
    {
        "name": "Majin Buu",
        "hp": 42,
        "ki": 20,
        "attack": 9,
        "special_name": "Candy Beam",
        "special_cost": 7,
        "special_damage": 18,
        "description": "Durable fighter who relies on staying alive.",
    },
    {
        "name": "Trunks",
        "hp": 30,
        "ki": 30,
        "attack": 12,
        "special_name": "Burning Attack",
        "special_cost": 9,
        "special_damage": 21,
        "description": "Glass cannon with explosive damage.",
    },
]


def setup_character(base_character):
    character = copy.deepcopy(base_character)
    character["max_hp"] = character["hp"]
    character["max_ki"] = character["ki"]
    character["defending"] = False
    return character


def create_bar(current, maximum, color):
    filled_slots = int((current / maximum) * 20) if maximum else 0
    empty_slots = 20 - filled_slots
    return f"[{color}]{'■' * filled_slots}[/][dim]{'■' * empty_slots}[/] {current}/{maximum}"


def show_title():
    console.print(
        Panel.fit(
            "[bold yellow]Dragon Ball CLI Battle Game[/]\n"
            "[white]Choose your fighter and survive the arena.[/]",
            border_style="bold blue",
        )
    )


def show_character_table():
    table = Table(title="Available Fighters", header_style="bold cyan")
    table.add_column("#", style="bold white", justify="center")
    table.add_column("Name", style="bold yellow")
    table.add_column("HP", justify="right")
    table.add_column("KI", justify="right")
    table.add_column("Attack", justify="right")
    table.add_column("Special")
    table.add_column("Style", style="white")

    for index, character in enumerate(CHARACTERS, start=1):
        table.add_row(
            str(index),
            character["name"],
            str(character["hp"]),
            str(character["ki"]),
            str(character["attack"]),
            character["special_name"],
            character["description"],
        )

    console.print(table)


def choose_character():
    while True:
        show_character_table()
        choice = console.input("[bold green]Choose your fighter by number:[/] ").strip()

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(CHARACTERS):
                return setup_character(CHARACTERS[index])

        console.print("[bold red]Invalid choice.[/] Please enter one of the listed numbers.\n")


def choose_enemy(player_name):
    available_characters = [char for char in CHARACTERS if char["name"] != player_name]
    return setup_character(random.choice(available_characters))


def show_battle_status(player, enemy):
    table = Table(title="Battle Status", header_style="bold magenta")
    table.add_column("Fighter", style="bold white")
    table.add_column("HP", style="green")
    table.add_column("KI", style="cyan")
    table.add_column("Attack", justify="right")
    table.add_column("Special")

    for fighter in (player, enemy):
        table.add_row(
            fighter["name"],
            create_bar(fighter["hp"], fighter["max_hp"], "green"),
            create_bar(fighter["ki"], fighter["max_ki"], "cyan"),
            str(fighter["attack"]),
            f"{fighter['special_name']} ({fighter['special_cost']} KI)",
        )

    console.print(table)


def basic_attack(attacker, defender):
    damage = attacker["attack"]
    if defender["defending"]:
        damage = max(1, damage - 4)
    defender["hp"] = max(0, defender["hp"] - damage)
    return f"{attacker['name']} attacks {defender['name']} for {damage} damage."


def special_attack(attacker, defender):
    if attacker["ki"] < attacker["special_cost"]:
        return None

    attacker["ki"] -= attacker["special_cost"]
    damage = attacker["special_damage"]
    if defender["defending"]:
        damage = max(2, damage - 5)
    defender["hp"] = max(0, defender["hp"] - damage)
    return (
        f"{attacker['name']} uses {attacker['special_name']} and deals "
        f"{damage} damage."
    )


def heal(character):
    heal_amount = 8 if character["name"] != "Piccolo" else 12
    old_hp = character["hp"]
    character["hp"] = min(character["max_hp"], character["hp"] + heal_amount)
    restored = character["hp"] - old_hp
    return f"{character['name']} recovers {restored} HP."


def charge_ki(character):
    gain = random.randint(6, 10)
    old_ki = character["ki"]
    character["ki"] = min(character["max_ki"], character["ki"] + gain)
    restored = character["ki"] - old_ki
    return f"{character['name']} focuses and restores {restored} KI."


def defend(character):
    character["defending"] = True
    return f"{character['name']} braces for the next attack."


def reset_defense(character):
    character["defending"] = False


def prompt_player_action(player):
    while True:
        console.print("\n[bold blue]Your turn[/]")
        console.print("1. Basic attack")
        console.print(
            f"2. {player['special_name']} "
            f"[dim](costs {player['special_cost']} KI)[/]"
        )
        console.print("3. Heal")
        console.print("4. Charge KI")
        console.print("5. Defend")

        choice = console.input("[bold green]Choose an action:[/] ").strip()
        valid_choices = {"1", "2", "3", "4", "5"}

        if choice in valid_choices:
            return choice

        console.print("[bold red]Invalid action.[/] Pick a number from 1 to 5.")


def player_turn(player, enemy):
    action = prompt_player_action(player)

    if action == "1":
        return basic_attack(player, enemy)
    if action == "2":
        result = special_attack(player, enemy)
        if result is None:
            console.print("[bold red]Not enough KI.[/] Choose a different action.")
            return player_turn(player, enemy)
        return result
    if action == "3":
        return heal(player)
    if action == "4":
        return charge_ki(player)
    return defend(player)


def enemy_turn(enemy, player):
    possible_actions = ["attack", "heal", "charge", "defend"]
    if enemy["ki"] >= enemy["special_cost"]:
        possible_actions.append("special")

    action = random.choice(possible_actions)

    if action == "attack":
        return basic_attack(enemy, player)
    if action == "special":
        return special_attack(enemy, player)
    if action == "heal":
        return heal(enemy)
    if action == "charge":
        return charge_ki(enemy)
    return defend(enemy)


def announce_turn_result(message, style):
    console.print(Panel(message, border_style=style))


def ask_to_play_again():
    answer = console.input("\n[bold green]Play again? (y/n):[/] ").strip().lower()
    return answer == "y"


def play_game():
    show_title()

    while True:
        player = choose_character()
        enemy = choose_enemy(player["name"])

        console.print(
            Panel.fit(
                f"[bold green]You chose {player['name']}[/]\n"
                f"[bold red]Enemy fighter: {enemy['name']}[/]",
                border_style="yellow",
            )
        )

        while player["hp"] > 0 and enemy["hp"] > 0:
            reset_defense(player)
            reset_defense(enemy)

            show_battle_status(player, enemy)
            announce_turn_result(player_turn(player, enemy), "blue")
            if enemy["hp"] <= 0:
                break

            sleep(1)
            announce_turn_result(enemy_turn(enemy, player), "red")
            sleep(1)

        show_battle_status(player, enemy)
        if player["hp"] > 0:
            console.print(Panel.fit("[bold green]You win![/]", border_style="green"))
        else:
            console.print(Panel.fit("[bold red]You lose![/]", border_style="red"))

        if not ask_to_play_again():
            console.print("\n[bold cyan]Thanks for playing![/]")
            break


play_game()
