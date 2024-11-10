from macros import *

class Board:
    def __init__(self):
        self.board = None
        self.height = None
        self.length = None
        self.setup()

    def print(self):
        for i in range(self.height):
            for j in range(self.length):
                print(f"{CYAN}{self.board[i][j]}{RESET}", end=" ")
            print()

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