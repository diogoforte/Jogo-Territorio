def create_player(x, y, username, color, number, score):
    return {'x': x, 'y': y, 'username': username, 'color': color, 'number': number, 'score': score, 'pieces': 21}


def move_player(player, x, y):
    player['x'] = x
    player['y'] = y

def create_board(height, length):
    return {'board': [[0 for _ in range(length)] for _ in range(height)], 'height': height, 'length': length}


def update_board(board, players):
    for player in players:
        board['board'][player['x']][player['y']] = player['number']