from model import *
from view import *
import json
import random
import os


def add_player_to_board(board, active_players, positions, player, color, number):
    x, y = positions.pop(0)
    new_player = create_player(player["username"], color, number, 0)
    update_board(board, new_player, x, y)
    active_players.append(new_player)


def print_player_list(players):
    print(f"{BLUE}Escolha os jogadores:{RESET}")
    for i, player in enumerate(players):
        print(f"{GREEN}{i + 1}{RESET} - {player['username']}")


def select_player(players, chosen_players=None):
    while True:
        try:
            selected_index = int(input(f"{BLUE}Escolha um jogador:\n{GREEN}->\t{RESET}")) - 1
            if selected_index < 0 or selected_index >= len(players):
                print(f"{RED}Índice inválido. Tente novamente.{RESET}")
                continue
            selected_player = players[selected_index]
            if chosen_players is not None and selected_player['username'] in chosen_players:
                print(f"{RED}Jogador já foi escolhido. Escolha outro.{RESET}")
                continue

            return selected_player
        except ValueError:
            print(f"{RED}Entrada inválida. Por favor, insira um número.{RESET}")


def setup_players(board, players):
    active_players = []
    while True:
        players_count = int(input(f"{BLUE}Defina o número de jogadores:\n{GREEN}->\t{RESET}"))
        if 1 <= players_count <= min(len(players), 4):
            break
        print(f"{RED}Número de jogadores insuficiente.{RESET}")
    positions = [(0, 0), (board['height'] - 1, board['length'] - 1), (board['height'] - 1, 0), (0, board['length'] - 1)]
    player_colors = [RED, BLUE, YELLOW, GREEN]
    print_player_list(players)
    for j in range(players_count):
        selected_player = select_player(players)
        add_player_to_board(board, active_players, positions, selected_player, player_colors[j], j + 1)
    return active_players


def setup_players_duplas(board, players):
    active_players = []
    team_colors = [(RED, BLUE), (YELLOW, GREEN)]
    positions = [(0, 0), (board['height'] - 1, board['length'] - 1), (board['height'] - 1, 0), (0, board['length'] - 1)]
    teams = [[], []]
    chosen_players = set()
    print_player_list(players)
    for team_index, (color1, color2) in enumerate(team_colors):
        print(f"{MAGENTA}Configurar equipa {team_index + 1}:{RESET}")
        for j in range(2):
            selected_player = select_player(players, chosen_players)
            chosen_players.add(selected_player['username'])
            teams[team_index].append(selected_player['username'])
            add_player_to_board(
                board, active_players, positions, selected_player, color1 if j == 0 else color2, len(active_players) + 1
            )
    return active_players, teams


def check_surroundings(x, y, board, number):
    return any(
        0 <= x + dx < board["height"] and 0 <= y + dy < board["length"] and board['board'][x + dx][y + dy] == number
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1])


def move_check(x, y, player, board):
    if not (0 <= x < board["height"] and 0 <= y < board["length"]):
        print(f"{RED}Movimento fora do tabuleiro.{RESET}")
    elif board["board"][x][y] != 0:
        print(f"{RED}Casa já ocupada.{RESET}")
    elif not check_surroundings(x, y, board, player["number"]):
        print(f"{RED}Movimento inválido.{RESET}")
    else:
        return True
    print(f"{YELLOW}Sugestão: Consulte as regras no menu principal (Opção 5).{RESET}")
    return False


def possible_plays_check(board, player):
    for i in range(board['height']):
        for j in range(board['length']):
            if board['board'][i][j] == player['number']:
                if check_surroundings(i, j, board, 0):
                    return True
    return False


def check_if_game_ended(players, board):
    if (all(player['pieces'] == 0 for player in players) or
            not any(board['board'][i][j] == 0 for i in range(board['height']) for j in range(board['length']))):
        return True
    return False


