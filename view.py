RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
GREY = "\033[90m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

def clear_screen():
    print(CLEAR)

def print_board(board):
    print("  ", end="")
    for j in range(board['length']):
        print(f"{j + 1:2}", end="")
    print(" X")
    for i in range(board['height']):
        print(f"{i + 1:2} ", end="")
        for j in range(board['length']):
            match board['board'][i][j]:
                case 0:
                    print(f"{GREY}{board['board'][i][j]}{RESET} ", end="")
                case 1:
                    print(f"{RED}{board['board'][i][j]}{RESET} ", end="")
                case 2:
                    print(f"{RED}{board['board'][i][j]}{RESET} ", end="")  # Adjust for team colors
                case 3:
                    print(f"{YELLOW}{board['board'][i][j]}{RESET} ", end="")
                case 4:
                    print(f"{YELLOW}{board['board'][i][j]}{RESET} ", end="")  # Adjust for team colors
        print()
    print(" Y")

def print_teams(players):
    teams = {"Red/Blue": [], "Yellow/Green": []}
    for player in players:
        if player['team']:
            teams[player['team']].append(player['username'])
    print(f"{BLUE}Equipas:{RESET}")
    for team, members in teams.items():
        print(f"{CYAN}{team}{RESET}: {', '.join(members)}")