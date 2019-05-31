import re
from operator import itemgetter
from resources import myexceptions as ex


class Parser:
    def __init__(self, raw):
        self.hor_w = []
        self.ver_w = []
        self.order = []
        self.width = 0
        self.height = 0
        self._reg = re.compile(
            r'\s*([HV])\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*(\d+)\s*'
            r'((?:\d\s*[a-zа-яё]\s*)*)',
            flags=re.I)
        self._parse_raw(raw)

    def _parse_raw(self, raw):
        order = []
        for i, line in enumerate(raw):
            if not line.strip():
                continue
            good = self._reg.match(line)
            if good:
                toadd = [good.group(1).lower(),
                         int(good.group(2)),
                         int(good.group(3)),
                         int(good.group(4))]
                # TODO: predefined letters
                # good.group(5).lower()]
                # if good.group(5):
                #     g = ''.join(good.group(5).lower().split())
                #     gg = []
                #     for j in range(0, len(g), 2):
                #         gg.append((g[j], g[j + 1]))
                #     toadd.append(tuple(gg))
                order.append(toadd)
            else:
                raise ex.InputError(
                    'Wrong line met ({0}): {1}'.format(
                        i + 1, line))
        neworder = sorted(order, key=itemgetter(1, 2, 0))
        for count, e in enumerate(neworder):
            neworder[count].append(count)
            word = neworder[count]
            if word[0] == 'h':
                width = word[2] + word[3]
                if width > self.width:
                    self.width = width
                self.hor_w.append(word[1:])
                self.order.append((word[0], len(self.hor_w) - 1))
            elif word[0] == 'v':
                height = word[1] + word[3]
                if height > self.height:
                    self.height = height
                self.ver_w.append(word[1:])
                self.order.append((word[0], len(self.ver_w) - 1))
