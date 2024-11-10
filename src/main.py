from src.Board import Board
from Players import Players
from macros import *

def clear_screen():
    print(CLEAR)

def game_loop(players, board):
    print("Game loop")
    while True:
        for players in players.get_all():
            clear_screen()
            board.print()
            print(f"{players.username} turn")

def main():
    clear_screen()
    print("Welcome to the game")
    board = Board()
    players = Players(board.height, board.length)
    game_loop(players, board)

if __name__ == "__main__":
    main()
