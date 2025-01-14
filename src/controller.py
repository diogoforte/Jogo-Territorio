from model import *
from view import *
import json
import random


def setup_players(players, height, length):
    active_players = []
    while True:
        players_count = int(input(f"{BLUE}Defina o numero de jogadores:\n{GREEN}->\t{RESET}"))
        if 1 <= players_count <= min(len(players), 4):
            break
        print(f"{RED}Numero de jogadores insuficiente{RESET}")
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
        active_players.append(
            create_player(x, y, selected_player["username"], player_colors[j], j + 1, selected_player["score"]))
    print(CLEAR)
    return active_players


def check_bounds(x, y, board):
    return 0 <= x < board["height"] and 0 <= y < board["length"]


def check_surroundings(x, y, board, number):
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
        print(f"{RED}Movimento fora do tabuleiro.{RESET}")
        print(f"{YELLOW}Sugestão: Consulte as regras no menu principal (Opção 5).{RESET}")
        return False
    if board["board"][x][y] != 0:
        print(f"{RED}Casa já ocupada.{RESET}")
        print(f"{YELLOW}Sugestão: Consulte as regras no menu principal (Opção 5).{RESET}")
        return False
    if not check_surroundings(x, y, board, player["number"]):
        print(f"{RED}Movimento inválido.{RESET}")
        print(f"{YELLOW}Sugestão: Consulte as regras no menu principal (Opção 5).{RESET}")
        return False
    return True

def possible_plays_check(board, player):
    for i in range(board['height']):
        for j in range(board['length']):
            if board['board'][i][j] == player['number']:
                if check_surroundings(i, j, board, 0):
                    return True
    return False

def check_full_board(board):
    for i in range(board['height']):
        for j in range(board['length']):
            if board['board'][i][j] == 0:
                return False
    return True
def check_pieces(players):
    for player in players:
        if player['pieces'] > 0:
            return False
    return True

def game_loop(players, board):
    print_board(board)
    while True:
        for player in players:
            moves = 1
            while moves:
                clear_screen()
                update_board(board, players)
                print_board(board)
                print(f"{BLUE}Turno do jogador {player['color']}{player['username']} {RESET}({player['number']})")
                if not possible_plays_check(board, player):
                    print(
                        f"{BLUE}O jogador {player['color']}{player['username']} {RESET}({player['number']}) {BLUE}nao tem jogadas possiveis. Passando a vez.")
                    input(f"{BLUE}Pressione Enter para continuar{RESET}")
                    clear_screen()
                    break
                while True:
                    y = int(input(f"{BLUE}Movimento x:\n{GREEN}->\t{RESET}")) - 1
                    x = int(input(f"{BLUE}Movimento y:\n{GREEN}->\t{RESET}")) - 1
                    if move_check(x, y, player, board):
                        break
                moves -= 1
                move_player(player, x, y)
                player['pieces'] -= 1
                if random.randint(0, 10) <= 5:
                    input(f"{BLUE}O jogador {player['color']}{player['username']} {RESET}({player['number']}) {BLUE}recebeu um bónus e ganhou uma jogada extra.{RESET}")
                    moves =+ 1
        if check_full_board(board) or check_pieces(players):
            break

def win_check(players):
    min_pieces = 22
    winner = None
    draw = False
    for player in players:
        if player['pieces'] < min_pieces:
            min_pieces = player['pieces']
            winner = player
            draw = False
        elif player['pieces'] == min_pieces:
            draw = True
    if draw:
        print(f"{BLUE}O jogo terminou em empate!{RESET}")
    elif winner:
        winner['score'] = 1
        print(f"{CLEAR}{winner['color']}{winner['username']}{RESET} ({winner['number']}){BLUE} venceu 🎉\n{RESET}")

def start_game(players):
    if len(players) < 2:
        print(CLEAR)
        print(f"{RED}Erro: É necessário pelo menos 2 jogadores registados para iniciar o jogo.{RESET}")
        input(f"{BLUE}Pressione Enter para continuar{RESET}")
        return
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
    win_check(active_players)
    print_board(board)
    print(f"{BLUE}Pontuação atual:{RESET}")
    for player in players:
        for active_player in active_players:
            if player['username'] == active_player['username'] and active_player['score'] == 1:
                player['score'] += 1
    for player in players:
        print(f"    {player['username']} -> {player['score']} pontos")
    input(f"{BLUE}Pressione Enter para continuar{RESET}")


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
            players.append(create_player(0, 0, username, 0, 0, 0))
            break


