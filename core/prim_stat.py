# -------------------------------------------------------------------------------------------------------------------- #

import core.utilities as ut

# @formatter:off


class AstroRefBook:
    ess_st = {
        (0, 4): 0, (1, 3): 0, (2, 2): 0, (3, 1): 0, (3, 6): 0, (4, 0): 0, (4, 7): 0, (5, 8): 0,
        (5, 11): 0, (6, 9): 0, (6, 10): 0, (7, 10): 0, (8, 11): 0, (9, 7): 0, (57, 5): 0, (15, 6): 0,
        (0, 10): 1, (1, 9): 1, (2, 8): 1, (3, 7): 1, (3, 0): 1, (4, 6): 1, (4, 1): 1, (5, 2): 1,
        (5, 5): 1, (6, 3): 1, (6, 4): 1, (7, 4): 1, (8, 5): 1, (9, 1): 1, (57, 11): 1, (15, 0): 1,
        (0, 0): 2, (1, 1): 2, (2, 5): 2, (3, 11): 2, (4, 9): 2, (5, 3): 2, (6, 6): 2, (7, 7): 2,
        (8, 10): 2, (9, 4): 2, (11, 2): 2, (23, 8): 2, (12, 7): 2, (56, 1): 2, (57, 2): 2, (15, 8): 2,
        (0, 6): 3, (1, 7): 3, (2, 11): 3, (3, 5): 3, (4, 3): 3, (5, 9): 3, (6, 0): 3, (7, 1): 3,
        (8, 4): 3, (9, 10): 3, (11, 8): 3, (23, 2): 3, (12, 1): 3, (56, 7): 3, (57, 8): 3, (15, 2): 3
    }

    pl_elm = {
        0: {0: 0, 1: 3, 2: 2, 3: 1, 4: 0, 5: 0, 6: 1, 7: 2, 8: 3, 9: 3, 57: 1, 15: 2},
        1: {0: 3, 1: 0, 2: 1, 3: 2, 4: 3, 5: 3, 6: 2, 7: 1, 8: 0, 9: 0, 57: 2, 15: 1}
    }
    bs_4pl = {
        0: {0: 0, 1: 1, 2: 2, 3: 1, 4: 0, 5: 0, 6: 1, 7: 2, 8: 1, 9: 0, 57: 1, 15: 2},
        1: {0: 1, 1: 0, 2: -1, 3: 0, 4: 1, 5: 1, 6: 0, 7: -1, 8: 0, 9: 1, 57: 0, 15: -1}
    }
    pl_4pl = {
        0: {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 57: 57, 15: 15},
        1: {0: 7, 1: 6, 2: 5, 3: 9, 4: 15, 5: 2, 6: 1, 7: 0, 8: 57, 9: 3, 57: 8, 15: 4}
    }
    rel_pl = {
        0: {
            0: {4, 5}, 1: {3, 8}, 2: {15, 7, 57}, 3: {1, 8, 15}, 4: {0, 5, 9}, 5: {0, 4, 8, 15}, 6: {7, 57},
            7: {2, 6, 15}, 8: {1, 3, 5}, 9: {4}, 57: {2, 6}, 15: {2, 3, 5, 7}
        },
        1: {
            0: {1, 7}, 1: {0, 6}, 2: {5}, 3: {4, 9}, 4: {3, 15}, 5: {2, 6}, 6: {1, 5}, 7: {0}, 8: {9, 57},
            9: {3, 8}, 57: {8}, 15: {4}
        }
    }

    el_sign = {0: 0, 1: 1, 2: 2, 3: 3, 4: 0, 5: 1, 6: 2, 7: 3, 8: 0, 9: 1, 10: 2, 11: 3}
    cr_sign = {0: 0, 1: 1, 2: 2, 3: 0, 4: 1, 5: 2, 6: 0, 7: 1, 8: 2, 9: 0, 10: 1, 11: 2}
    zo_sign = {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 1, 8: 2, 9: 2, 10: 2, 11: 2}
    qu_sign = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3}
    ns_sign = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}
    ew_sign = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 0, 10: 0, 11: 0}
    rul_sign = {
        0: {0: 4, 1: 3, 2: 2, 3: 1, 4: 0, 5: 57, 6: 15, 7: 9, 8: 5, 9: 6, 10: 7, 11: 8},
        1: {0: 9, 1: 15, 2: 57, 3: -1, 4: -1, 5: 2, 6: 3, 7: 4, 8: 8, 9: 7, 10: 6, 11: 5}
    }
    det_sign = {
        0: {0: 15, 1: 9, 2: 5, 3: 6, 4: 7, 5: 8, 6: 4, 7: 3, 8: 2, 9: 1, 10: 0, 11: 57},
        1: {0: 3, 1: 4, 2: 8, 3: 7, 4: 6, 5: 5, 6: 9, 7: 15, 8: 57, 9: -1, 10: -1, 11: 2}
    }
    ess_sign = {
        0: {0: 0, 1: 1, 2: 57, 3: 5, 4: 9, 5: 2, 6: 6, 7: 7, 8: 15, 9: 4, 10: 8, 11: 3},
        1: {0: 6, 1: 7, 2: 15, 3: 4, 4: 8, 5: 3, 6: 0, 7: 1, 8: 57, 9: 5, 10: 9, 11: 2}
    }

    rul_deg = dict(zip(range(360), [4, 0, 3, 2, 1, 6, 5, 9, 0, 8, 7, 1, 57, 15]*25 + [4, 0, 3, 2, 1, 6, 5, 9, 0, 8]))
    rul_ter = dict(zip(range(72), [4, 0, 3, 2, 1, 6, 5, 9, 0, 8, 7, 1, 57, 15]*5 + [4, 0]))
    rul_dec = dict(zip(range(36), [4, 0, 3, 2, 1, 6, 5, 9, 0, 8, 7, 1, 57, 15]*2 + [4, 0, 3, 2, 1, 6, 5, 9]))
    exa_deg = {19: 0, 33: 1, 165: 2, 357: 3, 298: 4, 105: 5, 200: 6, 232: 7, 308: 8, 142: 9, 64: 57, 247: 15}
    fal_deg = {199: 0, 213: 1, 345: 2, 177: 3, 118: 4, 285: 5, 20: 6, 52: 7, 128: 8, 322: 9, 244: 57, 67: 15}
    kad_deg = {
        0: {17, 68, 126, 174, 222, 280, 329},
        1: {22, 72, 159, 180, 228, 288, 333}
    }

    mtp_base = {
        'S': 0, 'M': 1, 'C': 2, 'P': 2, 'D': 2, 'S-M': 2, 'S-P': 0, 'M-P': 1, 'C-P': 2, 'P-P': 2, 'S-M-P': 2,
        'C-P-P': 2, 'S-P-P': 0, 'M-P-P': 1
    }

    def __init__(self, abo):
        self.pl_crd = abo.get_pl_crd()
        self.pl_sgn = abo.get_pl_sgn()
        self.pl_hse = abo.get_pl_hse()
        self.cs_sgn = abo.get_cs_sgn()

        self.pl_deg = {}
        self.ess_sym = {0: {}, 1: {}}
        self.ess_deg = {0: {}, 1: {}}

        self.el_4pl = {0: {}, 1: {}}
        self.cr_4pl = {0: {}, 1: {}}
        self.zo_4pl = {0: {}, 1: {}}
        self.qu_4pl = {0: {}, 1: {}}
        self.ns_4pl = {0: {}, 1: {}}
        self.ew_4pl = {0: {}, 1: {}}
        self.al_4cs = {0: {}, 1: {}}

        self.comp_el = {0: {}, 1: {}}
        self.comp_cr = {0: {}, 1: {}}
        self.comp_zo = {0: {}, 1: {}}
        self.comp_dg = {0: {}, 1: {}}

        self.reload()

    def get_pl_elm(self): return self.pl_elm
    def get_bs_4pl(self): return self.bs_4pl
    def get_rel_pl(self): return self.rel_pl
    def get_sg_rul(self): return self.rul_sign
    def get_sg_det(self): return self.det_sign
    def get_sg_ess(self): return self.ess_sign
    def get_dg_rul(self): return self.rul_deg
    def get_kd_deg(self): return self.kad_deg
    def get_tr_rul(self): return self.rul_ter
    def get_dc_rul(self): return self.rul_dec
    def get_mtp_bs(self): return self.mtp_base

    def get_ess_sym(self): return self.ess_sym
    def get_ess_deg(self): return self.ess_deg
    def get_al_4cs(self): return self.al_4cs

    def get_seq_4pl(self, ind=0):
        if ind == 5:
            return self.ew_4pl
        elif ind == 4:
            return self.ns_4pl
        elif ind == 3:
            return self.qu_4pl
        elif ind == 2:
            return self.zo_4pl
        elif ind == 1:
            return self.cr_4pl
        else:
            return self.el_4pl

    def get_com_seq(self, ind=0):
        if ind == 3:
            return self.comp_dg
        elif ind == 2:
            return self.comp_zo
        elif ind == 1:
            return self.comp_cr
        else:
            return self.comp_el

    def reload(self):
        self.calc_ess_sym()
        self.calc_ess_deg()
        self.calc_pl_seq()
        self.calc_compare()

    def calc_ess_sym(self):
        self.ess_sym[0].clear()
        self.ess_sym[1].clear()

        for i in {0, 1}:
            seq = self.pl_hse if i else self.pl_sgn
            for j in seq:
                self.ess_sym[i][j] = self.ess_st[(j, seq[j])] if (j, seq[j]) in self.ess_st else -1

    def calc_ess_deg(self):
        self.ess_deg[0].clear()
        self.ess_deg[1].clear()

        self.pl_deg.clear()
        for i in self.pl_crd:
            self.pl_deg[i] = int(self.pl_crd[i])

        for i in {0, 1}:
            seq = self.fal_deg if i else self.exa_deg
            for j in self.pl_4pl[0]:
                self.ess_deg[i][j] = seq[self.pl_deg[j]] if self.pl_deg[j] in seq else None

    def calc_pl_seq(self):
        self.el_4pl[0].clear()
        self.el_4pl[1].clear()
        self.cr_4pl[0].clear()
        self.cr_4pl[1].clear()
        self.zo_4pl[0].clear()
        self.zo_4pl[1].clear()
        self.qu_4pl[0].clear()
        self.qu_4pl[1].clear()
        self.ns_4pl[0].clear()
        self.ns_4pl[1].clear()
        self.ew_4pl[0].clear()
        self.ew_4pl[1].clear()
        self.al_4cs[0].clear()
        self.al_4cs[1].clear()

        for i in {0, 1}:
            ind = self.pl_hse if i else self.pl_sgn
            for j in ind:
                self.el_4pl[i][j] = self.el_sign[ind[j]]
                self.cr_4pl[i][j] = self.cr_sign[ind[j]]
                self.zo_4pl[i][j] = self.zo_sign[ind[j]]
                self.qu_4pl[i][j] = self.qu_sign[ind[j]]
                self.ns_4pl[i][j] = self.ns_sign[ind[j]]
                self.ew_4pl[i][j] = self.ew_sign[ind[j]]
            seq = self.det_sign[0] if i else self.rul_sign[0]
            for j in self.cs_sgn:
                self.al_4cs[i][j] = seq[self.cs_sgn[j]]

    def calc_compare(self):
        self.comp_el[0] = {0: {}, 1: {}}
        self.comp_el[1] = {0: {}, 1: {}}
        self.comp_cr[0] = {0: {}, 1: {}}
        self.comp_cr[1] = {0: {}, 1: {}}
        self.comp_zo[0] = {0: {}, 1: {}}
        self.comp_zo[1] = {0: {}, 1: {}}
        self.comp_dg[0].clear()
        self.comp_dg[1].clear()

        for i in {0, 1}:
            sam = self.pl_hse if i else self.pl_sgn
            for j in {0, 1}:
                for k in self.pl_4pl[0]:
                    self.comp_el[i][j][k] = (self.pl_elm[j][k] == self.el_sign[sam[k]])
                    self.comp_cr[i][j][k] = (self.bs_4pl[j][k] == self.cr_sign[sam[k]])
                    self.comp_zo[i][j][k] = (self.bs_4pl[j][k] == self.zo_sign[sam[k]])
                    if i == 0:
                        self.comp_dg[j][k] = (self.pl_4pl[j][k] == self.rul_deg[self.pl_deg[k]])


