from pnt import PNT


def main():
    print('hello world')
    test_pnt()


def test_pnt():
    pnt = PNT(10)
    print(f'n: {pnt.n}')
    while not pnt.game_over():
        print(f'available moves: {pnt.available_moves}')
        print(f'valid moves: {pnt.valid_moves()}')
        token = int(input())
        pnt.take(token)
        print()
        # pnt.take(1)
        # print()
        # print(f'available moves: {pnt.available_moves}')
        # print(f'valid moves: {pnt.valid_moves()}')
        # pnt.take(2)
        # print()
        # print(f'available moves: {pnt.available_moves}')
        # print(f'valid moves: {pnt.valid_moves()}')
        # pnt.take(6)
        # print()
        # break

    pnt.declare_winner()


if __name__ == '__main__':
    main()
