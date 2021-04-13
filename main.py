from pnt import PNT


def main():
    print('hello world')
    test_pnt()


def test_pnt():
    pnt = PNT(2)
    print(f'n: {pnt.n}')
    while not pnt.game_over():
        print(f'available moves: {pnt.available_moves}')
        # token = int(input())
        # pnt.play_move(token)
        print(pnt.valid_first_moves())
        print(f'{pnt.take(1)}')
        print(pnt.available_moves)
        print(f'{pnt.take(2)}')
        break

    pnt.declare_winner()


if __name__ == '__main__':
    main()