class MapCore:
    ccf_g = {
        'ZM': 1, 'ZS': 0, 'CM': 1, 'CS': 0, 'EMa': 0, 'ESa': 0, 'EMb': 1, 'ESb': 1, 'QMa': 0, 'QSa': 0,
        'QMb': 1, 'QSb': 1, 'HM': 1, 'HS': 1
    }
    ccf_s = {
        'ZM': 6, 'ZS': 3, 'CM': 6, 'CS': 3, 'EMa': 4, 'ESa': 4, 'EMb': 2, 'ESb': 2, 'QMa': 3, 'QSa': 3,
        'QMb': 1, 'QSb': 1, 'HM': 2, 'HS': 2
    }
    calc_pl = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 23, 12, 56, 57, 15}
    fic_pl = {11, 23, 12, 56}
    bs_src = None

    def __init__(self):
        self.el_4ce, self.qu_4ce = {}, {}
        self.cr_4ce, self.zo_4ce = {}, {}
        self.ns_4ce, self.ew_4ce = {}, {}
        self.bs_4ce = {}
        self.map_tp = ''

    def get_el4ce(self): return self.el_4ce
    def get_cr4ce(self): return self.cr_4ce
    def get_zo4ce(self): return self.zo_4ce
    def get_qu4ce(self): return self.qu_4ce
    def get_ns4ce(self): return self.ns_4ce
    def get_ew4ce(self): return self.ew_4ce
    def get_bs4ce(self): return self.bs_4ce

    def calc_core(self, ind, plan_cf, mtp_bs=None):
        self.el_4ce.clear()
        self.cr_4ce.clear()
        self.zo_4ce.clear()
        self.qu_4ce.clear()
        self.ns_4ce.clear()
        self.ew_4ce.clear()
        self.bs_4ce.clear()

        if mtp_bs is None:
            cf = self.ccf_g
            self.map_tp = ''
        else:
            cf = self.ccf_s
            self.calc_map_tp(ind)

        force = {i: 0 for i in range(12)}
        for i in self.calc_pl:
            force[ind[i]] += plan_cf[i]

        el_4ce = [0, 0, 0, 0]
        el_4ce[0] = force[0] + force[4] + force[8]
        el_4ce[1] = force[1] + force[5] + force[9]
        el_4ce[2] = force[2] + force[6] + force[10]
        el_4ce[3] = force[3] + force[7] + force[11]
        cr_4ce = [0, 0, 0]
        cr_4ce[0] = force[0] + force[3] + force[6] + force[9]
        cr_4ce[1] = force[1] + force[4] + force[7] + force[10]
        cr_4ce[2] = force[2] + force[5] + force[8] + force[11]
        zo_4ce = [0, 0, 0]
        zo_4ce[0] = force[0] + force[1] + force[2] + force[3]
        zo_4ce[1] = force[4] + force[5] + force[6] + force[7]
        zo_4ce[2] = force[8] + force[9] + force[10] + force[11]
        qu_4ce = [0, 0, 0, 0]
        qu_4ce[0] = force[0] + force[1] + force[2]
        qu_4ce[1] = force[3] + force[4] + force[5]
        qu_4ce[2] = force[6] + force[7] + force[8]
        qu_4ce[3] = force[9] + force[10] + force[11]
        ns_4ce = [0, 0]
        ns_4ce[0] = qu_4ce[2] + qu_4ce[3]
        ns_4ce[1] = qu_4ce[0] + qu_4ce[1]
        ew_4ce = [0, 0]
        ew_4ce[0] = qu_4ce[0] + qu_4ce[3]
        ew_4ce[1] = qu_4ce[1] + qu_4ce[2]

        el_4ce = {0: el_4ce, 1: ut.comp_seq(el_4ce)}
        cr_4ce = {0: cr_4ce, 1: ut.comp_seq(cr_4ce)}
        zo_4ce = {0: zo_4ce, 1: ut.comp_seq(zo_4ce)}
        qu_4ce = {0: qu_4ce, 1: ut.comp_seq(qu_4ce)}
        ns_4ce = {0: ns_4ce, 1: ut.comp_seq(ns_4ce)}
        ew_4ce = {0: ew_4ce, 1: ut.comp_seq(ew_4ce)}

        for i in range(4):
            self.el_4ce[i] = [el_4ce[0][i], el_4ce[1][i]]
            self.qu_4ce[i] = [qu_4ce[0][i], qu_4ce[1][i]]
            if i < 3:
                self.cr_4ce[i] = [cr_4ce[0][i], cr_4ce[1][i]]
                self.zo_4ce[i] = [zo_4ce[0][i], zo_4ce[1][i]]
            if i < 2:
                self.ns_4ce[i] = [ns_4ce[0][i], ns_4ce[1][i]]
                self.ew_4ce[i] = [ew_4ce[0][i], ew_4ce[1][i]]

        self.bs_src = [0, 0, 0]
        self.bs_calc_step(cf['ZM'], cf['ZS'], self.zo_4ce)
        self.bs_calc_step(cf['EMa'], cf['ESa'], self.el_4ce)
        seq = (self.el_4ce[0][0] + self.el_4ce[2][0], self.el_4ce[1][0] + self.el_4ce[3][0])
        self.bs_calc_step(cf['EMb'], cf['ESb'], list(zip(seq, ut.comp_seq(seq))))
        self.bs_calc_step(cf['CM'], cf['CS'], self.cr_4ce)
        self.bs_calc_step(cf['QMa'], cf['QSa'], self.qu_4ce)
        seq = (self.qu_4ce[0][0] + self.qu_4ce[2][0], self.qu_4ce[1][0] + self.qu_4ce[3][0])
        self.bs_calc_step(cf['QMb'], cf['QSb'], list(zip(seq, ut.comp_seq(seq))))
        self.bs_calc_step(cf['HM'], cf['HS'], self.ns_4ce)
        self.bs_calc_step(cf['HM'], cf['HS'], self.ew_4ce)
        if self.map_tp:
            self.bs_src[mtp_bs[self.map_tp]] += 4

        self.bs_src = {0: self.bs_src, 1: ut.comp_seq(self.bs_src)}
        for i in {0, 1, 2}:
            self.bs_4ce[i] = [self.bs_src[0][i], self.bs_src[1][i]]

    def bs_calc_step(self, mc, sc, seq):
        rsv, num = 1, len(seq)
        for i in range(num):
            if seq[i][1] == 1:
                k = 2 if num > 3 and i > 1 else 0
                self.bs_src[i-k] += mc
                rsv = 0
                break
        if rsv:
            self.bs_src[2] += sc

    def calc_map_tp(self, ind):
        self.map_tp = ''

        force = {i: 0 for i in range(12)}
        for i in self.calc_pl:
            k = 0.5 if i in self.fic_pl else 1
            force[ind[i]] += k

        cell = {0: [ind[0], force[ind[0]]], 1: [ind[1], force[ind[1]]], 2: []}
        for i in force:
            if force[i] >= 3 and i != ind[0] and i != ind[1]:
                cell[2].append(i)

        num = len(cell[2])

        if cell[0][1] >= 3 and cell[1][1] < 2 and num == 0:
            self.map_tp = 'S'
        elif cell[0][1] < 2 and cell[1][1] >= 3 and num == 0:
            self.map_tp = 'M'
        elif cell[0][1] >= 3 and ind[0] == ind[1] and num == 0:
            self.map_tp = 'C'
        elif cell[0][1] < 2 and cell[1][1] < 2 and num == 1:
            self.map_tp = 'P'
        elif cell[0][1] < 2 and cell[1][1] < 2 and num == 0:
            self.map_tp = 'D'

        elif cell[0][1] >= 3 and cell[1][1] >= 3 and ind[0] != ind[1] and num == 0:
            self.map_tp = 'S-M'
        elif cell[0][1] >= 3 and cell[1][1] < 2 and num == 1:
            self.map_tp = 'S-P'
        elif cell[0][1] < 2 and cell[1][1] >= 3 and num == 1:
            self.map_tp = 'M-P'
        elif cell[0][1] >= 3 and ind[0] == ind[1] and num == 1:
            self.map_tp = 'C-P'
        elif cell[0][1] < 2 and cell[1][1] < 2 and num == 2:
            self.map_tp = 'P-P'

        elif cell[0][1] >= 3 and cell[1][1] >= 3 and ind[0] != ind[1] and num == 1:
            self.map_tp = 'S-M-P'
        elif cell[0][1] >= 3 and ind[0] == ind[1] and num == 2:
            self.map_tp = 'C-P-P'
        elif cell[0][1] >= 3 and cell[1][1] < 2 and num == 2:
            self.map_tp = 'S-P-P'
        elif cell[0][1] < 2 and cell[1][1] >= 3 and num == 2:
            self.map_tp = 'M-P-P'


