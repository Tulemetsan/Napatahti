# -------------------------------------------------------------------------------------------------------------------- #

import json
import datetime
from math import sqrt

# @formatter:off


def pr_round(val, acc): return round(val, acc) if val % 1 else round(val)


def check(x, y):
    x = abs(x)
    y = abs(y)
    if x == 0:
        if y == 0:
            return 0
        else:
            return -1
    elif y == 0:
        return 1
    elif x/y >= 1.5:
        return 1
    elif y/x >= 1.5:
        return -1
    else:
        return 0


def comp_seq(seq):
    num = len(seq)
    res = [0] * num
    for i in range(num):
        flag = set()
        for j in range(num):
            if i == j:
                continue
            else:
                flag.add(check(seq[i], seq[j]))
        if len(flag) == 1:
            res[i] = list(flag)[0]
    return res


def get_max_day(year, mth):
    mth_mxd = {1: 31, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if mth != 2:
        return mth_mxd[mth]
    else:
        if year % 4:
            return 28
        else:
            if str(year).endswith('00'):
                if year % 400:
                    return 28
                else:
                    return 29
            else:
                return 29


def get_fraction(num, max_m, max_n, base):
    if num == 0:
        return 1, 1
    for i in range(1, max_m):
        for j in range(1, max_n):
            if base*i/j == num:
                return i, j
    return 1, 10


def deflect(asp, k=4, max_m=8, max_n=19, base=360):
    m, n = get_fraction(asp, max_m, max_n, base)
    return 28.5/(k * sqrt(m) * (1 + pow(n/7, 2) + pow(n/7, 3)))


# mode: 1 int, 2 float, 3 file name, 4 title
def factory_valid(mode, min_val=0, max_val=10, max_len=15, ext=None, ext_mode=0):
    sym = {' ', '_', '-', '+', '=', '@', '#', '$', '&', '!', '^'}

    def func_valid(arg):
        flag = 0

        if mode in {1, 2}:
            if mode == 1:
                if arg.isdigit():
                    arg = int(arg)
                    flag = 1
                else:
                    return False
            elif mode == 2:
                if arg.isdigit():
                    arg = int(arg)
                    flag = 1
                else:
                    try:
                        arg = float(arg)
                        flag = 1
                    except ValueError:
                        return False
            if not min_val <= arg <= max_val:
                flag = 0

        if ext:
            seq = ext.values() if ext_mode else ext
            if arg in seq:
                return False
            elif flag:
                return True
        elif flag:
            return True

        if mode == 3:
            for i in arg:
                if i.isalnum() or i in sym:
                    continue
                else:
                    return False
            if arg.strip() == '':
                return False
            return True if 0 < len(arg) <= max_len else False
        elif mode == 4:
            if arg.strip() == '':
                return False
            return True if 0 < len(arg) <= max_len else False

    return func_valid


class SmartDictJson:

    def __init__(self, file, mode, *args):
        self.file = file
        self.mode = mode
        self.del_list = args
        self.save_flag = 0

        try:
            self.base = {}
            with open(file) as fp:
                buf = json.load(fp)
                fp.close()
            for i in buf:
                if mode:
                    self.base[i] = json.loads(buf[i])
                else:
                    self.base[i] = set(buf[i])
        except BaseException as error:
            error_log(error)
            self.base = {}

        for i in args:
            self.base[i] = None

    def keys(self): return sorted(self.base.keys())
    def __getitem__(self, key): return self.base[key]
    def __contains__(self, key): return key in self.base

    def __setitem__(self, key, val):
        self.base[key] = val
        self.save_flag = 1

    def __delitem__(self, key):
        del self.base[key]
        self.save_flag = 1

    def __str__(self):
        buf = ''
        for i in self.base:
            buf += '%s : %s,\n' % (i, self.base[i])
        return buf[:-2]

    def dump(self):
        if self.save_flag == 1:
            buf = self.base.copy()
            for i in self.del_list:
                del buf[i]
            for i in buf:
                if self.mode:
                    buf[i] = json.dumps(buf[i])
                else:
                    buf[i] = list(buf[i])
            sep = (',\n', ': ') if self.mode else (', ', ': ')
            with open(self.file, 'w') as fp:
                json.dump(buf, fp, separators=sep)
                fp.close()
        self.save_flag = 0


def error_log(error):
    with open('error_log.txt', 'a') as fp:
        fp.write('%s : %s\n' % (datetime.datetime.now().ctime(), error))
        fp.close()

# -------------------------------------------------------------------------------------------------------------------- #
