from model import *
from view import *


def setup_players(players, height, length):
    active_players = []
    while True:
        players_count = int(input(f"{BLUE}Defina o numero de jogadores:\n{GREEN}->\t{RESET}"))
        if players_count > len(players) or players_count < 1 or players_count > 4 or len(players) < 2:
            print(f"{RED}Numero de jogadores insuficiente{RESET}")
            continue
        break
    positions = [(0, 0), (height - 1, length - 1), (height - 1, 0), (0, length - 1)]
    player_colors = [RED, BLUE, YELLOW, GREEN]
    print(f"{BLUE}Escolha os jogadores:{RESET}")
    for i, player in enumerate(players):
        print(f"{GREEN}{i + 1}{RESET}\t{player['username']}")
    for j in range(players_count):
        while True:
            selected_index = int(input(f"{BLUE}Escolha o jogador {j + 1}:\n{GREEN}->\t{RESET}")) - 1
            if selected_index < 0 or selected_index >= len(players):
                print(f"{RED}Indice invalido. Tente novamente.{RESET}")
                continue
            break
        selected_player = players[selected_index]
        x, y = positions[j]
        active_players.append(create_player(x, y, selected_player["username"], player_colors[j], j + 1))
    print(CLEAR)
    return active_players


def possible_plays_check(board, players):
    for player in players:
        player['possible_plays'] = 0
    for i in range(board['height']):
        for j in range(board['length']):
            if board['board'][i][j] == 0:
                for player in players:
                    if check_surroundings(i, j, player, board, player['number']):
                        player['possible_plays'] += 1
    for player in players:
        if player['possible_plays'] == 1:
            player['is_alive'] = False
            print(f"Jogador {player['username']} eliminado")


def check_bounds(x, y, board):
    return 0 <= x < board["height"] and 0 <= y < board["length"]


def check_surroundings(x, y, player, board, number):
    if check_bounds(x - 1, y - 1, board) and board["board"][x - 1][y - 1] == number:
        return True
    if check_bounds(x, y - 1, board) and board["board"][x][y - 1] == number:
        return True
    if check_bounds(x + 1, y - 1, board) and board["board"][x + 1][y - 1] == number:
        return True
    if check_bounds(x + 1, y + 1, board) and board["board"][x + 1][y + 1] == number:
        return True
    if check_bounds(x, y + 1, board) and board["board"][x][y + 1] == number:
        return True
    if check_bounds(x - 1, y + 1, board) and board["board"][x - 1][y + 1] == number:
        return True
    if check_bounds(x - 1, y, board) and board["board"][x - 1][y] == number:
        return True
    if check_bounds(x + 1, y, board) and board["board"][x + 1][y] == number:
        return True
    return False


def move_check(x, y, player, board):
    if not check_bounds(x, y, board):
        print(f"{RED}Movimento fora do tabuleiro{RESET}")
        return False
    if board["board"][x][y] != 0:
        print(f"{RED}Casa ja ocupada{RESET}")
        return False
    if not check_surroundings(x, y, player, board, player["number"]):
        print(f"{RED}Movimento invalido{RESET}")
        return False
    return True


def win_check(players):
    i = 0
    for player in players:
        if player['is_alive']:
            i = i + 1
    if i == 0:
        print(f"{RED}Empate!{RESET}")
        return True
    if i == 1:
        for player in players:
            if player['is_alive']:
                print(
                    f"{CLEAR}{player['color']}{player['username']}{RESET} ({player['number']}){BLUE}  venceu 🎉{RESET}")
                player['score'] += 1
                return True
    return False


def game_loop(players, board):
    while True:
        for player in players:
            possible_plays_check(board, players)
            if win_check(players):
                return
            update_board(board, players)
            print_board(board)
            print(f"{BLUE}Turno do jogador {player['color']}{player['username']} {RESET}({player['number']})")
            while True:
                y = int(input(f"{BLUE}Movimento x:\n{GREEN}->\t{RESET}")) - 1
                x = int(input(f"{BLUE}Movimento y:\n{GREEN}->\t{RESET}")) - 1
                if move_check(x, y, player, board):
                    break
            move_player(player, x, y)
            clear_screen()


def start_game(players):
    height = int(input(f"{BLUE}Defina a altura do tabuleiro:\n{GREEN}->\t{RESET}"))
    length = int(input(f"{BLUE}Defina a largura do tabuleiro:\n{GREEN}->\t{RESET}"))
    if height < 2 or length < 2:
        print(f"{RED}Tamanho invalido{RESET}")
        return
    board = create_board(height, length)
    active_players = setup_players(players, height, length)
    if not active_players:
        print(f"{RED}Numero insuficiente de jogadores registados{RESET}")
        return
    update_board(board, active_players)
    game_loop(active_players, board)
    for player in players:
        for active_player in active_players:
            if player['username'] == active_player['username']:
                player['score'] += active_player['score']


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
        username = input(f"{BLUE}Defina o nome do jogador:\n{GREEN}->\t{RESET}")
        if username_check(username, players):
            players.append(create_player(0, 0, username, 0, 0))
            break


def show_score(players):
    print(f"{BLUE}Pontuacao:{RESET}")
    for player in players:
        print(f"{player['username']}\t{GREEN}->\t{RESET}{player['score']}{RESET}")
    input(f"{BLUE}Pressione Enter para continuar{RESET}")


def main():
    players = []
    print(CLEAR)
    while True:
        match int(input(
            f"{BLUE}Menu:{RESET}\n{GREEN}1{RESET}\tRegistar Jogador\n{GREEN}2{RESET}\tIniciar Jogo\n{GREEN}3{RESET}\tVisualizar Pontoacao\n{GREEN}4{RESET}\tSair\n\n{GREEN}->\t{RESET}")):
            case 1:
                register_player(players)
                print(CLEAR)
            case 2:
                start_game(players)
            case 3:
                show_score(players)
                print(CLEAR)
            case 4:
                exit()
            case _:
                print(f"{RED}Opcao invalida{RESET}")
                continue
