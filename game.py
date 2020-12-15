# %%
import random
import math


class Dice:
    N = 6

    def throw(self):
        return random.randint(1, self.N)


class Player:

    def __init__(self, name):
        self.position = 1
        self.name = name

    def jump(self, jumps):
        self.position += jumps

    def move_to(self, position):
        self.position = position

    def __str__(self):
        return self.name


class Board:

    def __init__(self, size=10):
        self.size = size
        self.finish = size * size
        self.ladders = {}
        self.snakes = {}

    def is_valid_ladder(self, src, dest):
        valid_ladder = (
            src != dest
            and dest > math.ceil(src/self.size) * self.size
            and src not in self.snakes
            and dest not in self.snakes
        )
        return valid_ladder

    def is_valid_snake(self, src, dest):
        valid_snake = (
            src != dest
            and dest < math.ceil(src/self.size) * self.size
            and src not in self.ladders
            and dest not in self.ladders
        )
        return valid_snake

    def add_ladder(self, src, dest):
        if not self.is_valid_ladder(src, dest):
            raise ValueError("Ladder should always go upwards.")
        self.ladders[src] = dest

    def add_snake(self, src, dest):
        if not self.is_valid_snake(src, dest):
            raise ValueError("Snake should always go downwards.")
        self.snakes[src] = dest

    def randomize_ladders(self, count):
        while len(self.ladders) < count:
            try:
                self.add_ladder(
                    random.randint(1, self.finish),
                    random.randint(1, self.finish-1)
                )
            except:
                pass

    def randomize_snakes(self, count):
        while len(self.snakes) < count:
            try:
                self.add_snake(
                    random.randint(1, self.finish-1),
                    random.randint(1, self.finish)
                )
            except:
                pass


class SnakesAndLadders:

    def __init__(self, board):
        self.dice = Dice()
        self.board = board
        self.game_end = False

    def make_move(self, player):
        if self.game_end:
            print("Game has ended.")
            return

        dice_roll = self.dice.throw()
        player.jump(dice_roll)

        if player.position in self.board.ladders:
            print("{} has found a ladder!".format(player), end=' ')
            player.move_to(self.board.ladders[player.position])
        elif player.position in self.board.snakes:
            print("{} was bitten by a snake!!".format(player), end=' ')
            player.move_to(self.board.snakes[player.position])

        if player.position >= self.board.finish:
            print("{} has WON!!!".format(player.name))
            self.game_end = True
            return

        print("{} moved to {}".format(player.name, player.position))

# %%


def simulate():
    board = Board()
    board.randomize_ladders(count=10)
    board.randomize_snakes(count=10)
    game = SnakesAndLadders(board)

    p1 = Player('p1')
    p2 = Player('p2')
    p3 = Player('p3')

    players = [p1, p2, p3]
    player_idx = 0

    while not game.game_end:
        curr_player = players[player_idx]
        game.make_move(curr_player)
        player_idx = (player_idx + 1) % len(players)


simulate()
# %%
