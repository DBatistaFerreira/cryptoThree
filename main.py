from pnt import PNT


def main():
    print('hello world')
    test_pnt()


def test_pnt():
    pnt = PNT()
    print(pnt.n)
    print(pnt.last_move)
    print(pnt.available_moves)


if __name__ == '__main__':
    main()
