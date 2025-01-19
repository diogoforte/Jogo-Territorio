import json
import random
import os

# Definição de constantes para cores de texto
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
GREY = "\033[90m"
RESET = "\033[0m" # Reseta a formatação do texto para o padrão
CLEAR = "\033[2J\033[H" # Limpa a tela e posiciona o cursor no canto superior esquerdo

# Função para exibir o tabuleiro de jogo
def print_board(board):
    print("  ", end="") # Espaço inicial para alinhar os índices das colunas
    for j in range(board['length']): # Itera sobre o número de colunas
        print(f"{j + 1:2}", end="") # Exibe o índice da coluna, alinhado em 2 caracteres
    print(" X")
    for i in range(board['height']): # Itera sobre o número de linhas
        print(f"{i + 1:2} ", end="") # Exibe o índice da linha, alinhado em 2 caracteres
        for j in range(board['length']): # Itera sobre cada célula da linha
            # Verifica o valor da célula usando 'match-case' e aplica a cor correspondente
            match board['board'][i][j]:
                case 0:
                    print(f"{GREY}{board['board'][i][j]}{RESET} ", end="")
                case 1:
                    print(f"{RED}{board['board'][i][j]}{RESET} ", end="")
                case 2:
                    print(f"{BLUE}{board['board'][i][j]}{RESET} ", end="")
                case 3:
                    print(f"{YELLOW}{board['board'][i][j]}{RESET} ", end="")
                case 4:
                    print(f"{GREEN}{board['board'][i][j]}{RESET} ", end="")
        print()
    print(" Y")

# Cria e retorna um jogador com os atributos fornecidos
def create_player(username, color, number, score):
    return {'username': username, 'color': color, 'number': number, 'score': score, 'pieces': 20}


# Atualiza a posição de um jogador
def move_player(player, x, y):
    player['x'] = x
    player['y'] = y


# Cria e retorna um tabuleiro como uma matriz 2D inicializada com zeros
def create_board(height, length):
    return {'board': [[0 for _ in range(length)] for _ in range(height)], 'height': height, 'length': length}


# Coloca o número do jogador na posição (x, y) no tabuleiro
def update_board(board, player, x, y):
        board['board'][x][y] = player['number']


# Adiciona um jogador ao tabuleiro e à lista de jogadores activos
def add_player_to_board(board, active_players, positions, player, color, number):
    x, y = positions.pop(0)
    new_player = create_player(player["username"], color, number, 0)
    update_board(board, new_player, x, y)
    active_players.append(new_player)


# Exibe a lista de jogadores disponíveis
def print_player_list(players):
    print(f"{BLUE}Escolha os jogadores:{RESET}")
    for i, player in enumerate(players):
        print(f"{GREEN}{i + 1}{RESET} - {player['username']}")


# Permite seleccionar um jogador, garantindo que a escolha é válida
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


# Configura os jogadores individuais no tabuleiro
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


# Configura os jogadores em duplas
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


# Verifica se existe uma casa adjacente na posição (x, y) com o número especificado
def check_surroundings(x, y, board, number):
    return any(
        0 <= x + dx < board["height"] and 0 <= y + dy < board["length"] and board['board'][x + dx][y + dy] == number
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1])


# Verifica se o movimento para (x, y) é válido para o jogador
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


# Verifica se o jogador ainda tem jogadas possíveis no tabuleiro
def possible_plays_check(board, player):
    for i in range(board['height']):
        for j in range(board['length']):
            if board['board'][i][j] == player['number']:
                if check_surroundings(i, j, board, 0):
                    return True
    return False


# Verifica se o jogo terminou
def check_if_game_ended(players, board):
    if (all(player['pieces'] == 0 for player in players) or
            not any(board['board'][i][j] == 0 for i in range(board['height']) for j in range(board['length']))):
        return True
    return False


# Representa o turno de um jogador, permitindo-lhe realizar movimentos válidos
def play_turn(player, board):
    moves = 1
    while moves > 0:
        print(CLEAR)
        print_board(board)
        print(f"{RESET}Turno do jogador {player['color']}{player['username']} {RESET}({player['number']})")
        while True:
            if not check_player_plays(player, board):
                return
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
        # Bónus - Há uma chance de 20% do jogador ganhar uma jogada extra
        if random.randint(0, 10) <= 2:
            print(f"{RESET}Bónus! {player['color']}{player['username']}{RESET} ganhou uma jogada extra!{RESET}")
            moves += 1
            input(f"{BLUE}Pressione Enter para continuar{RESET}")


# Verifica se o jogador tem jogadas possíveis; caso contrário, passa a vez
def check_player_plays(player, board):
    if not possible_plays_check(board, player):
        input(
            f"{RESET}O jogador {player['color']}{player['username']} {RESET}({player['number']}) "
            f"não tem jogadas possíveis. Passando a vez.\n{BLUE}Pressione Enter para continuar{RESET}"
        )
        return False
    return True


# Controla a lógica principal do jogo com jogadores individuais
def game_loop(players, board):
    while True:
        for player in players:
            play_turn(player, board)
        if check_if_game_ended(players, board):
            break


# Controla a lógica principal do jogo em modo de equipas
def game_loop_duplas(players, board, teams):
    print_board(board)
    while True:
        for team_index, team in enumerate(teams):
            print(f"{BLUE}Turno da equipa {team_index + 1}:{RESET}")
            for player in [p for p in players if p["username"] in team]:
                play_turn(player, board)
        if check_if_game_ended(players, board):
            break


# Verifica qual equipa venceu, somando as peças restantes de cada equipa
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
    