def delete_player(players):
    if not players:
        print(f"{RED}Não há jogadores registados para apagar.{RESET}")
        input(f"{BLUE}Pressione Enter para continuar{RESET}")
        return

    print(f"{BLUE}Jogadores registados:{RESET}")
    for i, player in enumerate(players):
        print(f"{GREEN}{i + 1}{RESET} - {player['username']}")

    while True:
        try:
            index = int(input(f"{BLUE}Escolha o número do jogador a remover:\n{GREEN}->\t{RESET}")) - 1
            if 0 <= index < len(players):
                removed_player = players.pop(index)
                print(f"{GREEN}Jogador {removed_player['username']} removido com sucesso.{RESET}")
                return
            else:
                print(f"{RED}Número inválido. Tente novamente.{RESET}")
        except ValueError:
            print(f"{RED}Entrada inválida. Por favor, insira um número.{RESET}")


def show_score(players):
    if not players:
        print(CLEAR)
        print(f"{RED}Não há jogadores registados para mostrar pontuação.{RESET}")
        input(f"{BLUE}Pressione Enter para continuar{RESET}")
        return
    print(f"{BLUE}Pontuacao:{RESET}")
    for player in players:
        print(f"{player['username']}\t{GREEN}->\t{RESET}{player['score']}{RESET}")
    input(f"{BLUE}Pressione Enter para continuar{RESET}")


def show_rules():
    rules = """
    REGRAS DO JOGO TERRITÓRIO:
    1. Cada jogador escolhe uma cor e recebe um conjunto de peças.
    2. A primeira peça deve ser colocada no canto designado do tabuleiro.
    3. Cada nova peça deve tocar outra peça da mesma cor pelos cantos.
    4. Jogadores podem conquistar territórios adjacentes, desde que respeitem as regras.
    5. Quando não for possível fazer jogadas, o jogador passa a vez.
    6. O jogo termina quando todos os jogadores estão bloqueados.
    7. O jogador com menos quadrados restantes vence.
    8. Existem bónus que permitem conquistar mais territórios em uma jogada.
    """
    print(f"{RESET}{rules}")
    input(f"{BLUE}Pressione Enter para continuar{RESET}")

def save(players):
    with open('save.json', 'r+') as json_file:
        try:
            saved_players = json.load(json_file)
            for player in players:
                if player not in saved_players:
                    saved_players.append(player)
            json_file.seek(0)
            json_file.truncate()
            json.dump(saved_players, json_file, indent=4)
        except Exception:
            json.dump(players, json_file, indent=4)
    print(f"{GREEN}Jogo salvo com sucesso!{RESET}")
    input(f"{BLUE}Pressione Enter para continuar{RESET}")

def load():
    try:
        with open('save.json', 'r') as json_file:
            players = json.load(json_file)
            if not load_username_check(players):
                raise Exception("Nome de jogador repetido")
            print(f"{GREEN}Jogo carregado com sucesso!{RESET}")
            input(f"{BLUE}Pressione Enter para continuar{RESET}")
            return players
    except Exception as exception:
        print(f"{RED}Não foi possível carregar o jogo.\n{GREEN}->{RESET}\"{exception}\"")
        input(f"{BLUE}Pressione Enter para continuar{RESET}")
        return []

def load_username_check(players):
    seen_usernames = set()
    for player in players:
        if not player['username'] or player['username'] in seen_usernames:
            return False
        seen_usernames.add(player['username'])
    return True


def main():
    players = []
    while True:
        print(CLEAR)
        print(f"{BLUE}Menu:{RESET}")
        print(f"{GREEN}1{RESET} - Registar Jogador")
        print(f"{GREEN}2{RESET} - Iniciar Jogo")
        print(f"{GREEN}3{RESET} - Visualizar Pontuação")
        print(f"{GREEN}4{RESET} - Apagar Jogador")
        print(f"{GREEN}5{RESET} - Exibir Regras")
        print(f"{GREEN}6{RESET} - Salvar Pontuaçoes")
        print(f"{GREEN}7{RESET} - Carregar Pontuaçoes")
        print(f"{GREEN}8{RESET} - Sair")
        try:
            option = int(input(f"\n{GREEN}->\t{RESET}"))
            clear_screen()
            match option:
                case 1:
                    register_player(players)
                case 2:
                    start_game(players)
                case 3:
                    show_score(players)
                case 4:
                    delete_player(players)
                case 5:
                    show_rules()
                case 6:
                    save(players)
                case 7:
                    players = load()
                case 8:
                    print(f"{BLUE}Saindo do programa. Até logo!{RESET}")
                    break
                case _:
                    print(f"{RED}Opção inválida. Tente novamente.{RESET}")
        except Exception as exception:
            print(CLEAR)
            print(f"{RED}Exceção encontrada.\n{GREEN}->{RESET}\"{exception}\"")
            input(f"{BLUE}Pressione Enter para continuar{RESET}")
