from resources import crossword, myexceptions as ex
import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e',
        '--encoding',
        type=str,
        default='utf_8',
        help='Encoding of dictionary file (Default - UTF-8)')
    # parser.add_argument(
    #     '-c',
    #     '--count',
    #     type=int,
    #     default=1,
    #     help='Number of solutions (Default - 1)')
    parser.add_argument(
        '-d',
        '--draw',
        action='store_true',
        help='Draw crossword field with solution')
    parser.add_argument(
        '-w',
        '--write',
        default=None,
        help='Store solution in file')
    parser.add_argument(
        'dict',
        metavar='DICTIONARY',
        type=str,
        default='resources/ruwords.txt',
        help='List of words used for solving a crossword')
    parser.add_argument(
        'inp',
        metavar='INPUT',
        nargs='?',
        type=str,
        help='Grid pattern')

    # args = parser.parse_args(
    #     ['-ecp1251', '-d', 'dic_ex.txt', 'ex.txt'])
    args = parser.parse_args()
    file_name = args.inp
    dic = args.dict
    encoding = args.encoding
    count = 1
    draw = args.draw
    outp = args.write

    if file_name:
        with open(file_name) as f:
            file = f.readlines()
    else:
        file = sys.stdin.readlines()

    try:
        s = crossword.Solver(file, dic, encoding, count)
        s.solve()
    except ex.InputError as e:
        print(e, file=sys.stderr)
    else:
        if draw:
            print(s.draw_field())
        else:
            print(s)
        print('Done!')
        if outp is not None:
            with open(outp, 'w') as outp_file:
                if draw:
                    print(s.draw_field(), file=outp_file)
                else:
                    print(s, file=outp_file)


if __name__ == "__main__":
    main()
