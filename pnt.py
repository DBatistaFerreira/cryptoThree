from cryptolib import range_inclusive


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

    def get_valid_first_moves(self):
        first_moves = []
        for i in range(1, int(self.n / 2)):
            if i % 2 != 0:
                first_moves.append(i)

        return first_moves

