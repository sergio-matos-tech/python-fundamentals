players_list = list()

while True:
    player_name = str(input("Player name: ")).strip()
    amount_games = int(input("Amount of games: "))
    gols = list()
    player = dict()
    total_gols = 0
    if amount_games > 0:
        for c in range(amount_games):
            gol = int(input(f"    Amount of gols in match {c + 1}: "))
            if gol >= 0:
                gols.append(gol)
                total_gols = sum(gols)
        player['name'] = player_name
        player['amount_games'] = amount_games
        player['gols'] = gols[:]
        player['total_gols'] = total_gols
    players_list.append(player)
    option = input("Continue: [Y/N] ").lower().strip()
    if option == 'n':
        break

print("-" * 60)
cont = 0
for player in players_list:
    print(f"   {cont} ->  {player} ")
    cont += 1
print("-" * 60)

lenght_playerslist = len(players_list)
while True:
    option_player = int(input(f"Which player do you want to show? Enter the code? (0 -> {lenght_playerslist - 1}) "
                              f"[x < 0 to stop] "))
    if 0 <= option_player < lenght_playerslist:
        print(f"{players_list[option_player]}")
    else:
        break
