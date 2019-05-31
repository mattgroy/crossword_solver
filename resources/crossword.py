import re
import random
from resources import parser, myexceptions as ex
from copy import copy
from operator import itemgetter
from itertools import chain


class Solver:
    def __init__(self, inp, dic, encoding, count):
        # self.count = count
        self.solutions = []
        p = parser.Parser(inp)
        self._hor_words = p.hor_w
        self._ver_words = p.ver_w
        self._order = p.order
        self._width = p.width
        self._height = p.height
        self._overlaps = self._find_overlaps()

        with open(dic, encoding=encoding) as d:
            self._dict = d.read().split()
        dict_lengths = {len(word) for word in self._dict}
        for word in chain(self._hor_words, self._ver_words):
            if word[2] not in dict_lengths:
                raise ex.InputError(
                    'Dictionary does not have a word with length {0}'
                        .format(word[2], word))
        if len(self._dict) < len(self._hor_words) + len(self._ver_words):
            raise ex.InputError('Dictionary has less words than a pattern')

    def draw_field(self):
        string = ''
        for solcount, solution in enumerate(self.solutions):
            data = [['  ' for _ in range(self._width)]
                    for _ in range(self._height)]
            for word in solution:
                if word[0] == 'h':
                    x = self._hor_words[word[1]][0]
                    y = self._hor_words[word[1]][1]
                    for num, letter in enumerate(word[2]):
                        data[x].pop(y + num)
                        data[x].insert(y + num, letter.upper() + ' ')
                elif word[0] == 'v':
                    x = self._ver_words[word[1]][0]
                    y = self._ver_words[word[1]][1]
                    for num, letter in enumerate(word[2]):
                        data[x + num].pop(y)
                        data[x + num].insert(y, letter.upper() + ' ')

            string += 'Solution {}:\n'.format(solcount + 1)
            for i in range(self._height):
                for char in data[i]:
                    string += char
                string += '\n'
        return string

    def __str__(self):
        string = ''
        for solcount, solution in enumerate(self.solutions):
            sol_h = sorted(
                filter(
                    lambda x: x[0] == 'h',
                    solution),
                key=itemgetter(1))
            sol_v = sorted(
                filter(
                    lambda x: x[0] == 'v',
                    solution),
                key=itemgetter(1))

            string += '\nSolution {}:\n    Horizontal:\n    '.format(
                solcount + 1)
            for wcount, h in enumerate(self._hor_words):
                string += '    {0}. {1}\n    '.format(
                    h[3] + 1, sol_h[wcount][2])
            string += 'Vertical:\n    '
            for wcount, v in enumerate(self._ver_words):
                string += '    {0}. {1}\n    '.format(
                    v[3] + 1, sol_v[wcount][2])
        return string

    # finds positions of shared letters
    def _find_overlaps(self):
        overlap = []
        for h_i, h_tuple in enumerate(self._hor_words):
            for h_pos in range(h_tuple[2]):
                for v_i, v_tuple in enumerate(self._ver_words):
                    for v_pos in range(v_tuple[2]):
                        if h_tuple[0] == v_tuple[0] + \
                                v_pos and h_tuple[1] + h_pos == v_tuple[1]:
                            overlap.append((h_i, h_pos, v_i, v_pos))
        return overlap

    # inserts shared letters (if exist) in overlapped positions
    def _get_constraints(self, pos, count):
        orientation, index = pos[0], pos[1]
        constraints = [tuple(pos)]
        if orientation == 'h':
            constraints.append(self._hor_words[index][2])
            for lap in self._overlaps:
                if lap[0] == index:
                    h_pos, v_i, v_pos = lap[1], lap[2], lap[3]
                    for word in self.solutions[count]:
                        if word[0] == 'v' and word[1] == v_i:
                            constraints.append((h_pos, word[2][v_pos]))
                            break
        elif orientation == 'v':
            constraints.append(self._ver_words[index][2])
            for lap in self._overlaps:
                if lap[2] == index:
                    h_i, h_pos, v_pos = lap[0], lap[1], lap[3]
                    for word in self.solutions[count]:
                        if word[0] == 'h' and word[1] == h_i:
                            constraints.append((v_pos, word[2][h_pos]))
                            break
        return constraints

    def _match(self, constraints, del_words):
        regs = []
        pos = constraints[0]
        restr_w = -1
        if pos in del_words:
            restr_w = del_words[pos]
        for i in range(constraints[1]):
            regs.append('\w')
        regs.append('$')
        constraints.pop(0)
        length = constraints.pop(0)
        for i in constraints:
            regs[i[0]] = i[1]
        reg = re.compile(''.join(regs))
        try:
            choose_list = [[val, i] for i, val in enumerate(
                self._dict) if reg.match(val) and i != restr_w]
            word = random.choice(choose_list)
        except IndexError:
            return None
        return word

    def _backup(self, pos, count, order, del_order):
        if pos[0] == 'v':
            for overlap in filter(lambda x: x[2] == pos[1], self._overlaps):
                n_pos = ('h', overlap[0])
                if n_pos in del_order:
                    next_pos = n_pos
                    if pos in del_order:
                        del_order.remove(pos)
                    self._backup(next_pos, count, order, del_order)

        elif pos[0] == 'h':
            for overlap in filter(lambda x: x[0] == pos[1], self._overlaps):
                n_pos = ('v', overlap[2])
                if n_pos in del_order:
                    next_pos = n_pos
                    if pos in del_order:
                        del_order.remove(pos)
                    self._backup(next_pos, count, order, del_order)

        el = [item for item in self.solutions[count]
              if item[0] == pos[0] and item[1] == pos[1]]
        if len(el) == 1:
            self.solutions[count].remove(el[0])
        if pos not in order:
            order.insert(0, pos)
        return

    def solve(self):
        # for count in range(self.count):
        count = 0
        self.solutions.append([])
        order = copy(self._order)

        del_order = []
        del_words = {}
        while len(order) > 0:
            constraints = self._get_constraints(order[0], count)
            pos = constraints[0]
            match = self._match(constraints, del_words)
            if not match:
                self._backup(pos, count, order, del_order)
                continue

            self.solutions[count].append(
                (order[0][0], order[0][1], match[0], match[1]))
            del_order.append(order.pop(0))
