# -------------------------------------------------------------------------------------------------------------------- #

import json
import core.utilities as ut

# @formatter:off


class AspectPage:
    pl_src = {
        0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
        10: 11, 11: 23, 12: 12, 13: 56, 14: 57, 15: 15, 16: -4
    }
    asp_src = {
        0: 0, 1: 20, 2: 360/14, 3: 30, 4: 36, 5: 40, 6: 45, 7: 360/7, 8: 60, 9: 72, 10: 80, 11: 90, 12: 100,
        13: 720/7, 14: 108, 15: 120, 16: 135, 17: 140, 18: 144, 19: 150, 20: 1080/7, 21: 160, 22: 180
    }
    asp_enb = {0, 20, 30, 36, 40, 45, 60, 72, 80, 90, 108, 120, 135, 144, 150, 160, 180}
    asp_pnt = {
        0: 4, 180: 3, 135: 0.5, 90: 2, 45: 1, 120: 3, 150: 0.5, 60: 2, 30: 1,
        72: 6, 108: 1, 144: 4, 36: 2, 40: 6, 160: 2, 80: 4, 20: 1, 100: 0, 140: 0,
        360/7: 0, 1080/7: 0, 720/7: 0, 360/14: 0
    }
    _s = {
        -1: 'ø', 0: 'q', 180: 'w', 135: 'u', 90: 'r', 45: 'y', 120: 'e', 150: 'K', 60: 't', 30: 'i',
        72: 'Q', 108: 'TD', 144: 'BQ', 36: 'D', 40: 'N', 160: 'KN', 80: 'BN', 20: 'PN', 100: 'SG', 140: 'SD',
        360/7: 'S', 1080/7: 'TS', 720/7: 'BS', 360/14: 'PS'
    }
    _c = {
        -1: '#008000', 0: '#008000', 180: '#000000', 135: '#000000', 90: '#000000', 45: '#000000',
        120: '#F00000', 150: '#F00000', 60: '#F00000', 30: '#F00000',
        72: '#00C800', 108: '#00C800', 144: '#00C800', 36: '#00C800',
        40: '#0080FF', 160: '#0080FF', 80: '#0080FF', 20: '#0080FF', 100: '#0080FF', 140: '#0080FF',
        360/7: '#9400D3', 1080/7: '#9400D3', 720/7: '#9400D3', 360/14: '#9400D3'
    }
    _t = {
        -1: 1, 0: 1, 180: 1, 135: 1, 90: 1, 45: 1, 120: 1, 150: 0, 60: 1, 30: 1,
        72: 0, 108: 0, 144: 0, 36: 0, 40: 0, 160: 0, 80: 0, 20: 0, 100: 0, 140: 0,
        360/7: 0, 1080/7: 0, 720/7: 0, 360/14: 0
    }
    _d = {
        -1: None, 0: None, 180: None, 135: 5, 90: None, 45: 1, 120: None, 150: 5, 60: None, 30: 1,
        72: None, 108: 5, 144: None, 36: 1, 40: None, 160: 5, 80: None, 20: 1, 100: (5, 1, 1), 140: (5, 1, 1),
        360/7: None, 1080/7: 5, 720/7: None, 360/14: 1
    }
    tab_4_mx = {0: 1, 1: 0.5, 2: 0.3, 3: 0.2, 4: 0.1}
    asp_sam = {0: {0, 1}, 1: {2, 3, 4}, 2: {5, 11, 23, 12, 56}, 3: {6, 7, 15}, 4: {8, 9, 57}}
    pg_tit = ''
    flag, level = 0, 4

    def __init__(self, conf, cos_st=None):
        self.asp_src = {}
        self.asp_enb = set()
        self.asp_pnt = {}
        self._s, self._c, self._t, self._d = {}, {}, {}, {}
        self.tab_4_pl, self.tab_4_cs, self.tab_4_mx = {}, {}, {}

        self.pth = conf.get_app_pth()
        self.var = conf.get_act_var()
        self.cos_st = cos_st

        self.set_act_var = conf.set_act_var

        self.load_apg(self.var[3])

    def get_st_flag(self): return self.flag & 2 == 2
    def swi_st_flag(self): self.flag = self.flag ^ 2

    def get_pg_tit(self): return self.pg_tit

    def set_pg_tit(self, val):
        self.pg_tit = val
        self.flag = self.flag | 1

    def get_pl_src(self): return self.pl_src
    def get_asp_src(self): return self.asp_src

    def get_asp_enb(self): return self.asp_enb

    def set_asp_enb(self, asp=None, mode=1):
        if asp is None:
            self.asp_enb.clear()
            if mode:
                self.asp_enb |= set(self.asp_src.values())
        else:
            self.asp_enb.add(asp) if mode else self.asp_enb.discard(asp)

    def get_asp_pnt(self): return self.asp_pnt

    def set_asp_pnt(self, asp, val):
        self.asp_pnt[asp] = val
        self.flag = self.flag | 1

    def get_asp_prop(self, asp=None, mode=1):
        if mode == 1:
            src_seq = self._s
        elif mode == 2:
            src_seq = self._c
        elif mode == 3:
            src_seq = self._t
        elif mode == 4:
            src_seq = self._d
        else:
            return None

        if asp is None:
            return src_seq
        else:
            return src_seq[asp] if asp in src_seq else src_seq[-1]

    def get_asp_orb(self, mode=0):
        if mode == 2:
            return self.tab_4_mx
        elif mode == 1:
            return self.tab_4_cs
        else:
            return self.tab_4_pl

    def set_asp_orb(self, asp=None, ind=None, val=1):
        if asp is None:
            self.tab_4_mx[ind] = val
        elif ind is None:
            self.tab_4_cs[asp] = val
        else:
            self.tab_4_pl[(asp, ind)] = val
        self.flag = self.flag | 1

    def calc_blt_page(self):
        self.asp_src.clear()
        self.asp_enb.clear()
        self.asp_pnt.clear()
        self._s.clear()
        self._c.clear()
        self._t.clear()
        self._d.clear()
        self.tab_4_pl.clear()
        self.tab_4_cs.clear()
        self.tab_4_mx.clear()

        for i in AspectPage.asp_src:
            self.asp_src[i] = AspectPage.asp_src[i]

        asp_val = AspectPage.asp_src.values()
        for i in asp_val:
            self.asp_pnt[i] = AspectPage.asp_pnt[i]
            self._s[i] = AspectPage._s[i]
            self._c[i] = AspectPage._c[i]
            self._t[i] = AspectPage._t[i]
            self._d[i] = AspectPage._d[i]
        self.asp_enb |= AspectPage.asp_enb
        self._s[-1] = AspectPage._s[-1]
        self._c[-1] = AspectPage._c[-1]
        self._t[-1] = AspectPage._t[-1]
        self._d[-1] = AspectPage._d[-1]

        for i in AspectPage.tab_4_mx:
            self.tab_4_mx[i] = AspectPage.tab_4_mx[i]

        for i in self.pl_src.values():
            for j in asp_val:
                orb = ut.deflect(j, self.level)
                for f in range(5):
                    if i in self.asp_sam[f]:
                        self.tab_4_pl[(j, i)] = round(orb - 0.075*f*orb, 4)
                if not (j, i) in self.tab_4_pl:
                    self.tab_4_pl[(j, i)] = round(0.65*orb, 4)

        for i in asp_val:
            orb = ut.deflect(i, self.level)
            self.tab_4_cs[i] = round(0.6*orb, 4)

        if self.flag & 2:
            self.apply_stat()

    def apply_stat(self):
        if not self.cos_st:
            return None
        for i in self.tab_4_pl:
            if i[1] in {11, 23, 12, 56}:
                continue
            elif i[1] in self.cos_st:
                if self.cos_st[i[1]] >= 7:
                    if self.flag & 2:
                        self.tab_4_pl[i] = round(self.tab_4_pl[i]*1.05, 4)
                    else:
                        self.tab_4_pl[i] = round(self.tab_4_pl[i]/1.05, 4)
                elif self.cos_st[i[1]] <= -7:
                    if self.flag & 2:
                        self.tab_4_pl[i] = round(self.tab_4_pl[i]*0.95, 4)
                    else:
                        self.tab_4_pl[i] = round(self.tab_4_pl[i]/0.95, 4)

    def use_sam(self, sam):
        self.asp_enb.clear()
        self.asp_enb |= sam & set(self.asp_src.values())
        self.flag = self.flag | 1

    def upd_asp(self, asp, sym, f_type, col, dash):
        asp_val = self.asp_src.values()
        if asp not in asp_val:
            buf = list(asp_val)
            buf.append(asp)
            self.asp_src.clear()
            ind = 0
            for i in sorted(buf):
                self.asp_src[ind] = i
                ind += 1
            self.asp_enb.add(asp)
            for i in self.pl_src.values():
                self.tab_4_pl[(asp, i)] = 1.0
            self.tab_4_cs[asp] = 1.0
            self.asp_pnt[asp] = 0
            if asp == 0:
                self.tab_4_mx.clear()
                for i in AspectPage.tab_4_mx:
                    self.tab_4_mx[i] = AspectPage.tab_4_mx[i]
        self._s[asp] = sym
        self._c[asp] = col
        self._t[asp] = f_type
        self._d[asp] = dash
        self.flag = self.flag | 1

    def del_asp(self, asp):
        buf = list(self.asp_src.values())
        buf.remove(asp)
        self.asp_src.clear()
        ind = 0
        for i in sorted(buf):
            self.asp_src[ind] = i
            ind += 1
        self.asp_enb.discard(asp)
        for i in self.pl_src.values():
            del self.tab_4_pl[(asp, i)]
        del self.tab_4_cs[asp]
        del self.asp_pnt[asp]
        if asp == 0:
            self.tab_4_mx.clear()
        del self._s[asp]
        del self._t[asp]
        del self._c[asp]
        del self._d[asp]
        self.flag = self.flag | 1

    def dump_apg(self):
        if self.flag & 1 and self.pg_tit != '':
            enc = ['Aspect source', json.dumps(list(self.asp_src.items()))]
            enc += ['Aspect enable', json.dumps(list(self.asp_enb))]
            asp_val = self.asp_src.values()
            sep_tab = {i: [] for i in asp_val}
            for i in asp_val:
                for j in self.tab_4_pl:
                    if j[0] == i:
                        sep_tab[i].append([j[1], self.tab_4_pl[j]])
            for i in sep_tab:
                sep_tab[i] = json.dumps(sep_tab[i])
            enc += ['Orbs table', sep_tab]
            enc += ['For cuspids', json.dumps(list(self.tab_4_cs.items()))]
            enc += ['For stars', json.dumps(list(self.tab_4_mx.items()))]
            enc += ['Aspect point', json.dumps(list(self.asp_pnt.items()))]
            enc += ['Symbol', json.dumps(list(self._s.items()))]
            enc += ['Color', json.dumps(list(self._c.items()))]
            enc += ['Font type', json.dumps(list(self._t.items()))]
            enc += ['Dash', json.dumps(list(self._d.items()))]
            with open('%s/%s.json' % (self.pth[3], self.pg_tit), 'w') as fp:
                json.dump(enc, fp, separators=(',\n', ': '))
                fp.close()
            self.flag = self.flag ^ 1

    def load_apg(self, pg_tit=''):
        self.flag = self.flag ^ 1 if self.flag & 1 else self.flag
        check = 0
        try:
            with open('%s/%s.json' % (self.pth[3], pg_tit)) as fp:
                src_data = json.load(fp)
                fp.close()
            for i in range(1, len(src_data), 2):
                if src_data[i-1] == 'Aspect source':
                    self.asp_src.clear()
                    dec = dict(json.loads(src_data[i]))
                    for j in dec:
                        self.asp_src[j] = dec[j]
                    check |= 1
                elif src_data[i-1] == 'Aspect enable':
                    self.asp_enb.clear()
                    self.asp_enb |= set(json.loads(src_data[i]))
                    check |= 2
                elif src_data[i-1] == 'Orbs table':
                    self.tab_4_pl.clear()
                    dec = dict(src_data[i])
                    for j in dec:
                        for k in json.loads(dec[j]):
                            self.tab_4_pl[(float(j), k[0])] = k[1]
                    check |= 4
                elif src_data[i-1] == 'For cuspids':
                    self.tab_4_cs.clear()
                    dec = dict(json.loads(src_data[i]))
                    for j in dec:
                        self.tab_4_cs[j] = dec[j]
                    check |= 8
                elif src_data[i-1] == 'For stars':
                    self.tab_4_mx.clear()
                    dec = dict(json.loads(src_data[i]))
                    for j in dec:
                        self.tab_4_mx[j] = dec[j]
                    check |= 16
                elif src_data[i-1] == 'Aspect point':
                    self.asp_pnt.clear()
                    dec = dict(json.loads(src_data[i]))
                    for j in dec:
                        self.asp_pnt[j] = dec[j]
                    check |= 32
                elif src_data[i-1] == 'Symbol':
                    self._s.clear()
                    self._s[-1] = 'ø'
                    dec = dict(json.loads(src_data[i]))
                    for j in dec:
                        self._s[j] = dec[j]
                    check |= 64
                elif src_data[i-1] == 'Color':
                    self._c.clear()
                    self._c[-1] = '#008000'
                    dec = dict(json.loads(src_data[i]))
                    for j in dec:
                        self._c[j] = dec[j]
                    check |= 128
                elif src_data[i-1] == 'Font type':
                    self._t.clear()
                    self._t[-1] = 1
                    dec = dict(json.loads(src_data[i]))
                    for j in dec:
                        self._t[j] = dec[j]
                    check |= 256
                elif src_data[i-1] == 'Dash':
                    self._d.clear()
                    self._d[-1] = None
                    dec = dict(json.loads(src_data[i]))
                    for j in dec:
                        self._d[j] = tuple(dec[j]) if type(dec[j]) is list else dec[j]
                    check |= 512
            self.pg_tit = pg_tit
            self.set_act_var(3, self.pg_tit)
        except BaseException as error:
            if pg_tit != '':
                ut.error_log(error)

        if check != 1023:
            self.calc_blt_page()
            self.pg_tit = ''
            self.set_act_var(3, self.pg_tit)

# -------------------------------------------------------------------------------------------------------------------- #
