from model import *
from view import *


def setup_players(players, height, length):
    active_players = []
    if len(players) < 2:
        print(f"{RED}Numero insuficiente de jogadores registados{RESET}")
        return
    players_count = int(input("Defina o numero de jogadores:\n\t"))
    while players_count > 4 or players_count < 1:
        print(f"{RED}Numero invalido de jogadores{RESET}")
        players_count = int(input("Defina o numero de jogadores:\n\t"))
    positions = [(0, 0), (height - 1, length - 1), (height - 1, 0), (0, length - 1)]
    player_colors = [RED, BLUE, YELLOW, GREEN]
    print("Escolha os jogadores:")
    for i, player in enumerate(players):
        print(f"{GREEN}{i + 1}\t{player['username']}{RESET}")
    for j in range(players_count):
        while True:
            selected_index = int(input(f"Escolha o jogador {j + 1}:\n\t")) - 1
            if selected_index < 0 or selected_index >= len(players):
                print(f"{RED}Indice invalido. Tente novamente.{RESET}")
                continue
            selected_player = players[selected_index]
            break
        x, y = positions[j]
        active_players.append(create_player(x, y, selected_player["username"], player_colors[j], j + 1))
    return active_players


def win_check(board, players):
    pass


def check_bounds(x, y, board):
    return 0 <= x < board["height"] and 0 <= y < board["length"]


def move_check(x, y, player, board):
    if not check_bounds(x, y, board):
        print_message(f"{RED}Movimento fora do tabuleiro.{RESET}")
        return False
    if board["board"][x][y] != 0:
        print_message(f"{RED}Square already taken.{RESET}")
        return False
    if check_bounds(x - 1, y - 1, board) and board["board"][x - 1][y - 1] == player["number"]:
        return True
    if check_bounds(x, y - 1, board) and board["board"][x][y - 1] == player["number"]:
        return True
    if check_bounds(x + 1, y - 1, board) and board["board"][x + 1][y - 1] == player["number"]:
        return True
    if check_bounds(x + 1, y + 1, board) and board["board"][x + 1][y + 1] == player["number"]:
        return True
    if check_bounds(x, y + 1, board) and board["board"][x][y + 1] == player["number"]:
        return True
    if check_bounds(x - 1, y + 1, board) and board["board"][x - 1][y + 1] == player["number"]:
        return True
    if check_bounds(x - 1, y, board) and board["board"][x - 1][y] == player["number"]:
        return True
    if check_bounds(x + 1, y, board) and board["board"][x + 1][y] == player["number"]:
        return True
    print_message(f"{RED}Movimento invalido.{RESET}")
    return False


def game_loop(players, board):
    while True:
        for player in players:
            update_board(board, players)
            print_board(board)
            print_message(f"Turno do jogador {player['username']}")
            while True:
                y = int(input("Movimento x:\n\t")) - 1
                x = int(input("Movimento y:\n\t")) - 1
                if move_check(x, y, player, board):
                    break
            move_player(player, x, y)
            clear_screen()


def start_game(players):
    height = int(input("Defina a altura do tabuleiro:\n\t"))
    length = int(input("Defina a largura do tabuleiro:\n\t"))
    if height < 2 or length < 2:
        print_message(f"{RED}Tamanho invalido{RESET}")
        return
    board = create_board(height, length)
    players = setup_players(players, height, length)
    if not players:
        return
    print(CLEAR)
    update_board(board, players)
    game_loop(players, board)


def username_check(username, players):
    if not username:
        print(f"{RED}Nome invalido{RESET}")
        return False
    for player in players:
        if username == player["username"]:
            print(f"{RED}Nome ja existente{RESET}")
            return False
    return True


def register_player(players):
    while True:
        username = input(f"Defina o nome do jogador:\n\t")
        if username_check(username, players):
            players.append(create_player(0, 0, username, 0, 0))
            break


def show_score(players):
    for player in players:
        print(f"{player['username']} - {player['score']}")


def main():
    clear_screen()
    players = []
    while True:
        match int(input(
            f"{BLUE}Menu:{RESET}\n{GREEN}1{RESET}\tRegistar Jogador\n{GREEN}2{RESET}\tIniciar Jogo\n{GREEN}3{RESET}\tVisualizar Pontoacao\n{GREEN}4{RESET}\tSair\n\n")):
            case 1:
                register_player(players)
            case 2:
                start_game(players)
            case 3:
                show_score(players)
            case 4:
                exit()
            case _:
                print_message(f"{RED}Opcao invalida{RESET}")
                continue