class PrimStat(MapCore):
    scf_g = {
        0: 2, 1: 2, 2: 1.5, 3: 1.5, 4: 1.5, 5: 1, 6: 1, 7: 1, 8: 1,
        9: 1, 11: 0.5, 23: 0.5, 12: 0.5, 56: 0.5, 57: 1, 15: 0.8
    }
    scf_s = {
        0: 2, 1: 2, 2: 1.5, 3: 1.5, 4: 1.5, 5: 1, 6: 1, 7: 1, 8: 1,
        9: 1, 11: 0.5, 23: 0.5, 12: 0.5, 56: 0.5, 57: 1, 15: 1
    }
    alm = None
    head = ''

    def __init__(self, abo, arb, mode=0):
        MapCore.__init__(self)

        self.src_st, self.pln_st = {}, {}
        self.sum_st = 0
        self.core_st = 0

        self.pl_crd = abo.get_pl_crd()
        self.cs_crd = abo.get_cs_crd()
        self.pl_sgn = abo.get_pl_sgn()
        self.pl_hse = abo.get_pl_hse()
        self.cs_sgn = abo.get_cs_sgn()

        self.get_pl_name = abo.get_pl_name

        self.sg_rul = arb.get_sg_rul()
        self.sg_det = arb.get_sg_det()
        self.sg_ess = arb.get_sg_ess()
        self.bs_4pl = arb.get_bs_4pl()
        self.mtp_bs = arb.get_mtp_bs()

        self.ess_sym = arb.get_ess_sym()
        self.ess_deg = arb.get_ess_deg()
        self.el_4pl = arb.get_seq_4pl(0)
        self.cr_4pl = arb.get_seq_4pl(1)
        self.zo_4pl = arb.get_seq_4pl(2)
        self.qu_4pl = arb.get_seq_4pl(3)
        self.ns_4pl = arb.get_seq_4pl(4)
        self.ew_4pl = arb.get_seq_4pl(5)
        self.al_4cs = arb.get_al_4cs()

        self.comp_el = arb.get_com_seq(0)
        self.comp_cr = arb.get_com_seq(1)
        self.comp_zo = arb.get_com_seq(2)
        self.comp_dg = arb.get_com_seq(3)

        self.reload(mode)

    def get_src_st(self): return self.src_st
    def get_pln_st(self): return self.pln_st
    def get_sum_st(self): return self.sum_st
    def get_core_st(self): return self.core_st
    def get_map_tp(self): return self.map_tp

    def reload(self, mode):
        self.sum_st = 0
        self.src_st.clear()
        self.pln_st.clear()

        b1 = mode & 1 == 1
        b2 = mode & 2 == 2
        b12 = mode & 3 == 3

        if b1:
            ind = self.pl_hse
            self.head = 'HOR'
        else:
            ind = self.pl_sgn
            self.head = 'COS'
        if b2:
            plan_cf = self.scf_g
            mtp_bs = None
            self.head += ' GLO'
        else:
            plan_cf = self.scf_s
            mtp_bs = self.mtp_bs
            self.head += ' SCH'
        if b12:
            self.calc_alm(mode)

        self.calc_core(ind, plan_cf, mtp_bs)

        ess_sm = self.ess_sym[b1]
        pos_el = self.comp_el[b1][0]
        neg_el = self.comp_el[b1][1]
        pos_cr = self.comp_cr[b1][0]
        neg_cr = self.comp_cr[b1][1]
        pos_zo = self.comp_zo[b1][0]
        neg_zo = self.comp_zo[b1][1]

        el_4pl = self.el_4pl[b1]
        cr_4pl = self.cr_4pl[b1]
        zo_4pl = self.zo_4pl[b1]
        qu_4pl = self.qu_4pl[b1]
        ns_4pl = self.ns_4pl[b1]
        ew_4pl = self.ew_4pl[b1]
        pos_bs_4pl = self.bs_4pl[0]
        neg_bs_4pl = self.bs_4pl[1]

        if b12:
            pos_dg = self.comp_dg[0]
            neg_dg = self.comp_dg[1]
            exa_dg = self.ess_deg[0]
            fal_dg = self.ess_deg[1]
        else:
            pos_dg, neg_dg = {}, {}
            exa_dg, fal_dg = {}, {}

        for i in self.calc_pl:
            self.src_st[i] = [0, 0]
            if i in self.fic_pl:
                if not b1:
                    if i in {12, 56}:
                        if b2:
                            if self.el_4ce[el_4pl[i]][1] == 1:
                                self.src_st[i][0] += 1
                            if self.cr_4ce[cr_4pl[i]][1] == 1:
                                self.src_st[i][0] += 1
                            if self.zo_4ce[zo_4pl[i]][1] == 1:
                                self.src_st[i][0] += 1
                        else:
                            m1, m2 = 12, 56
                            if i == 56:
                                m1, m2 = 56, 12
                            if ut.check(self.el_4ce[el_4pl[m1]][0], self.el_4ce[el_4pl[m2]][0]) == 1:
                                self.src_st[i][0] += 1
                            if ut.check(self.cr_4ce[cr_4pl[m1]][0], self.cr_4ce[cr_4pl[m2]][0]) == 1:
                                self.src_st[i][0] += 1
                            if ut.check(self.zo_4ce[zo_4pl[m1]][0], self.zo_4ce[zo_4pl[m2]][0]) == 1:
                                self.src_st[i][0] += 1
                            if ess_sm[i] == 3:
                                self.src_st[i][0] -= 1
                        if ess_sm[i] == 2:
                            self.src_st[i][0] += 1
                    else:
                        n1, n2 = 11, 23
                        if i == 23:
                            n1, n2 = 23, 11
                        if b2:
                            k = 2
                        else:
                            k = 1
                            if ut.check(self.zo_4ce[zo_4pl[n1]][0], self.zo_4ce[zo_4pl[n2]][0]) == 1:
                                self.src_st[i][0] += 1
                        if ut.check(self.el_4ce[el_4pl[n1]][0], self.el_4ce[el_4pl[n2]][0]) == 1:
                            self.src_st[i][0] += k
                        if self.ns_4ce[ns_4pl[i]][1] == 1:
                            self.src_st[i][0] += 1
                continue

            if ess_sm[i] == 0:
                self.src_st[i][0] += 3
            elif ess_sm[i] == 1:
                self.src_st[i][1] -= 3
            elif ess_sm[i] == 2:
                self.src_st[i][0] += 3
            elif ess_sm[i] == 3:
                self.src_st[i][1] -= 3
            if (i == 2 and ind[i] == 5) or (i == 57 and ind[i] == 2):
                self.src_st[i][0] += 1  # exception (Mer, Vir), (Pro, Gem): 4
            elif (i == 2 and ind[i] == 11) or (i == 57 and ind[i] == 8):
                self.src_st[i][1] -= 1  # exception (Mer, Psc), (Pro, Sag): -4

            if pos_el[i]:
                self.src_st[i][0] += 2
            elif neg_el[i]:
                self.src_st[i][1] -= 2
            if b2 and i == 1 and ind[i] == 7:
                self.src_st[i][0] -= 1  # exception (Mon, Sco): 1

            if pos_cr[i]:
                self.src_st[i][0] += 2
            if b2 and i == 4 and ind[i] == 3:
                self.src_st[i][0] -= 1  # exception (Mar, Cnc): 1
            if not b2 and neg_cr[i]:
                self.src_st[i][1] -= 2

            if pos_zo[i]:
                self.src_st[i][0] += 1
            if not b2 and neg_zo[i]:
                self.src_st[i][1] -= 1

            if b12:
                if (i, ind[i]) in self.alm:
                    swi = self.alm[(i, ind[i])]
                    self.src_st[i][swi] = self.src_st[i][swi] - 3 if swi else self.src_st[i][swi] + 3

                if pos_dg[i]:
                    self.src_st[i][0] += 1
                if neg_dg[i]:
                    self.src_st[i][1] -= 1

                if exa_dg[i] is not None:
                    self.src_st[i][0] += 0.5
                    if i == exa_dg[i]:
                        self.src_st[i][0] += 1.5
                if fal_dg[i] is not None:
                    self.src_st[i][1] -= 0.5
                    if i == fal_dg[i]:
                        self.src_st[i][0] -= 1.5

            self.st_calc_step(i, 2, self.el_4ce[el_4pl[i]][1])
            self.st_calc_step(i, 2, self.cr_4ce[cr_4pl[i]][1])
            self.st_calc_step(i, 1, self.zo_4ce[zo_4pl[i]][1])
            self.st_calc_step(i, 1, self.qu_4ce[qu_4pl[i]][1])
            self.st_calc_step(i, 1, self.ns_4ce[ns_4pl[i]][1])
            self.st_calc_step(i, 1, self.ew_4ce[ew_4pl[i]][1])
            self.st_calc_step(i, 1, self.bs_4ce[pos_bs_4pl[i]][1])
            if not b2:
                if self.bs_4ce[pos_bs_4pl[i]][1] == -1:
                    self.src_st[i][1] += 1
                if i not in {2, 7, 15} and self.bs_4ce[neg_bs_4pl[i]][1] == 1:
                    self.src_st[i][1] -= 1

            self.pln_st[i] = self.src_st[i][0] + self.src_st[i][1]
            self.sum_st += self.pln_st[i]

        if not b1:
            seq1 = self.calc_pl ^ self.fic_pl
            seq2 = self.calc_pl ^ {12, 56}

            dis = self.sg_rul
            opp = self.sg_det
            ess = self.sg_ess

            for i in self.fic_pl:
                ds1, ds2 = dis[0][ind[i]], dis[1][ind[i]]
                op1, op2 = opp[0][ind[i]], opp[1][ind[i]]
                el, hu = ess[0][ind[i]], ess[1][ind[i]]
                k1 = self.pln_st[ds2] if ds2 != -1 else 0
                k2 = self.pln_st[op2] if op2 != -1 else 0
                self.src_st[i][0] += 0.5*self.pln_st[ds1] + 0.25*k1
                self.src_st[i][0] -= 0.5*self.pln_st[op1] + 0.25*k2
                self.src_st[i][0] += 0.5*self.pln_st[el]
                self.src_st[i][0] -= 0.5*self.pln_st[hu]

                if i == 12:
                    mid = {0: [], 1: []}
                    for j in seq1:
                        if self.pln_st[j] < 0:
                            mid[0].append(self.pln_st[j])
                        elif self.pln_st[j] > 0:
                            mid[1].append(self.pln_st[j])
                    if mid[0]:
                        self.src_st[12][0] -= sum(mid[0])/len(mid[0])
                    if mid[1]:
                        self.src_st[56][0] += sum(mid[1])/len(mid[1])
                elif i == 11:
                    mid = {0: [], 1: []}
                    src, buf, k = [], [], 0
                    for j in seq2:
                        src.append([self.pl_crd[j], j])
                    for j in sorted(src):
                        if j[1] in {11, 23}:
                            k = 0 if j[1] == 23 else 1
                            mid[k] += buf
                            buf = []
                        else:
                            buf.append(self.pln_st[j[1]])
                    mid[k ^ 1] += buf
                    if mid[0]:
                        self.src_st[11][0] += sum(mid[0])/len(mid[0])
                    if mid[1]:
                        self.src_st[23][0] += sum(mid[1])/len(mid[1])

        self.core_st = 2 if b2 else 0
        for i in self.bs_4ce:
            if self.bs_4ce[i][1] == 1:
                if b2 and self.sum_st >= 0:
                    self.core_st = 1
                    break
                elif not b2:
                    self.core_st = 2
                    break

        if not b2 and self.core_st == 2:
            ebs = 4
            for i in range(4):
                if self.el_4ce[i][1] == 1:
                    ebs = i
                    break
            if ebs > 1:
                ebs -= 2
            if self.zo_4ce[ebs][1] == 1 and self.cr_4ce[ebs][1] == 1:
                self.core_st = 1

    def st_calc_step(self, pl, cf, val):
        if val:
            key = 0 if val > 0 else 1
            self.src_st[pl][key] += cf*val

    def calc_alm(self, mode):
        self.alm = {}
        pos_al_cs = self.al_4cs[0]
        neg_al_cs = self.al_4cs[1]
        pos_al_sg = self.sg_rul[0]
        neg_al_sg = self.sg_det[0]

        if mode & 4:
            for i in range(12):
                self.alm[(pos_al_cs[i], i)] = 0
                self.alm[(neg_al_cs[i], i)] = 1
        else:
            sp = {}
            for i in range(12):
                nh = i + 1 if i < 11 else 0
                if i in {0, 3, 6, 9} or self.cs_sgn[i] == self.cs_sgn[nh]:
                    self.alm[(pos_al_cs[i], i)] = 0
                    self.alm[(neg_al_cs[i], i)] = 1
                else:
                    ns = self.cs_sgn[i] + 1 if self.cs_sgn[i] < 11 else 0
                    if ns == self.cs_sgn[nh]:
                        sp[i] = ns*30 - self.cs_crd[i] if ns*30 - self.cs_crd[i] > 0 else ns*30 - self.cs_crd[i] + 360
                        if (30 - sp[i])/sp[i] > 1.5 or (30 - sp[i])/sp[i] == 1.5:
                            self.alm[(pos_al_sg[ns], i)] = 0
                            self.alm[(neg_al_sg[ns], i)] = 1
                        else:
                            self.alm[(pos_al_cs[i], i)] = 0
                            self.alm[(neg_al_cs[i], i)] = 1
                    elif ns + 1 == self.cs_sgn[nh]:
                        self.alm[(pos_al_cs[i], i)] = 0
                        self.alm[(neg_al_cs[i], i)] = 1

    def __str__(self, mode=0):
        if mode:
            ess = {0: [], 1: [], 2: []}
            tit = {0: 'Royal M+7', 1: 'Royal L-7', 2: 'Absolute'}

            buf = {i: self.src_st[i][0] + self.src_st[i][1] for i in self.src_st}
            res = 'Prime status of planets, %s:\n\n' % self.head

            for i in self.src_st:
                if i in self.fic_pl:
                    continue
                elif buf[i] >= 7:
                    ess[0].append(i)
                elif buf[i] <= -7:
                    ess[1].append(i)
                if self.src_st[i][0] == 0 or self.src_st[i][1] == 0:
                    ess[2].append(i)
                res += '%10s %+3d (%+3d, %3d)\n' % (self.get_pl_name(i), buf[i], self.src_st[i][0], self.src_st[i][1])

            res += '\n%9s: %+3d' % ('Total', self.sum_st)
            for i in ess:
                if ess[i]:
                    res += '\n%9s: ' % tit[i]
                    for j in ess[i]:
                        res += '%s ' % self.get_pl_name(j)
        else:
            add = ' +-'
            cst = {0: 'Absent', 1: 'Formed', 2: 'Split'}
            hdr = self.head.split(' ')
            res = 'Cosmogram %s:\n\n' % hdr[1] if hdr[0] == 'COS' else 'Horoscope %s\n\n' % hdr[1]

            res += 'Elements:\n'
            buf = {0: 'Fire', 1: 'Land', 2: 'Air', 3: 'Water'}
            for i in self.el_4ce:
                res += '%5s %4.1f %s\n' % (buf[i], self.el_4ce[i][0], add[self.el_4ce[i][1]])
            res += '\nCrosses:\n'
            buf = {0: 'Cardinal', 1: 'Basic', 2: 'Mutable'}
            for i in self.cr_4ce:
                res += '%8s %4.1f %s\n' % (buf[i], self.cr_4ce[i][0], add[self.cr_4ce[i][1]])
            res += '\nQuadrants:\n'
            buf = {0: 'I', 1: 'II', 2: 'III', 3: 'IV'}
            for i in self.qu_4ce:
                res += '%3s %4.1f %s\n' % (buf[i], self.qu_4ce[i][0], add[self.qu_4ce[i][1]])
            res += '\nZones:\n'
            buf = {0: 'I', 1: 'II', 2: 'III'}
            for i in self.zo_4ce:
                res += '%3s %4.1f %s\n' % (buf[i], self.zo_4ce[i][0], add[self.zo_4ce[i][1]])
            res += '\nHemispheres:\n'
            buf = {0: 'N', 1: 'S', 2: 'E', 3: 'W'}
            for i in self.ns_4ce:
                res += '%s %4.1f %s\n' % (buf[i], self.ns_4ce[i][0], add[self.ns_4ce[i][1]])
            for i in self.ew_4ce:
                res += '%s %4.1f %s\n' % (buf[i+2], self.ew_4ce[i][0], add[self.ew_4ce[i][1]])
            res += '\nBases:\n'
            buf = {0: 'A', 1: 'P', 2: 'M'}
            for i in self.bs_4ce:
                res += '%s %4.1f %s\n' % (buf[i], self.bs_4ce[i][0], add[self.bs_4ce[i][1]])
            res += '\nCore: %s' % cst[self.core_st]
            if self.map_tp:
                res += ', %s' % self.map_tp

        return res

# -------------------------------------------------------------------------------------------------------------------- #
