from controller import *

def main():
    players = []
    mode = True
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
                    break
                case _:
                    print(f"{RED}Opção inválida. Tente novamente.{RESET}")
        except Exception as exception:
            print(CLEAR)
            print(f"{RED}Exceção encontrada.\n{GREEN}->{RESET}\"{exception}\"")
            input(f"{BLUE}Pressione Enter para continuar{RESET}")