# Determina o vencedor individual ou verifica se houve empate
def win_check(players):
    min_pieces = min(player['pieces'] for player in players)
    winners = [player for player in players if player['pieces'] == min_pieces]
    if len(winners) > 1:
        print(f"{BLUE}O jogo terminou em empate!{RESET}")
    else:
        winner = winners[0]
        winner['score'] = 1
        print(f"{CLEAR}{winner['color']}{winner['username']}{RESET} ({winner['number']}){BLUE} venceu 🎉\n{RESET}")


# Inicia o jogo, configurando tabuleiro e jogadores, e executa o loop principal
def start_game(players, mode):
    if len(players) < 2:
        print(CLEAR)
        print(f"{RED}É necessário pelo menos 2 jogadores registados para iniciar o jogo.{RESET}")
        input(f"{BLUE}Pressione Enter para continuar{RESET}")
        return
    if not mode and len(players) < 4:
        print(CLEAR)
        print(f"{RED}O modo de jogo 'Duplas' requer exatamente 4 jogadores registados.{RESET}")
        input(f"{BLUE}Pressione Enter para continuar{RESET}")
        return
    try:
        height = int(input(f"{BLUE}Defina a altura do tabuleiro:\n{GREEN}->\t{RESET}"))
        length = int(input(f"{BLUE}Defina a largura do tabuleiro:\n{GREEN}->\t{RESET}"))
    except ValueError:
        input(f"{RED}As dimensões devem ser números inteiros.{RESET}")

        return
    if height < 2 or length < 2 or height > 10 or length > 10:
        input(f"{RED}Tamanho inválido.\n{BLUE}Pressione Enter para continuar{RESET}")
        return
    board = create_board(height, length)
    if mode:
        # Configura jogadores individuais
        active_players = setup_players(board, players)
        if not active_players:
            input(f"{RED}Número insuficiente de jogadores ativos.\n{BLUE}Pressione Enter para continuar{RESET}{RESET}")
            return
        game_loop(active_players, board)
        win_check(active_players)
    else:
        # Configura equipas para o modo Duplas
        active_players, teams = setup_players_duplas(board, players)
        if not active_players or not teams:
            print(f"{RED}Problema na configuração das equipas.{RESET}")
            return
        game_loop_duplas(active_players, board, teams)
        win_check_duplas(active_players, teams)
    print_board(board)
    # Atualiza e apresenta a pontuação final
    print(f"{BLUE}Pontuação atual:{RESET}")
    for player in players:
        for active_player in active_players:
            if player['username'] == active_player['username'] and active_player['score'] == 1:
                player['score'] += 1
    for player in players:
        print(f"    {player['username']} -> {player['score']} pontos")
    input(f"{BLUE}Pressione Enter para continuar{RESET}")


# Verifica se o nome de utilizador é válido e único
def username_check(username, players):
    if not username:
        print(f"{RED}Nome invalido{RESET}")
        return False
    for player in players:
        if username == player["username"]:
            print(f"{RED}Nome ja existente{RESET}")
            return False
    return True


# Regista um novo jogador com um nome único
def register_player(players):
    while True:
        username = input(f"{BLUE}Defina o nome do jogador:\n{GREEN}->\t{RESET}")
        if username_check(username, players):
            players.append(create_player(username, 0, 0, 0))
            break


# Remove um jogador da lista de jogadores registados
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


# Mostra a pontuação atual de todos os jogadores registados
def show_score(players):
    if not players:
        input(
            f"{CLEAR}{RED}Não há jogadores registados para mostrar pontuação.\n{BLUE}Pressione Enter para continuar{RESET}")
        return
    print(f"{BLUE}Pontuação:{RESET}")
    for player in players:
        print(f"{player['username']}\t{GREEN}->\t{RESET}{player['score']}{RESET}")
    input(f"{BLUE}Pressione Enter para continuar{RESET}")

# Mostra as regras do jogo
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


# Função que guarda o estado do jogo num ficheiro JSON
def save(players):
    file_path = './save.json'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump([], json_file) # Cria um ficheiro vazio caso não exista
    with open(file_path, 'r+') as json_file:
        try:
            saved_players = json.load(json_file) # Carrega os jogadores salvos
            for player in players:
                if player not in saved_players: # Adiciona jogadores novos
                    saved_players.append(player)
            json_file.seek(0)
            json_file.truncate() # Limpa o ficheiro antes de gravar
            json.dump(saved_players, json_file, indent=4) # Grava os jogadores atualizados
        except Exception:
            json_file.seek(0)
            json_file.truncate() # Limpa o ficheiro se houver erro
            json.dump(players, json_file, indent=4) # Grava o estado atual do jogo
    input(f"{GREEN}Jogo salvo com sucesso!\n{BLUE}Pressione Enter para continuar{RESET}")


# Função que carrega o estado do jogo a partir de um ficheiro JSON
def load():
    try:
        with open('./save.json', 'r') as json_file:
            players = json.load(json_file) # Carrega os jogadores do ficheiro
            if not load_username_check(players): # Verifica se os nomes dos jogadores são únicos
                raise Exception("Nome de jogador repetido")
            input(f"{GREEN}Jogo carregado com sucesso!\n{BLUE}Pressione Enter para continuar{RESET}")
            return players
    except Exception as exception:
        input(
            f"{RED}Não foi possível carregar o jogo.\n{GREEN}->{RESET}\"{exception}\"{BLUE}\nPressione Enter para continuar{RESET}")
        return []


# Verifica se os nomes dos jogadores são válidos e únicos
def load_username_check(players):
    seen_usernames = set()
    for player in players:
        if not player['username'] or player['username'] in seen_usernames:
            return False
        seen_usernames.add(player['username'])
    return True