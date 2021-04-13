from cryptolib import range_inclusive
from max import Max
from min import Min


def build_available_moves_list(n):
    available_moves_list = []
    for i in range_inclusive(1, n):
        available_moves_list.append(i)

    return available_moves_list


class PNT:
    def __init__(self, n=9):
        self.n = n
        self.last_move = None
        self.available_moves = build_available_moves_list(n)
        self.player_max = Max()
        self.player_min = Min()
        self.turn = self.player_max

    def valid_first_moves(self):
        first_moves = []
        for i in range_inclusive(1, int(self.n / 2)):
            if i % 2 != 0:
                first_moves.append(i)

        return first_moves

    def is_multiple(self, token):
        return token % self.last_move == 0

    def is_factor(self, token):
        return self.last_move % token == 0

    def is_valid_move(self, token):
        return self.available_moves.__contains__(token) and (self.is_multiple(token) or self.is_factor(token))

    def is_valid_first_move(self, token):
        return self.available_moves.__contains__(token) and self.valid_first_moves().__contains__(token)

    def next_turn_player(self):
        return self.player_min if self.turn is self.player_max else self.player_max

    def declare_winner(self):
        print(f'winner: {self.next_turn_player().name}')

    def game_over(self):
        return not self.available_moves

    def take(self, token):
        if self.last_move is None:
            if self.is_valid_first_move(token):
                self.available_moves.remove(token)
                self.last_move = token
                print(f'{self.turn.name} played: {token}')
                self.turn = self.next_turn_player()
                return True
        elif self.is_valid_move(token):
            self.available_moves.remove(token)
            self.last_move = token
            print(f'{self.turn.name} played: {token}')
            self.turn = self.next_turn_player()
            return True

        return False
