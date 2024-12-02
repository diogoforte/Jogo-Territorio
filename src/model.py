def create_player(x, y, username, color, number):
    return {'x': x, 'y': y, 'username': username, 'color': color, 'number': number, 'score': 0}


def move_player(player, x, y):
    player['x'] = x
    player['y'] = y


def get_player_pos(player):
    return player['x'], player['y']


def create_board(height, length):
    return {'board': [[0 for _ in range(length)] for _ in range(height)], 'height': height, 'length': length}


def update_board(board, players):
    for player in players:
        x, y = get_player_pos(player)
        board['board'][x][y] = player['number']

# def check_win()