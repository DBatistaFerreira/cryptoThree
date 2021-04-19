import copy
import math
from sys import maxsize

from pnt import PNT


class Game:
    def __init__(self, tokens, taken_tokens, list_of_taken_tokens, depth):
        self.tokens = tokens
        self.taken_tokens = taken_tokens
        self.list_of_taken_tokens = list_of_taken_tokens
        self.depth = depth
        self.pnt = self.build_pnt()
        self.best_move = None
        self.initial_state = copy.deepcopy(self.pnt)
        self.number_of_nodes_visited = 0
        self.number_of_nodes_evaluated = 0
        self.depth_reached = maxsize

    def build_pnt(self):
        pnt = PNT(self.tokens)
        for token in self.list_of_taken_tokens:
            pnt.available_moves.remove(token)

        if self.taken_tokens % 2 == 0:
            pnt.turn = pnt.player_max
        else:
            pnt.turn = pnt.player_min

        pnt.last_move = None if not self.list_of_taken_tokens else self.list_of_taken_tokens[-1]

        return pnt

    def alpha_beta(self, pnt: PNT, depth: int, alpha: float, beta: float, maximizing_player: bool):
        self.number_of_nodes_visited += 1

        if not pnt.valid_moves():
            return [self.evaluate(pnt, not maximizing_player, depth), pnt.last_move]
        if depth == 0:
            return [self.evaluate(pnt, maximizing_player, depth), pnt.valid_moves()[0]]
        best_move = 0
        winning_moves = []
        if maximizing_player:
            value = - (maxsize - 1)
            for token in pnt.valid_moves():
                pnt_child = copy.deepcopy(pnt)
                pnt_child.take(token)

                child_value = self.alpha_beta(pnt_child, depth - 1, alpha, beta, False)
                value = max(value, child_value.pop(0))
                alpha = max(alpha, value)
                best_move = token
                # value == 1 indicates that the current token leads to a win so break out
                if value == 1:
                    winning_moves.append(best_move)
                if beta <= alpha:
                    break
            # value == -1 indicates that all options lead to losing so return the lowest valid move
            if value == -1:
                best_move = pnt.valid_moves()[0]
            if value == 1:
                best_move = winning_moves[0]
            return [value, best_move]
        else:
            value = maxsize
            for token in pnt.valid_moves():
                pnt_child = copy.deepcopy(pnt)
                pnt_child.take(token)

                child_value = self.alpha_beta(pnt_child, depth - 1, alpha, beta, True)
                value = min(value, child_value.pop(0))
                beta = min(beta, value)
                best_move = token
                # value == -1 indicates that the current token leads to a win so break out
                if value == -1:
                    winning_moves.append(best_move)
                if beta <= alpha:
                    break
            # value == 1 indicates that all options lead to losing so return the lowest valid move
            if value == 1:
                best_move = pnt.valid_moves()[0]
            if value == -1:
                best_move = winning_moves[0]
            return [value, best_move]

    def evaluate(self, pnt, maximizing_player, depth):
        self.number_of_nodes_evaluated += 1
        if depth < self.depth_reached:
            self.depth_reached = depth
        if pnt.game_over():
            if maximizing_player:
                return 1.0
            else:
                return -1.0

        if maximizing_player:
            if 1 in pnt.valid_moves():
                return 0.0
            elif pnt.last_move == 1:
                return 0.5 if len(pnt.valid_moves()) % 2 == 1 else -0.5
            elif pnt.is_prime(pnt.last_move):
                return 0.7 if len(pnt.valid_moves()) % 2 == 1 else -0.7
            elif not pnt.is_prime(pnt.last_move):
                return 0.6 if len(pnt.valid_moves()) % 2 == 1 else -0.6
        else:
            if 1 in pnt.valid_moves():
                return 0.0
            elif pnt.last_move == 1:
                return -0.5 if len(pnt.valid_moves()) % 2 == 1 else 0.5
            elif pnt.is_prime(pnt.last_move):
                return -0.7 if len(pnt.valid_moves()) % 2 == 1 else 0.7
            elif not pnt.is_prime(pnt.last_move):
                return -0.6 if len(pnt.valid_moves()) % 2 == 1 else 0.6


def initialize():
    print(f'Enter game data <#tokens> <#taken_tokens> <list_of_taken_tokens> <depth>:\n')
    data = input().split()
    data.pop(0)
    tokens = int(data.pop(0))
    taken_tokens = int(data.pop(0))
    depth = int(data.pop())
    list_of_taken_tokens = []
    for token in data:
        list_of_taken_tokens.append(int(token))

    return Game(tokens, taken_tokens, list_of_taken_tokens, depth)


def file_initialize():
    file = open("testcases/testcase.txt", "r")
    for line in file:
        data = line.split()
        data.pop(0)
        for token in data:
            print(token, end=" ")
        tokens = int(data.pop(0))
        taken_tokens = int(data.pop(0))
        depth = int(data.pop())
        list_of_taken_tokens = []
        for token in data:
            list_of_taken_tokens.append(int(token))

        yield Game(tokens, taken_tokens, list_of_taken_tokens, depth)
    file.close()


def start():
    for game in file_initialize():
        if game.depth == 0:
            game.depth = maxsize
        value = game.alpha_beta(game.pnt, game.depth, -math.inf, math.inf, True if game.pnt.turn == 'Max' else False)
        max_depth = game.depth - game.depth_reached
        print(f'\nMove: {value[1]}\nValue: {value[0]}')  # best move (token number)
        print(f"Number of Nodes Visited: {game.number_of_nodes_visited}")  # number of tokens visited during evaluation
        print(f"Number of Nodes Evaluated: {game.number_of_nodes_evaluated}")  # number of tokens evaluated (end game state or specified depth)
        print(f"Max Depth Reached: {max_depth}")  # max depth reached (root is 0)
        # The average branching factor can be quickly calculated as the number of
        # non-root nodes (the size of the tree, minus one; or the number of edges)
        # divided by the number of non-leaf nodes (the number of nodes with children).
        print("Avg Effective Branching Factor: {:.1f}".format((game.number_of_nodes_visited - 1) / (game.number_of_nodes_visited - game.number_of_nodes_evaluated)))
        print()
