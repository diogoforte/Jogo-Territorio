from model import *
from view import *


def setup_players(height, length):
    players = []
    players_count = int(input("Define the number of players:\n\t"))
    while players_count > 4 or players_count < 1:
        print(f"{RED}Invalid number of Players{RESET}")
        players_count = int(input("Define the number of players:\n\t"))
    positions = [(0, 0), (height - 1, length - 1), (height - 1, 0), (0, length - 1)]
    player_colors = [RED, BLUE, YELLOW, GREEN]
    usernames = set()
    for i in range(players_count):
        while True:
            username = input(f"Define the name of player {i + 1}:\n\t")
            if not username:
                print(f"{RED}Invalid username{RESET}")
                continue
            elif username in usernames:
                print(f"{RED}Username already taken. Please choose a different name.{RESET}")
                continue
            usernames.add(username)
            break
        x, y = positions[i]
        players.append(create_player(x, y, username, player_colors[i], i + 1))
    return players


def move_check(x, y, player, board):
    if x < 0 or y < 0 or x >= board["height"] or y >= board["length"]:
        print_message(f"{RED}Out of bounds move.{RESET}")
        return False
    if board["board"][x][y] != 0:
        print_message(f"{RED}Square already taken.{RESET}")
        return False
    if x - 1 >= 0 and y - 1 >= 0 and board["board"][x - 1][y - 1] == player["number"]:
        return True
    if x - 1 >= 0 and y + 1 < board["length"] and board["board"][x - 1][y + 1] == player["number"]:
        return True
    if x + 1 < board["height"] and y - 1 >= 0 and board["board"][x + 1][y - 1] == player["number"]:
        return True
    if x + 1 < board["height"] and y + 1 < board["length"] and board["board"][x + 1][y + 1] == player["number"]:
        return True
    print_message(f"{RED}Non diagonal move.{RESET}")
    return False


def game_loop(players, board):
    while True:
        for player in players:
            update_board(board, players)
            print_board(board)
            print_message(f"{player['username']}'s turn")
            while True:
                y = int(input("Move x:\n\t")) - 1
                x = int(input("Move y:\n\t")) - 1
                if move_check(x, y, player, board):
                    break
            move_player(player, x, y)
            clear_screen()


def start_game():
    clear_screen()
    print_message("Welcome to the game")
    height = int(input("Define the board height:\n\t"))
    length = int(input("Define the board length:\n\t"))
    if height < 2 or length < 2:
        print_message(f"{RED}Invalid board size{RESET}")
        return
    board = create_board(height, length)
    players = setup_players(height, length)
    update_board(board, players)
    game_loop(players, board)
