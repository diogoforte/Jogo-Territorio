from macros import *


class Player:
    def __init__(self, x, y, username, color, number):
        self.x = x
        self.y = y
        self.username = username
        self.color = color
        self.number = number

    def move(self, x, y):
        self.x = x
        self.y = y

    def print(self):
        print(f"{self.color}{self.username} | x = {self.x} y = {self.y} | number = {self.number}{RESET}")