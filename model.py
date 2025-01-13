def create_player(x, y, username, color, number, score):
    return {
        'x': x, 
        'y': y, 
        'username': username, 
        'color': color, 
        'number': number, 
        'score': score, 
        'is_alive': True,
        'possible_plays': 0,
        'remaining_pieces': 21,
        'used_bonus': False,
        'territories_conquered': 0,
        'team': None
    }

def move_player(player, x, y):
    player['x'] = x
    player['y'] = y
    player['remaining_pieces'] -= 1
    player['territories_conquered'] += 1

def get_player_pos(player):
    return player['x'], player['y']

def create_board(height, length):
    return {'board': [[0 for _ in range(length)] for _ in range(height)], 'height': height, 'length': length}

def update_board(board, players):
    for player in players:
        x, y = get_player_pos(player)
        board['board'][x][y] = player['number']
