from Player import Player
from macros import *

class Players:
    def __init__(self, height, length):
        self.players = []
        self.setup(height, length)

    def print(self):
        for player in self.players:
            player.print()

    def get(self, index):
        return self.players[index]

    def get_all(self):
        return self.players

    def setup(self, height, length):
        players_count = (int(input("Define the number of players:\n\t")))
        while players_count > 4 or players_count < 1:
            print(f"{RED}Invalid number of Players{RESET}")
            players_count = (int(input("Define the number of players:\n\t")))
        positions = [(0, 0), (0, length - 1), (height - 1, 0), (height - 1, length - 1)]
        player_colors = [RED, GREEN, YELLOW, BLUE]
        usernames = set()
        for i in range(players_count):
            while True:
                username = input(f"Define the name of player {i + 1}:\n\t")
                if not username:
                    print(f"{RED}Invalid username{RESET}")
                    continue
                elif username in usernames:
                    print(f"{RED}Username already taken. Please choose a different name.{RESET}")
                    continue
                usernames.add(username)
                break
            x, y = positions[i]
            self.players.append(Player(x, y, username, player_colors[i]))