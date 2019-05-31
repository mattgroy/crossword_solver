import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from resources import crossword as cr, parser as par, myexceptions as ex


def test_parser_all_fine():
    inp = ['\n', 'h (0, 0) 1', ' H( 1,0 )4 ', 'v ( 0, 1)  8']
    parser = par.Parser(inp)
    hor = parser.hor_w
    ver = parser.ver_w
    order = parser.order
    height = parser.height
    width = parser.width
    assert hor == [[0, 0, 1, 0], [1, 0, 4, 2]]
    assert ver == [[0, 1, 8, 1]]
    assert order == [('h', 0), ('v', 0), ('h', 1)]
    assert height == 8
    assert width == 4


def test_parser_wrong():
    inp = ['\n', ' asdh (0, 0) 1', ' H 1,0 )4 ', 'v ( 0, 1)  8']
    err_str = ''
    try:
        par.Parser(inp)
    except ex.InputError as e:
        err_str = str(e)
    assert err_str == 'Wrong line met (2):  asdh (0, 0) 1'
    with pytest.raises(ex.InputError):
        par.Parser([' H 1,0 )4'])


def test_solver_no_dict():
    inp = ['\n', 'h (0, 0) 1', ' H( 1,0 )4 ', 'v ( 0, 1)  8']
    dic = 'tests/wrong_dict.txt'
    enc = 'cp1251'
    with pytest.raises(ex.InputError):
        cr.Solver(inp, dic, enc, 1)
    with pytest.raises(ex.InputError):
        cr.Solver(['h (0,0) 3', 'v (0,1) 3', 'h (2, 1) 3'], dic, enc, 1)


def test_ex_single():
    enc = 'utf_8'
    with open('tests/ex_single.txt') as f:
        inp = f.readlines()
    with open('tests/exS_single.txt', encoding=enc) as f:
        res_expected = f.read()
    with open('tests/exSD_single.txt', encoding=enc) as f:
        resD_expected = f.read()
    sols_expected = {'ил', 'бар', 'коп', 'род', 'ель', 'беда', 'окоп', 'омар',
                     'ра', 'табачок', 'бывший', 'упруго', 'прохвост'}
    dic = 'tests/dic_ex_single.txt'
    s = cr.Solver(inp, dic, enc, 1)
    s.solve()
    sols = {i[2] for i in s.solutions[0]}
    assert sols == sols_expected
    assert str(s).strip() == res_expected.strip().replace('\t', '    ')
    draw = s.draw_field()
    assert draw.strip() == resD_expected.strip()


def test_ex_single_2():
    enc = 'utf_8'
    with open('tests/ex_single_2.txt') as f:
        inp = f.readlines()
    with open('tests/exS_single_2.txt', encoding=enc) as f:
        res_expected = f.read()
    with open('tests/exSD_single_2.txt', encoding=enc) as f:
        resD_expected = f.read()
    sols_expected = {'пловец', 'голова', 'егерь', 'полка', 'анды', 'обводка'}
    dic = 'tests/dic_ex_single_2.txt'
    s = cr.Solver(inp, dic, enc, 1)
    s.solve()
    sols = {i[2] for i in s.solutions[0]}
    assert sols == sols_expected
    assert str(s).strip() == res_expected.strip().replace('\t', '    ')
    draw = s.draw_field()
    assert draw.strip() == resD_expected.strip()


if __name__ == '__main__':
    pytest.main()
