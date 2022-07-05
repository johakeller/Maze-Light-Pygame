level_0 = {
    'walls': '../levels/0/level_0_walls.csv',
    'coins': '../levels/0/level_0_coins.csv',
    'flowers': '../levels/0/level_0_flowers.csv',
    'enemies': '../levels/0/level_0_enemies.csv',
    'player': '../levels/0/level_0_player.csv',
    'floor': '../graphics/terrain/floor_0.png',
    'unlock': 1}

level_1 = {
    'walls': '../levels/1/level_1_walls.csv',
    'coins': '../levels/1/level_1_coins.csv',
    'flowers': '../levels/1/level_1_flowers.csv',
    'enemies': '../levels/1/level_1_enemies.csv',
    'player': '../levels/1/level_1_player.csv',
    'floor': '../graphics/terrain/floor_1.png',
    'unlock': 2}

level_2 = {
    'walls': '../levels/2/level_2_walls.csv',
    'coins': '../levels/2/level_2_coins.csv',
    'flowers': '../levels/2/level_2_flowers.csv',
    'enemies': '../levels/2/level_2_enemies.csv',
    'player': '../levels/2/level_2_player.csv',
    'floor': '../graphics/terrain/floor_2.png',
    'unlock': 2}

levels = {
    0: level_0,
    1: level_1,
    2: level_2}

menu_dict = {'game_over': ['Continue'], 'win': ['Continue'],
             'paused': ['Resume'], 'start': ['Training Level', 'Level 1', 'Level 2', 'Exit']}
