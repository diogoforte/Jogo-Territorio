def create_player(username, color, number, score):
    return {'username': username, 'color': color, 'number': number, 'score': score, 'pieces': 20}


def move_player(player, x, y):
    player['x'] = x
    player['y'] = y

def create_board(height, length):
    return {'board': [[0 for _ in range(length)] for _ in range(height)], 'height': height, 'length': length}


def update_board(board, player, x, y):
        board['board'][x][y] = player['number']
