from macros import *


class Board:
    def __init__(self):
        self.board = None
        self.height = None
        self.length = None
        self.setup()

    def print(self):
        print("  ", end="")
        for j in range(self.length):
            print(f"{j + 1:2}", end="")
        print(" X")
        for i in range(self.height):
            print(f"{i + 1:2} ", end="")
            for j in range(self.length):
                match self.board[i][j]:
                    case 0:
                        print(f"{GREY}{self.board[i][j]}{RESET} ", end="")
                    case 1:
                        print(f"{RED}{self.board[i][j]}{RESET} ", end="")
                    case 2:
                        print(f"{GREEN}{self.board[i][j]}{RESET} ", end="")
                    case 3:
                        print(f"{YELLOW}{self.board[i][j]}{RESET} ", end="")
                    case 4:
                        print(f"{BLUE}{self.board[i][j]}{RESET} ", end="")
            print()
        print(" Y")

    def setup(self):
        while True:
            self.height = int(input("Define the board height:\n\t"))
            if self.height <= 0:
                print(f"{RED}Invalid height.{RESET}")
                continue
            break
        while True:
            self.length = int(input("Define the board length:\n\t"))
            if self.length <= 0:
                print(f"{RED}Invalid length.{RESET}")
                continue
            break
        self.board = [[0 for i in range(self.length)] for j in range(self.height)]
