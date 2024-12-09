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
        print(f"{RED}Movimento fora do tabuleiro.{RESET}")
        print(f"{YELLOW}Sugestão: Consulte as regras no menu principal (Opção 5).{RESET}")
        return False
    if board["board"][x][y] != 0:
        print(f"{RED}Casa já ocupada.{RESET}")
        print(f"{YELLOW}Sugestão: Consulte as regras no menu principal (Opção 5).{RESET}")
        return False
    if not check_surroundings(x, y, player, board, player["number"]):
        print(f"{RED}Movimento inválido.{RESET}")
        print(f"{YELLOW}Sugestão: Consulte as regras no menu principal (Opção 5).{RESET}")
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
            if win_check(players):  # verifica se o jogo terminou
                print(f"\n{BLUE}Pontuação Final:{RESET}")
                for p in players:
                    print(f"{p['username']} -> {p['score']} pontos")
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
def delete_player(players):
    if not players:
        print(f"{RED}Não há jogadores registados para apagar.{RESET}")
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
    print(f"{BLUE}{rules}{RESET}")

def main():
    players = []
    print(CLEAR)
    while True:
        print(f"{BLUE}Menu:{RESET}")
        print(f"{GREEN}1{RESET} - Registar Jogador")
        print(f"{GREEN}2{RESET} - Iniciar Jogo")
        print(f"{GREEN}3{RESET} - Visualizar Pontuação")
        print(f"{GREEN}4{RESET} - Apagar Jogador")
        print(f"{GREEN}5{RESET} - Exibir Regras")
        print(f"{GREEN}6{RESET} - Sair")
        try:
            option = int(input(f"\n{GREEN}->\t{RESET}"))
            clear_screen()
            match option:
                case 1:
                    register_player(players)
                case 2:
                    if len(players) < 2:
                        print(f"{RED}Erro: É necessário pelo menos 2 jogadores registados para iniciar o jogo.{RESET}")
                    else:
                        start_game(players)
                case 3:
                    if not players:
                        print(f"{RED}Não há jogadores registados para mostrar pontuação.{RESET}")
                    else:
                        show_score(players)
                case 4:
                    delete_player(players)
                case 5:
                    show_rules()
                case 6:
                    print(f"{BLUE}Saindo do programa. Até logo!{RESET}")
                    exit()
                case _:
                    print(f"{RED}Opção inválida. Tente novamente.{RESET}")
        except ValueError:
            print(f"{RED}Entrada inválida. Por favor, insira um número correspondente às opções.{RESET}")
