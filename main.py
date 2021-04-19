import game


def main():
    game.start()


def test_pnt():
    pnt = game.initialize().pnt
    print(f'n: {pnt.tokens}')
    while not pnt.game_over():
        print(f'available moves: {pnt.available_moves}')
        print(f'valid moves: {pnt.valid_moves()}')
        token = int(input())
        pnt.take(token)
        print()

    pnt.declare_winner()


if __name__ == '__main__':
    main()
