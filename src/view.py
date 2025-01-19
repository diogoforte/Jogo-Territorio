from controller import *
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

# Função principal do programa
def main():
    players = [] # Lista que vai armazenar os jogadores registados
    mode = True # Loop principal do menu
    while True:
        print(CLEAR)
        if mode:
            print(f"{BLUE}Modo Atual: {YELLOW}Player vs Player{RESET}")
        else:
            print(f"{BLUE}Modo Atual: {RED}Duplas{RESET}")
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
                    break # Encerra o loop principal
                case _:
                    print(f"{RED}Opção inválida. Tente novamente.{RESET}")
        except Exception as exception:
            # Trata de exceções, mostra o erro e permite que o utilizador continue
            print(CLEAR)
            print(f"{RED}Exceção encontrada.\n{GREEN}->{RESET}\"{exception}\"")
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