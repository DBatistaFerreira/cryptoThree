import copy
import math
from sys import maxsize
from typing import List

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


def alpha_beta(pnt: PNT, depth: int, alpha: float, beta: float, maximizing_player: bool):
    if not pnt.valid_moves():
        return [evaluate(pnt, maximizing_player)]
    if depth == 0:
        return [evaluate(pnt, maximizing_player)]
    best_move = 0
    if maximizing_player:
        value = - (maxsize - 1)
        for token in pnt.valid_moves():
            pnt.take(token)
            print(f"Best Move for man: {token}")
            print(f"depth: {depth}")
            print(f"Value: {value}\n")
            child_value = alpha_beta(pnt, depth - 1, alpha, beta, False)
            value = max(value, child_value.pop(0))
            alpha = max(alpha, value)
            best_move = token
            if beta <= alpha:
                break
        return [value, best_move]
    else:
        value = maxsize
        for token in pnt.valid_moves():
            pnt.take(token)
            print(f"Best Move for min: {token}")
            print(f"depth: {depth}")
            print(f"Value: {value}\n")

            child_value = alpha_beta(pnt, depth - 1, alpha, beta, True)
            value = min(value, child_value.pop(0))
            beta = min(beta, value)
            best_move = token
            if beta <= alpha:
                break
        return [value, best_move]


def evaluate(pnt, maximizing_player):
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
    tokens = int(data.pop(0))
    taken_tokens = int(data.pop(0))
    depth = int(data.pop())
    list_of_taken_tokens = []
    for token in data:
        list_of_taken_tokens.append(int(token))

    return Game(tokens, taken_tokens, list_of_taken_tokens, depth)


def start():
    game = initialize()
    value = alpha_beta(game.pnt, game.depth, -math.inf, math.inf, True if game.pnt.turn == 'Max' else False)
    move = game.best_move        # best move (token number)
    print(f'move: {move}\nvalue: {value}')
    visited = 0     # number of tokens visited during evaluation
    evaluated = 0   # number of tokens evaluated (end game state or specified depth)
    max_depth = 0   # max depth reached (root is 0)
    aebf = 0        # average effective branching factor (avg number of successors that are not pruned)
