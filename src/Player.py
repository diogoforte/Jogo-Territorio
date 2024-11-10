from macros import *

class Player:
    def __init__(self, x, y, username, color):
        self.x = x
        self.y = y
        self.username = username
        self.color = color

    def move(self, x, y):
        self.x += x
        self.y += y

    def get_pos(self):
        return self.x, self.y

    def print(self):
        print(f"{self.color}{self.username} | {self.x} {self.y}{RESET}")