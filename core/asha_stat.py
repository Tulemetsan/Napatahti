# -------------------------------------------------------------------------------------------------------------------- #

# @formatter:off


class AshaStat:
    calc_pl = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 57, 15}

    def __init__(self, abo, arb):
        self.pl_crd = abo.get_pl_crd()
        self.cs_crd = abo.get_cs_crd()
        self.pl_hse = abo.get_pl_hse()
        self.pl_sgn = abo.get_pl_sgn()

        self.get_pl_name = abo.get_pl_name

        self.sg_rul = arb.get_sg_rul()
        self.sg_ess = arb.get_sg_ess()
        self.dg_rul = arb.get_dg_rul()
        self.tr_rul = arb.get_tr_rul()
        self.dc_rul = arb.get_dc_rul()

        self.ash_pw = {}
        self.ash_cr = {}
        self.ash_st = {}
        self.ess_pl = {}

        self.reload()

    def get_asha_pw(self): return self.ash_pw
    def get_asha_cr(self): return self.ash_cr
    def get_asha_st(self): return self.ash_st
    def get_asha_pl(self): return self.ess_pl

    def reload(self):
        self.ash_pw.clear()
        self.ash_cr.clear()
        self.ash_st.clear()
        for i in self.calc_pl:
            self.ash_pw[i] = 0
            self.ash_cr[i] = 0
            self.ash_st[i] = [0, 0]
        self.ess_pl[0] = {}
        self.ess_pl[1] = {}
        self.ess_pl[2] = {}
        self.ess_pl[3] = {}

        ext_pt = {
            1: self.cs_crd[0], 10: self.cs_crd[9], 15: self.cs_crd[0] + self.pl_crd[1] - self.pl_crd[0],  # fortuna
            2: self.cs_crd[1], 5: self.cs_crd[4], 14: self.cs_crd[0] + self.pl_crd[3] - self.pl_crd[5],  # happiness
            8: self.cs_crd[7], 11: self.cs_crd[10], 13: self.cs_crd[0] + self.pl_crd[4] - self.pl_crd[6]   # fate cross
        }
        for i in {13, 14, 15}:
            if ext_pt[i] >= 360:
                ext_pt[i] -= 360
            elif ext_pt[i] < 0:
                ext_pt[i] += 360

        for i in self.calc_pl:
            sig = self.sg_rul[0][self.pl_hse[i]]
            ds1 = self.sg_rul[0][self.pl_sgn[i]]
            ds2 = self.sg_rul[1][self.pl_sgn[i]]
            ess = self.sg_ess[0][self.pl_sgn[i]]
            dgr = self.dg_rul[int(self.pl_crd[i])]
            tmr = self.tr_rul[int(self.pl_crd[i]/5)]
            dcr = self.dc_rul[int(self.pl_crd[i]/10)]
            self.ash_pw[sig] += 6
            self.ash_pw[ds1] += 5
            if ds2 != -1:
                self.ash_pw[ds2] += 4
            self.ash_pw[ess] += 4
            self.ash_pw[dgr] += 3
            self.ash_pw[tmr] += 2
            self.ash_pw[dcr] += 1
            if i in {0, 1}:
                self.ash_cr[ds1] += 5
                if ds2 != -1:
                    self.ash_cr[ds2] += 4
                self.ash_cr[ess] += 4
                self.ash_cr[dgr] += 3
                self.ash_cr[tmr] += 2
                self.ash_cr[dcr] += 1
            elif i in {3, 5}:
                self.ash_st[ds1][0] += 5
                if ds2 != -1:
                    self.ash_st[ds1][0] += 4
                self.ash_st[ess][0] += 4
                self.ash_st[dgr][0] += 3
                self.ash_st[tmr][0] += 2
                self.ash_st[dcr][0] += 1
            elif i in {4, 6}:
                self.ash_st[ds1][1] -= 5
                if ds2 != -1:
                    self.ash_st[ds1][1] -= 4
                self.ash_st[ess][1] -= 4
                self.ash_st[dgr][1] -= 3
                self.ash_st[tmr][1] -= 2
                self.ash_st[dcr][1] -= 1

        for i in ext_pt:
            sgn = int(ext_pt[i]/30)
            ds1 = self.sg_rul[0][sgn]
            ds2 = self.sg_rul[1][sgn]
            ess = self.sg_ess[0][sgn]
            dgr = self.dg_rul[int(ext_pt[i])]
            tmr = self.tr_rul[int(ext_pt[i]/5)]
            dcr = self.dc_rul[int(ext_pt[i]/10)]
            if i in {1, 10, 15}:
                self.ash_cr[ds1] += 5
                if ds2 != -1:
                    self.ash_cr[ds2] += 4
                self.ash_cr[ess] += 4
                self.ash_cr[dgr] += 3
                self.ash_cr[tmr] += 2
                self.ash_cr[dcr] += 1
            elif i in {2, 5, 14}:
                self.ash_st[ds1][0] += 5
                if ds2 != -1:
                    self.ash_st[ds1][0] += 4
                self.ash_st[ess][0] += 4
                self.ash_st[dgr][0] += 3
                self.ash_st[tmr][0] += 2
                self.ash_st[dcr][0] += 1
            elif i in {8, 11, 13}:
                self.ash_st[ds1][1] -= 5
                if ds2 != -1:
                    self.ash_st[ds1][1] -= 4
                self.ash_st[ess][1] -= 4
                self.ash_st[dgr][1] -= 3
                self.ash_st[tmr][1] -= 2
                self.ash_st[dcr][1] -= 1

        buf = {i: self.ash_st[i][0] + self.ash_st[i][1] for i in self.ash_st}
        max_st = max(buf.values())
        min_st = min(buf.values())
        max_cr = max(self.ash_cr.values())
        max_pw = max(self.ash_pw.values())

        for i in self.ash_st:
            if buf[i] == max_st:
                self.ess_pl[0][i] = max_st
            elif buf[i] == min_st:
                self.ess_pl[1][i] = min_st
            if self.ash_cr[i] == max_cr:
                self.ess_pl[2][i] = max_cr
            if self.ash_pw[i] == max_pw:
                self.ess_pl[3][i] = max_pw

    def __str__(self):
        buf = {i: self.ash_st[i][0] + self.ash_st[i][1] for i in self.ash_st}

        res = 'Avestian status of planets:\n\n'
        res += '%10s %3s, %3s (%3s, %3s), %3s\n' % ('', 'POW', 'KND', 'POS', 'NEG', 'CRV')

        for i in self.ash_st:
            res += '%10s %3d, %+3d (%+3d, %3d), %3d\n' % (self.get_pl_name(i), self.ash_pw[i], buf[i],
                                                          self.ash_st[i][0], self.ash_st[i][1], self.ash_cr[i])
        res += '\n%s: ' % 'Anareta'
        for i in self.ess_pl[1]:
            res += '%s ' % self.get_pl_name(i)
        res += '\n%s: ' % 'Alcocoden'
        for i in self.ess_pl[0]:
            res += '%s ' % self.get_pl_name(i)
        res += '\n%s: ' % 'Dominus Genitura'
        for i in self.ess_pl[3]:
            res += '%s ' % self.get_pl_name(i)

        return res

# -------------------------------------------------------------------------------------------------------------------- #
