import json
import os
import random

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


# Verifica se existe uma casa adjacente na posição (x, y) com o número especificado
def check_surroundings(x, y, board, number):
    return any(
        0 <= x + dx < board["height"] and 0 <= y + dy < board["length"] and board['board'][x + dx][y + dy] == number
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1])


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


# Regista um novo jogador com um nome único
def register_player(players):
    while True:
        username = input(f"{BLUE}Defina o nome do jogador:\n{GREEN}->\t{RESET}")
        if username_check(username, players):
            players.append(create_player(username, 0, 0, 0))
            break


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