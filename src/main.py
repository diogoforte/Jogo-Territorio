from Players import Players
from Board import Board
from macros import *

def clear_screen():
    print(CLEAR)

def board_updater(board, players):
    for player in players.get_all():
        x, y = player.get_pos()
        board.board[x][y] = player.number

def move_check(x, y, player, board):
    if x < 0 or y < 0 or x >= board.height or y >= board.length:
        print(f"{RED}Out of bounds move.{RESET}")
        return False
    if board.board[x][y] != 0:
        print(f"{RED}Square already taken.{RESET}")
        return False
    if x - 1 >= 0 and y - 1 >= 0 and board.board[x - 1][y - 1] == player.number:
        return True
    if x - 1 >= 0 and y + 1 < board.length and board.board[x - 1][y + 1] == player.number:
        return True
    if x + 1 < board.height and y - 1 >= 0 and board.board[x + 1][y - 1] == player.number:
        return True
    if x + 1 < board.height and y + 1 < board.length and board.board[x + 1][y + 1] == player.number:
        return True
    print(f"{RED}Non diagonal move.{RESET}")
    return False

def game_loop(players, board):
    while True:
        for player in players.get_all():
            board_updater(board, players)
            board.print()
            print(f"{player.username}'s turn")
            while True:
                y = int(input("Move x:\n\t")) - 1
                x = int(input("Move y:\n\t")) - 1
                if move_check(x, y, player, board):
                    break
            player.move(x, y)
            clear_screen()

def main():
    clear_screen()
    print("Welcome to the game")
    board = Board()
    players = Players(board.height, board.length)
    board_updater(board, players)
    game_loop(players, board)

if __name__ == "__main__":
    main()