def play_turn(player, board):
    moves = 1
    while moves > 0:
        print(CLEAR)
        print_board(board)
        print(f"{BLUE}Turno do jogador {player['color']}{player['username']} {RESET}({player['number']})")
        while True:
            try:
                y = int(input(f"{BLUE}Movimento x:\n{GREEN}->\t{RESET}")) - 1
                x = int(input(f"{BLUE}Movimento y:\n{GREEN}->\t{RESET}")) - 1
                if move_check(x, y, player, board):
                    break
            except ValueError:
                print(f"{RED}Entrada inválida. Tente novamente.{RESET}")
        update_board(board, player, x, y)
        player["pieces"] -= 1
        moves -= 1
        if random.randint(0, 10) <= 2:
            print(f"{BLUE}Bónus! {player['username']} ganhou uma jogada extra!{RESET}")
            moves += 1
            input(f"{BLUE}Pressione Enter para continuar{RESET}")


def check_player_plays(player, board):
    if not possible_plays_check(board, player):
        input(
            f"{BLUE}O jogador {player['color']}{player['username']} {RESET}({player['number']}) "
            f"{BLUE}não tem jogadas possíveis. Passando a vez.\n{BLUE}Pressione Enter para continuar{RESET}"
        )
        return False
    return True


def game_loop(players, board):
    while True:
        for player in players:
            if not check_player_plays(player, board):
                continue
            play_turn(player, board)
        if check_if_game_ended(players, board):
            break


def game_loop_duplas(players, board, teams):
    print_board(board)
    while True:
        for team_index, team in enumerate(teams):
            print(f"{BLUE}Turno da equipa {team_index + 1}:{RESET}")
            for player in [p for p in players if p["username"] in team]:
                if not check_player_plays(player, board):
                    continue
                play_turn(player, board)
        if check_if_game_ended(players, board):
            break


def win_check_duplas(players, teams):
    team_totals = [0, 0]
    for i, team in enumerate(teams):
        team_totals[i] = sum(player['pieces'] for player in players if player['username'] in team)
    if team_totals[0] < team_totals[1]:
        print(f"{CLEAR}{RED}Equipa 1 venceu 🎉{RESET}")
        for player in players:
            if player['username'] in teams[0]:
                player['score'] += 1
    elif team_totals[0] > team_totals[1]:
        print(f"{CLEAR}{BLUE}Equipa 2 venceu 🎉{RESET}")
        for player in players:
            if player['username'] in teams[1]:
                player['score'] += 1
    else:
        print(f"{CLEAR}{YELLOW}O jogo terminou em empate entre as equipas!{RESET}")
    


def win_check(players):
    min_pieces = min(player['pieces'] for player in players)
    winners = [player for player in players if player['pieces'] == min_pieces]
    if len(winners) > 1:
        print(f"{BLUE}O jogo terminou em empate!{RESET}")
    else:
        winner = winners[0]
        winner['score'] = 1
        print(f"{CLEAR}{winner['color']}{winner['username']}{RESET} ({winner['number']}){BLUE} venceu 🎉\n{RESET}")


def start_game(players, mode):
    if len(players) < 2:
        print(CLEAR)
        print(f"{RED}Erro: É necessário pelo menos 2 jogadores registados para iniciar o jogo.{RESET}")
        input(f"{BLUE}Pressione Enter para continuar{RESET}")
        return
    if not mode and len(players) < 4:
        print(CLEAR)
        print(f"{RED}Erro: O modo de jogo 'Duplas' requer exatamente 4 jogadores registados.{RESET}")
        input(f"{BLUE}Pressione Enter para continuar{RESET}")
        return
    try:
        height = int(input(f"{BLUE}Defina a altura do tabuleiro:\n{GREEN}->\t{RESET}"))
        length = int(input(f"{BLUE}Defina a largura do tabuleiro:\n{GREEN}->\t{RESET}"))
    except ValueError:
        print(f"{RED}Erro: As dimensões devem ser números inteiros.{RESET}")
        return
    if height < 2 or length < 2:
        print(f"{RED}Tamanho inválido. O tabuleiro deve ter pelo menos 2x2.{RESET}")
        return
    board = create_board(height, length)
    if mode:
        active_players = setup_players(board, players)
        if not active_players:
            print(f"{RED}Erro: Número insuficiente de jogadores ativos.{RESET}")
            return
        game_loop(active_players, board)
        win_check(active_players)
    else:
        active_players, teams = setup_players_duplas(board, players)
        if not active_players or not teams:
            print(f"{RED}Erro: Problema na configuração das equipas.{RESET}")
            return
        game_loop_duplas(active_players, board, teams)
        win_check_duplas(active_players, teams)
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
            players.append(create_player(username, 0, 0, 0))
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
            print(f"{RED}Número inválido. Tente novamente.{RESET}")
        except ValueError:
            print(f"{RED}Entrada inválida. Por favor, insira um número.{RESET}")


