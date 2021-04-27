# -------------------------------------------------------------------------------------------------------------------- #

import core.utilities as ut
import json
import swisseph as swe

# @formatter:off


class AspectTable:
    cls_3_cfg = {
        (90, 90, 180): [3, 1], (135, 135, 90): [4, 1], (45, 45, 90): [5, 1],
        (120, 120, 120): [6, 2], (60, 60, 120): [7, 2], (150, 150, 60): [8, 2], (30, 30, 60): [9, 2],
        (72, 72, 144): [10, 3], (144, 144, 72): [11, 3], (108, 108, 144): [12, 3], (36, 36, 72): [13, 3],
        (40, 40, 80): [14, 4], (80, 80, 160): [15, 4], (160, 160, 40): [16, 4], (20, 20, 40): [17, 4]
    }
    cls_3_ind = {0: set(range(3, 18)) ^ {6}, 1: {7, 8, 9, 10, 11, 12, 13}}
    ext_3_cfg = {
        (100, 100, 160): [18, 4], (140, 140, 80): [19, 4],
        (360/7, 360/7, 720/7): [70, 9], (720/7, 720/7, 1080/7): [71, 9],
        (1080/7, 1080/7, 360/7): [72, 9], (180/7, 180/7, 360/7): [73, 9]
    }
    cls_4_cfg = {
        (90, 90, 90, 90, 180, 180): [2, 1, [3]],
        (45, 45, 135, 135, 90, 180): [20, 1, [4, 5]], (45, 45, 45, 135, 90, 90): [21, 1, [5]],
        (60, 60, 120, 120, 120, 180): [22, 5, [6, 7]], (60, 60, 60, 180, 120, 120): [23, 5, [7]],
        (60, 120, 60, 120, 180, 180): [24, 5, []], (30, 30, 150, 150, 60, 180): [25, 5, [8, 9]],
        (30, 30, 30, 90, 60, 60): [26, 5, [9]],
        (36, 36, 36, 108, 72, 72): [27, 3, [13]],
        (36, 36, 144, 144, 72, 180): [28, 6, [11, 13]], (72, 72, 108, 108, 144, 180): [29, 6, [10, 12]],
        (72, 36, 72, 180, 108, 108): [30, 6, []], (72, 108, 72, 108, 180, 180): [31, 6, []],
        (40, 40, 140, 140, 80, 180): [32, 7, [14, 19]], (80, 80, 100, 100, 160, 180): [33, 7, [15, 18]],
        (20, 20, 160, 160, 40, 180): [34, 7, [16, 17]],
        (40, 40, 40, 120, 80, 80): [35, 8, [14]], (80, 80, 80, 120, 160, 160): [36, 8, [15]],
        (20, 20, 20, 60, 40, 40): [37, 8, [17]], (40, 20, 40, 100, 60, 60): [68, 8, []]
    }
    ext_4_cfg = {
        (45, 90, 45, 180, 135, 135): [38, 1, []], (90, 45, 90, 135, 135, 135): [39, 1, []],
        (45, 135, 45, 135, 180, 180): [40, 1, []],
        (30, 60, 30, 120, 90, 90): [41, 5, []], (60, 30, 60, 150, 90, 90): [42, 5, []],
        (30, 90, 30, 150, 120, 120): [43, 5, []], (30, 120, 30, 180, 150, 150): [44, 5, []],
        (90, 30, 90, 150, 120, 120): [45, 5, []], (120, 30, 120, 90, 150, 150): [46, 5, []],
        (30, 150, 30, 150, 180, 180): [47, 5, []], (60, 90, 60, 150, 150, 150): [48, 5, []],
        (90, 60, 90, 120, 150, 150): [49, 5, []],
        (36, 72, 36, 144, 108, 108): [50, 3, []], (108, 36, 108, 108, 144, 144): [51, 3, []],
        (36, 144, 36, 144, 180, 180): [52, 6, []], (36, 108, 36, 180, 144, 144): [53, 6, []],
        (40, 140, 40, 140, 180, 180): [54, 7, []], (80, 100, 80, 100, 180, 180): [55, 7, []],
        (40, 100, 40, 180, 140, 140): [56, 7, []], (80, 20, 80, 180, 100, 100): [57, 7, []],
        (20, 160, 20, 160, 180, 180): [58, 7, []], (20, 140, 20, 180, 160, 160): [59, 7, []],
        (80, 40, 80, 160, 120, 120): [60, 8, []], (40, 80, 40, 160, 120, 120): [61, 8, []],
        (120, 40, 120, 80, 160, 160): [62, 8, []], (40, 120, 40, 160, 160, 160): [63, 8, []],
        (60, 40, 60, 160, 100, 100): [64, 8, []], (40, 60, 40, 140, 100, 100): [65, 8, []],
        (60, 80, 60, 160, 140, 140): [66, 8, []], (80, 60, 80, 140, 140, 140): [67, 8, []],
        (80, 100, 80, 100, 180, 180): [69, 7, []]
    }
    sam_cfg = {
        0: {0}, 1: {180, 90, 135, 45}, 2: {120, 60, 150, 30}, 3: {72, 144, 108, 36}, 4: {40, 80, 160, 20, 100, 140},
        9: {360/7, 720/7, 1080/7, 180/7}
    }
    cfg_cor = {
        0: {0: 1}, 1: {180: 2, 90: 3, 135: 4, 45: 5}, 2: {120: 6, 60: 7, 150: 8, 30: 9},
        3: {72: 10, 144: 11, 108: 12, 36: 13}, 4: {40: 14, 80: 15, 160: 16, 20: 17}
    }
    ind_cor = {
        0: 0, 1: 0, 2: 180, 3: 90, 4: 135, 5: 45, 6: 120, 7: 60, 8: 150, 9: 30,
        10: 72, 11: 144, 12: 108, 13: 36, 14: 0, 15: 80, 16: 160, 17: 20
    }
    asp_maj = {0, 180, 90, 120, 60, 72, 144, 40, 80}
    cfg_maj = {0, 1, 2, 3, 6, 7, 10, 11, 14, 15}
    fic_pl = {11, 23, 12, 56}
    fic_sam = {
        0: {2: {1, 2, 3, 6, 7, 10, 11, 14, 15}, 1: {0, 4, 5, 8, 9, 12, 13, 16, 17}},
        1: {2: {1, 2, 3, 6, 7, 10, 14}, 1: {0, 4, 5, 8, 9, 11, 12, 13, 17, 68}}
    }
    src_sam, src_seq = None, None
    asp_sam, asp_seq = None, None
    zero = None
    shw_cfg = None
    din_pl_enb = None
    asp_num = 0

    def __init__(self, abo, apg, conf, data):
        self.base_pl = abo.get_base_pl()
        self.main_pl = self.base_pl ^ self.fic_pl
        self.cat_pl = abo.get_cat_pl()
        self.pl_enb = abo.get_pl_enb()
        self.pl_crd = abo.get_pl_crd()
        self.pl_sgn = abo.get_pl_sgn()
        self.cs_crd = abo.get_cs_crd()

        self.get_jul_day = abo.get_jul_day

        self.asp_src = apg.get_asp_src()
        self.asp_enb = apg.get_asp_enb()
        self.asp_pnt = apg.get_asp_pnt()
        self.orb_4pl = apg.get_asp_orb()
        self.orb_4mx = apg.get_asp_orb(2)

        self.pth = conf.get_app_pth()
        self.var = conf.get_act_var()
        self.data = data

        self.tab_4pl = {}
        self.tab_4mx = {0: {}, 1: {}}
        self.asp_fld = {}
        self.asp_cfg = {}
        self.acf_bnd = {}
        self.fic_src = {0: {}, 1: {}}
        self.rex_pit = {0: [], 1: []}
        self.maj_are = 0
        self.stm_sgn = set()
        self.top_pln = {0: set(), 1: set()}

        self.load_ext_acf()
        self.reload()

    def get_tab_4pl(self): return self.tab_4pl
    def get_tab_4mx(self): return self.tab_4mx
    def get_asp_fld(self): return self.asp_fld
    def get_asp_num(self): return self.asp_num
    def get_asp_cfg(self): return self.asp_cfg
    def get_acf_bnd(self): return self.acf_bnd
    def get_fic_src(self): return self.fic_src
    def get_rex_pit(self): return self.rex_pit
    def get_maj_are(self): return self.maj_are
    def get_stm_sgn(self): return self.stm_sgn
    def get_top_pln(self): return self.top_pln

    def reload(self):
        self.calc_tab_4pl()
        if self.var[22]:
            self.calc_tab_4mx()
        self.calc_all_cfg(0)
        self.calc_asp_fld()
        self.calc_fic_src()
        self.calc_rex_pit()
        self.calc_all_cfg()

    def calc_tab_4pl(self):
        self.tab_4pl.clear()
        self.src_sam = {i: {} for i in range(10)}
        self.src_seq = {i: set() for i in range(10)}

        patch = self.data[2] if self.data[2] else {}
        asp_val = set(self.asp_src.values())
        pl_crd = sorted(self.pl_crd)

        for i in pl_crd:
            for j in pl_crd:
                if i == j:
                    continue
                else:
                    if (j, i) in self.tab_4pl:
                        continue
                    else:
                        if (i, j) in patch and patch[(i, j)][1] in asp_val:
                            asp = patch[(i, j)]
                        else:
                            tag = 't%d%d' % (i, j)
                            asp = self.pl_crd[i] - self.pl_crd[j]  # [abs val, asp val, orb, acc(-1/0/1), tag]
                            asp = [abs(asp), -1, 0, 0, tag] if abs(asp) <= 180 else [360 - abs(asp), -1, 0, 0, tag]

                            for k in asp_val:
                                or1 = self.orb_4pl[(k, i)] if (k, i) in self.orb_4pl else self.orb_4pl[(k, -4)]
                                or2 = self.orb_4pl[(k, j)] if (k, j) in self.orb_4pl else self.orb_4pl[(k, -4)]
                                orb = max(or1, or2)
                                acc = [0.06375*orb, 0.1275*orb]
                                if k == 0 and asp[0] <= orb:
                                    asp[1] = k
                                    asp[2] = asp[0]
                                    if asp[0] <= acc[0]:
                                        asp[3] = 1
                                    elif (orb - acc[1]) <= asp[0] <= orb:
                                        asp[3] = -1
                                elif (k - orb) <= asp[0] <= (k + orb):
                                    asp[1] = k
                                    asp[2] = abs(asp[0] - k)
                                    if (k - acc[0]) <= asp[0] <= (k + acc[0]):
                                        asp[3] = 1
                                    elif ((k + orb - acc[1]) <= asp[0] <= (k + orb) or
                                          (k - orb) <= asp[0] <= (k - orb + acc[1])):
                                        asp[3] = -1
                        self.tab_4pl[(i, j)] = asp
                        if i in self.base_pl and j in self.base_pl:
                            self.add_cell((i, j), self.src_sam, self.src_seq)

    def calc_tab_4mx(self):
        self.tab_4mx[0].clear()
        self.tab_4mx[1].clear()

        if not self.orb_4mx:
            return None
        jul_day = self.get_jul_day()
        buf = {}

        for i in range(1, 1139):
            if i == 106:
                continue
            fs = swe.fixstar2_ut('%d' % i, jul_day)
            if fs[1][0] != ',':
                mag = swe.fixstar2_mag('%d' % i)
                ind = int(mag)
                if ind < 0:
                    ind = 0
                if ind > 4:
                    ind = 4
                for j in self.cat_pl:
                    asp = abs(self.pl_crd[j] - fs[0][0])
                    if asp > 180:
                        asp = 360 - asp
                    if asp <= self.orb_4mx[ind]:
                        if j in self.tab_4mx[0]:
                            if mag < buf[j]:
                                self.tab_4mx[0][j] = fs[1].split(',')[0]
                                buf[j] = mag
                        else:
                            self.tab_4mx[0][j] = fs[1].split(',')[0]
                            buf[j] = mag
                for j in self.cs_crd:
                    asp = abs(self.cs_crd[j] - fs[0][0])
                    if asp > 180:
                        asp = 360 - asp
                    if asp <= self.orb_4mx[ind]:
                        self.tab_4mx[1][j] = fs[1].split(',')[0]

    def add_cell(self, key, sam, seq):
        asp = self.tab_4pl[key][1]
        ind = -1
        if asp in self.sam_cfg[0]:
            ind = 0
        elif asp in self.sam_cfg[1]:
            ind = 1
        elif asp in self.sam_cfg[2]:
            ind = 2
        elif asp in self.sam_cfg[3]:
            ind = 3
        elif asp in self.sam_cfg[4]:
            ind = 4
        elif asp in self.sam_cfg[9]:
            ind = 9

        if ind > -1:
            sam[ind][key] = self.tab_4pl[key]
            seq[ind].add(key[0])
            seq[ind].add(key[1])
            if ind in {1, 2}:
                sam[5][key] = self.tab_4pl[key]
                seq[5].add(key[0])
                seq[5].add(key[1])
            if ind in {1, 3}:
                sam[6][key] = self.tab_4pl[key]
                seq[6].add(key[0])
                seq[6].add(key[1])
            if ind in {1, 4}:
                sam[7][key] = self.tab_4pl[key]
                seq[7].add(key[0])
                seq[7].add(key[1])
            if ind in {2, 4}:
                sam[8][key] = self.tab_4pl[key]
                seq[8].add(key[0])
                seq[8].add(key[1])

    def calc_all_cfg(self, mode=1):
        self.asp_cfg.clear()
        self.acf_bnd.clear()
        self.shw_cfg = {}
        for i in {0, 1}:
            self.asp_cfg[i] = []
        for i in self.cls_3_cfg.values():
            self.asp_cfg[i[0]] = []
        for i in self.ext_3_cfg.values():
            self.asp_cfg[i[0]] = []
        for i in self.cls_4_cfg.values():
            self.asp_cfg[i[0]] = []
        for i in self.ext_4_cfg.values():
            self.asp_cfg[i[0]] = []

        if not mode:
            self.maj_are = 0
            self.top_pln[0].clear()
            self.top_pln[1].clear()

        if mode:
            self.asp_sam = {i: {} for i in range(10)}
            self.asp_seq = {i: set() for i in range(10)}

            self.din_pl_enb = self.pl_enb if self.var[8] & 1 else self.base_pl & self.pl_enb

            for i in self.tab_4pl:
                if i[0] in self.din_pl_enb and i[1] in self.din_pl_enb:
                    asp = self.tab_4pl[i][1]
                    acc = self.tab_4pl[i][3]
                    if asp == -1 or asp not in self.asp_enb:
                        continue
                    if not(self.var[4] == 2 or acc == self.var[4]):
                        continue
                    self.add_cell(i, self.asp_sam, self.asp_seq)

        self.calc_zero_cfg(mode)

        for i in self.cls_3_cfg:
            self.calc_asp_cfg(i, mode)

        if self.var[8] & 2:
            for i in self.ext_3_cfg:
                self.calc_asp_cfg(i, mode)

        for i in self.cls_4_cfg:
            self.calc_asp_cfg(i, mode)

        if self.var[8] & 2:
            for i in self.ext_4_cfg:
                self.calc_asp_cfg(i, mode)

    def calc_zero_cfg(self, mode=1):
        self.stm_sgn.clear()
        self.zero, src_zero = [], []

        if mode:
            sam = self.asp_sam[0]
            seq = self.asp_seq[0]
        else:
            sam = self.src_sam[0]
            seq = self.src_seq[0]

        for i in seq:
            res = {i}
            for j in sam:
                if i in j:
                    k = j[0] if i == j[1] else j[1]
                    res.add(k)
            src_zero.append(res)

        for i in src_zero:
            if len(i) > 2:
                for j in src_zero:
                    if i == j:
                        continue
                    if i & j:
                        for k in i ^ j:
                            i.add(k)
        for i in src_zero:
            if i not in self.zero:
                self.zero.append(i)

        for i in self.zero:
            j = len(i)
            if j < 3:
                continue
            cfg = self.sort_by_crd(i)
            if j == 3 and cfg not in self.asp_cfg[0]:
                self.asp_cfg[0].append(cfg)
                self.acf_bnd[tuple(cfg)] = i
                if not mode and not self.maj_are:
                    self.set_maj_are(0, cfg)
            elif j > 3 and cfg not in self.asp_cfg[1]:
                self.asp_cfg[1].append(cfg)
                self.acf_bnd[tuple(cfg)] = i
                if not mode and not self.maj_are:
                    self.set_maj_are(1, cfg)
                for k in cfg:
                    self.stm_sgn.add(self.pl_sgn[k])

    def calc_asp_cfg(self, asp, mode=1):
        src_cfg, ext = [], []
        swi = 1 if len(asp) == 3 else 0

        if swi:
            spec = self.cls_3_cfg[asp] if asp in self.cls_3_cfg else self.ext_3_cfg[asp]
        else:
            spec = self.cls_4_cfg[asp] if asp in self.cls_4_cfg else self.ext_4_cfg[asp]
            ext = spec[2]

        if spec[1] == -1:
            sam = {}
            seq = set()
            for i in self.tab_4pl:
                if mode:
                    cond = i[0] in self.din_pl_enb and i[1] in self.din_pl_enb and self.tab_4pl[i][1] in asp
                else:
                    cond = i[0] in self.base_pl and i[1] in self.base_pl and self.tab_4pl[i][1] in asp
                if cond:
                    sam[i] = self.tab_4pl[i]
                    seq.add(i[0])
                    seq.add(i[1])
        else:
            if mode:
                sam = self.asp_sam[spec[1]]
                seq = self.asp_seq[spec[1]]
            else:
                sam = self.src_sam[spec[1]]
                seq = self.src_seq[spec[1]]

        for i in seq:
            pl = {}
            for j in sam:
                if i in j and sam[j][1] == asp[0]:
                    pl[1] = j[0] if i == j[1] else j[1]
                    for k in sam:
                        if pl[1] in k and sam[k][1] == asp[1]:
                            pl[2] = k[0] if pl[1] == k[1] else k[1]
                            key = 0
                            if (i, pl[2]) in sam:
                                key = (i, pl[2])
                            elif (pl[2], i) in sam:
                                key = (pl[2], i)
                            pl[2] = pl[2]
                            if swi:
                                res = {i, pl[1], pl[2]}
                                if key in sam and sam[key][1] == asp[2] and res not in src_cfg:
                                    src_cfg.append(res)
                            else:
                                if key not in sam or sam[key][1] != asp[4]:
                                    continue
                                for n in sam:
                                    if pl[2] in n and sam[n][1] == asp[2]:
                                        pl[3] = n[0] if pl[2] == n[1] else n[1]
                                        key = 0
                                        if (pl[1], pl[3]) in sam:
                                            key = (pl[1], pl[3])
                                        elif (pl[3], pl[1]) in sam:
                                            key = (pl[3], pl[1])
                                        if key not in sam or sam[key][1] != asp[5]:
                                            continue
                                        key = 0
                                        if (i, pl[3]) in sam:
                                            key = (i, pl[3])
                                        elif (pl[3], i) in sam:
                                            key = (pl[3], i)
                                        res = {i, pl[1], pl[2], pl[3]}
                                        if key in sam and sam[key][1] == asp[3] and res not in src_cfg:
                                            src_cfg.append(res)

        for i in range(len(src_cfg)):
            if not mode and spec[0] in self.cls_3_ind[0]:
                self.add_top_pl(src_cfg[i], spec[0])
            cfg = src_cfg[i].copy()
            for j in src_cfg[i]:
                for k in self.zero:
                    if j in k:
                        cfg |= k
            cfg = self.sort_by_crd(cfg)
            if cfg not in self.asp_cfg[spec[0]]:
                self.asp_cfg[spec[0]].append(cfg)
                self.acf_bnd[tuple(cfg)] = src_cfg[i]
                if not mode and not self.maj_are:
                    self.set_maj_are(spec[0], src_cfg[i])
            if ext:
                for j in ext:
                    if j in self.asp_cfg:
                        cur = set(cfg)
                        res, shw = [], []
                        for k in self.asp_cfg[j]:
                            shw.append(k) if cur & set(k) == set(k) else res.append(k)
                        self.asp_cfg[j] = res
                        if spec[0] != 2 and shw:
                            if j in self.shw_cfg:
                                for f in shw:
                                    self.shw_cfg[j].append(f)
                            else:
                                self.shw_cfg[j] = shw

    def sort_by_crd(self, seq):
        crd = sorted([[self.pl_crd[i], i] for i in seq])
        return [i[1] for i in crd]

    def set_maj_are(self, ind, cfg):
        if ind in self.cfg_maj:
            seq = set(cfg)
            if self.main_pl & seq == seq:
                self.maj_are = 1

    def add_top_pl(self, cfg, ind):
        k = 0 if ind in self.cls_3_ind[1] else 1
        for i in cfg:
            seq = list(cfg ^ {i})
            p1 = seq[0]
            p2 = seq[1]
            as1 = self.tab_4pl[(min(i, p1), max(i, p1))][1]
            as2 = self.tab_4pl[(min(i, p2), max(i, p2))][1]
            if as1 == as2:
                self.top_pln[k].add(i)

    def calc_asp_fld(self):
        self.asp_num = 0
        for i in range(5):
            self.asp_fld[i] = [0, 0]

        k = {0: 1, 1: 3/2, -1: 2/3}

        for i in self.cfg_cor:
            self.asp_num += len(self.src_sam[i])

            for j in self.src_sam[i].values():
                self.asp_fld[i][0] += k[j[3]] * self.asp_pnt[j[1]]

            if i == 0:
                p = self.asp_pnt[0] if 0 in self.asp_pnt else 0
                self.asp_fld[0][0] += (p - 1) * len(self.asp_cfg[0])
            for j in self.cfg_cor[i]:
                ind = self.cfg_cor[i][j]
                p = self.asp_pnt[j] if j in self.asp_pnt else 0
                self.asp_fld[i][0] += p * len(self.asp_cfg[ind])
                if ind in self.shw_cfg:
                    self.asp_fld[i][0] += p * len(self.shw_cfg[ind])

        self.asp_fld[1][1] = ut.check(self.asp_fld[1][0], self.asp_fld[2][0])
        self.asp_fld[2][1] = ut.check(self.asp_fld[2][0], self.asp_fld[1][0])
        self.asp_fld[3][1] = ut.check(self.asp_fld[3][0], self.asp_fld[4][0])
        self.asp_fld[4][1] = ut.check(self.asp_fld[4][0], self.asp_fld[3][0])

    def calc_fic_src(self):
        for i in {0, 1}:
            for j in self.fic_pl:
                self.fic_src[i][j] = 0

        zero = {i: [] for i in self.fic_pl}

        for i in self.src_seq[0]:
            for j in self.src_sam[0]:
                if i in j and i in self.fic_pl:
                    p = j[0] if i == j[1] else j[1]
                    zero[i].append(p)
                    p = 4 if p in {0, 1} else 3
                    self.fic_src[0][i] += p
                    self.fic_src[1][i] += p
                    if self.src_sam[0][j][3] == 1:
                        self.fic_src[0][i] += 1

        for i in self.fic_pl:
            for j in self.pl_sgn:
                if i == j:
                    continue
                if self.pl_sgn[i] == self.pl_sgn[j] and j not in zero[i]:
                    p = 3 if j in {0, 1} else 2
                    self.fic_src[0][i] += p
                    self.fic_src[1][i] += p

        for i in {1, 2, 3, 4}:
            for j in self.src_seq[i]:
                for k in self.src_sam[i]:
                    if j in k and j in self.fic_pl:
                        if 11 in k and 23 in k:
                            continue
                        asp = self.src_sam[i][k][1]
                        p = [0, 0]
                        if i == 1:
                            p = [2, 2] if asp in {90, 180} else [1, 1]
                        elif i == 2:
                            p = [2, 2] if asp in {60, 120} else [1, 1]
                        elif i == 3:
                            p[0] = 2 if asp in {72, 144} else 1
                            p[1] = 2 if asp in {72, 108} else 1
                        else:
                            if asp in {40, 80}:
                                p[0] = 2
                            elif asp in {20, 160}:
                                p[0] = 1
                            if asp in {40, 100}:
                                p[1] = 2
                            elif asp in {20, 80}:
                                p[1] = 1
                        self.fic_src[0][j] += p[0]
                        self.fic_src[1][j] += p[1]
                        if self.src_sam[i][k][3] == 1:
                            self.fic_src[0][j] += 1

        for i in self.fic_sam:
            for j in self.fic_sam[i]:
                for k in self.fic_sam[i][j]:
                    for n in self.asp_cfg[k]:
                        for t in self.fic_pl:
                            if t in n:
                                self.fic_src[i][t] += j
                    if k in self.shw_cfg:
                        for n in self.shw_cfg[k]:
                            for t in self.fic_pl:
                                if t in n:
                                    self.fic_src[i][t] += j

    def calc_rex_pit(self):
        self.rex_pit[0].clear()
        self.rex_pit[1].clear()
        asp_4pl = {i: [0, 0, 0] for i in self.base_pl}

        for k in self.tab_4pl:
            asp = self.tab_4pl[k][1]
            if asp != -1 and k[0] in self.base_pl and k[1] in self.base_pl:
                asp_4pl[k[0]][0] += self.asp_pnt[asp]
                asp_4pl[k[0]][1] += 1
                asp_4pl[k[1]][0] += self.asp_pnt[asp]
                asp_4pl[k[1]][1] += 1
                if asp in self.asp_maj:
                    asp_4pl[k[0]][2] = 1
                    asp_4pl[k[1]][2] = 1

        for k in self.ind_cor:
            asp = self.ind_cor[k]
            if asp in self.asp_pnt:
                p = self.asp_pnt[asp] if k != 0 else 0.75*self.asp_pnt[asp]
                for j in self.asp_cfg[k]:
                    for i in j:
                        asp_4pl[i][0] += p
                        asp_4pl[i][1] += 1
                        asp_4pl[i][2] = 1
                if k in self.shw_cfg:
                    for j in self.shw_cfg[k]:
                        for i in j:
                            asp_4pl[i][0] += p
                            asp_4pl[i][1] += 1
                            asp_4pl[i][2] = 1

        key, val = [], []
        for i in asp_4pl:
            key.append(i)
            val.append(asp_4pl[i][0] * asp_4pl[i][1])
            if asp_4pl[i][2] == 0:
                self.rex_pit[1].append(i)
        buf = ut.comp_seq(val)
        k = 0
        for i in buf:
            if i == 1:
                self.rex_pit[0].append(key[k])
                break
            k += 1

        if not self.rex_pit[0]:
            buf = sorted(val, reverse=True)
            c1 = ut.check(buf[0], buf[2])
            c2 = ut.check(buf[1], buf[2])
            c3 = ut.check(buf[0], buf[1])
            if c3 < c1 == c2 == 1:
                v1 = buf[0]
                v2 = buf[1]
                k, b = 0, 0
                for i in val:
                    if v1 == i or v2 == i and v1 != v2:
                        self.rex_pit[0].append(key[k])
                        b += 1
                        if b == 2:
                            break
                    elif v1 == v2 == i:
                        self.rex_pit[0].append(key[k])
                        self.rex_pit[0].append(key[k+1])
                        break
                    k += 1

    def dump_ext_acf(self):
        enc3, enc4 = {}, {}

        for i in self.ext_3_cfg:
            enc3[json.dumps(i)] = json.dumps(self.ext_3_cfg[i])
        for i in self.ext_4_cfg:
            enc4[json.dumps(i)] = json.dumps(self.ext_4_cfg[i])

        with open('%s/ext_3_cfg.json' % self.pth[5], 'w') as fp:
            json.dump(enc3, fp, separators=(',\n', ': '))
            fp.close()
        with open('%s/ext_4_cfg.json' % self.pth[5], 'w') as fp:
            json.dump(enc4, fp, separators=(',\n', ': '))
            fp.close()

    def load_ext_acf(self):
        dec3, dec4 = {}, {}
        check = 0

        try:
            with open('%s/ext_3_cfg.json' % self.pth[5]) as fp:
                dec = json.load(fp)
                fp.close()
            for i in dec:
                dec3[tuple(json.loads(i))] = json.loads(dec[i])
            check |= 1

            with open('%s/ext_4_cfg.json' % self.pth[5]) as fp:
                dec = json.load(fp)
                fp.close()
            for i in dec:
                dec4[tuple(json.loads(i))] = json.loads(dec[i])
            check |= 2
        except BaseException as error:
            ut.error_log(error)

        if check == 3:
            self.ext_3_cfg = dec3
            self.ext_4_cfg = dec4
        else:
            self.ext_3_cfg = AspectTable.ext_3_cfg.copy()
            self.ext_4_cfg = AspectTable.ext_4_cfg.copy()

# -------------------------------------------------------------------------------------------------------------------- #
