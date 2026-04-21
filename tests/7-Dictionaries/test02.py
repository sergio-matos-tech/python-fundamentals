game_properties = ["current_score", "high_score", "number_of_lives", "items_in_inventory", "power_ups", "ammo", "enemies_on_screen", "enemy_kills", "enemy_kill_streaks", "minutes_played", "notifications", "achievements"] 

initial_game_state = dict.fromkeys(game_properties, 0)


inventory = {'croissant': 19, 'bagel': 4, 'muffin': 8, 'cake': 1}

stock_list = inventory.copy()
print(stock_list)

stock_list['Cookie'] = 18
print(stock_list)

stock_list.pop('cake')
print(stock_list)