def show_score(players):
    if not players:
        input(
            f"{CLEAR}{RED}Não há jogadores registados para mostrar pontuação.\n{BLUE}Pressione Enter para continuar{RESET}")
        return
    print(f"{BLUE}Pontuação:{RESET}")
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
    input(f"{RESET}{rules}\n{BLUE}Pressione Enter para continuar{RESET}")


def save(players):
    file_path = './save.json'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump([], json_file)
    with open(file_path, 'r+') as json_file:
        try:
            saved_players = json.load(json_file)
            for player in players:
                if player not in saved_players:
                    saved_players.append(player)
            json_file.seek(0)
            json_file.truncate()
            json.dump(saved_players, json_file, indent=4)
        except Exception:
            json_file.seek(0)
            json_file.truncate()
            json.dump(players, json_file, indent=4)
    input(f"{GREEN}Jogo salvo com sucesso!\n{BLUE}Pressione Enter para continuar{RESET}")


def load():
    try:
        with open('./save.json', 'r') as json_file:
            players = json.load(json_file)
            if not load_username_check(players):
                raise Exception("Nome de jogador repetido")
            input(f"{GREEN}Jogo carregado com sucesso!\n{BLUE}Pressione Enter para continuar{RESET}")
            return players
    except Exception as exception:
        input(
            f"{RED}Não foi possível carregar o jogo.\n{GREEN}->{RESET}\"{exception}\"{BLUE}\nPressione Enter para continuar{RESET}")
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
    mode = True
    while True:
        print(CLEAR)
        if mode:
            print(f"{BLUE}Modo Atual: {YELLOW}1 vs 1{RESET}")
        else:
            print(f"{BLUE}Modo Atual: {RED}2 vs 2{RESET}")
        print(f"{BLUE}Menu:{RESET}")
        print(f"{GREEN}1{RESET} - Registar Jogador")
        print(f"{GREEN}2{RESET} - Iniciar Jogo")
        print(f"{GREEN}3{RESET} - Visualizar Pontuação")
        print(f"{GREEN}4{RESET} - Apagar Jogador")
        print(f"{GREEN}5{RESET} - Exibir Regras")
        print(f"{GREEN}6{RESET} - Salvar Pontuações")
        print(f"{GREEN}7{RESET} - Carregar Pontuações")
        print(f"{GREEN}8{RESET} - Trocar Modo De Jogo")
        print(f"{GREEN}9{RESET} - Sair")
        try:
            option = int(input(f"\n{GREEN}->\t{RESET}"))
            print(CLEAR)
            match option:
                case 1:
                    register_player(players)
                case 2:
                    start_game(players, mode)
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
                    mode = not mode
                case 9:
                    print(f"{BLUE}Saindo do programa. Até logo!{RESET}")
                    break
                case _:
                    print(f"{RED}Opção inválida. Tente novamente.{RESET}")
        except Exception as exception:
            print(CLEAR)
            print(f"{RED}Exceção encontrada.\n{GREEN}->{RESET}\"{exception}\"")
            input(f"{BLUE}Pressione Enter para continuar{RESET}")
