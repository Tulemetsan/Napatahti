# -------------------------------------------------------------------------------------------------------------------- #

# @formatter:off


class CosmicStat:
    calc_pl = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 57, 15}
    fic_pl = {11, 23, 12, 56}
    chain = None
    ew_pl = None

    def __init__(self, abo, arb, atb):
        self.pl_crd = abo.get_pl_crd()
        self.pl_sgn = abo.get_pl_sgn()

        self.get_pl_name = abo.get_pl_name

        self.sg_rul = arb.get_sg_rul()
        self.sg_det = arb.get_sg_det()
        self.sg_ess = arb.get_sg_ess()
        self.dg_rul = arb.get_dg_rul()
        self.tr_rul = arb.get_tr_rul()
        self.dc_rul = arb.get_dc_rul()
        self.kd_deg = arb.get_kd_deg()
        self.pl_elm = arb.get_pl_elm()
        self.bs_4pl = arb.get_bs_4pl()
        self.rel_pl = arb.get_rel_pl()

        self.ess_sym = arb.get_ess_sym()
        self.ess_deg = arb.get_ess_deg()
        self.comp_el = arb.get_com_seq(0)
        self.el_4pl = arb.get_seq_4pl(0)

        self.tab_4pl = atb.get_tab_4pl()
        self.asp_fld = atb.get_asp_fld()
        self.rex_pit = atb.get_rex_pit()
        self.stm_sgn = atb.get_stm_sgn()
        self.top_pln = atb.get_top_pln()

        self.get_maj_are = atb.get_maj_are

        self.pl_rec = {}
        self.ess_pl = {}
        self.map_vw = {}
        self.csm_st = {}
        self.sum_st = 0

        self.reload()

    def get_pl_rec(self): return self.pl_rec
    def get_ess_pl(self): return self.ess_pl
    def get_map_vw(self): return self.map_vw
    def get_csm_st(self): return self.csm_st
    def get_sum_st(self): return self.sum_st

    def reload(self):
        self.calc_pl_rec()
        self.calc_ess_pl()
        self.calc_map_vw()
        self.calc_csm_st()

    def calc_pl_rec(self):
        self.pl_rec.clear()
        for i in range(5):
            self.pl_rec[i] = []
        self.chain = {0: [], 1: [], 2: [], 3: []}

        for i in self.calc_pl:
            j = self.sg_rul[0][self.pl_sgn[i]]
            self.add_rul_rec(i, j, 0)
            self.add_2_chain(i, j, 0)
            j = self.sg_rul[1][self.pl_sgn[i]]
            self.add_rul_rec(i, j, 0)
            self.add_2_chain(i, j, 0)
            j = self.sg_det[0][self.pl_sgn[i]]
            self.add_rul_rec(i, j, 1)
            self.add_2_chain(i, j, 1)
            j = self.sg_det[1][self.pl_sgn[i]]
            self.add_rul_rec(i, j, 1)
            self.add_2_chain(i, j, 1)

            j = self.sg_ess[0][self.pl_sgn[i]]
            self.add_ess_rec(i, j, 2)
            self.add_2_chain(i, j, 2)
            j = self.sg_ess[1][self.pl_sgn[i]]
            self.add_ess_rec(i, j, 3)
            self.add_2_chain(i, j, 3)

            j = self.dg_rul[int(self.pl_crd[i])]
            self.add_ess_rec(i, j, 4)

        for i in range(4):
            for j in self.chain[i]:
                for k in self.chain[i]:
                    if j & k:
                        j |= k
            buf = self.chain[i].copy()
            self.chain[i] = set()
            for j in buf:
                if len(j) >= 8:
                    self.chain[i] = j
                    break

    def add_rul_rec(self, p1, p2, mode):
        if p1 != p2 and p2 != -1:
            if mode == 1:
                sg_rul = self.sg_det
            elif mode == 0:
                sg_rul = self.sg_rul
            else:
                return None
            rc_seq = self.pl_rec[mode]

            p3 = sg_rul[0][self.pl_sgn[p2]]
            if p1 == p3:
                rec = sorted((p1, p2))
                if rec not in rc_seq:
                    rc_seq.append(rec)
            p3 = sg_rul[1][self.pl_sgn[p2]]
            if p1 == p3:
                rec = sorted((p1, p2))
                if rec not in rc_seq:
                    rc_seq.append(rec)

    def add_ess_rec(self, p1, p2, mode):
        if p1 != p2:
            if mode == 4:
                p3 = self.dg_rul[int(self.pl_crd[p2])]
            elif mode == 3:
                p3 = self.sg_ess[1][self.pl_sgn[p2]]
            elif mode == 2:
                p3 = self.sg_ess[0][self.pl_sgn[p2]]
            else:
                return None
            rc_seq = self.pl_rec[mode]

            if p1 == p3:
                rec = sorted((p1, p2))
                if rec not in rc_seq:
                    rc_seq.append(rec)

    def add_2_chain(self, p1, p2, mode):
        if p2 != -1:
            chain = self.chain[mode]
            if not chain:
                chain.append({p1, p2})
            else:
                flag = 1
                for i in chain:
                    if p1 in i:
                        i.add(p2)
                        flag = 0
                    elif p2 in i:
                        i.add(p1)
                        flag = 0
                if flag:
                    chain.append({p1, p2})

    def calc_ess_pl(self):
        self.ew_pl = {0: set(), 1: set()}
        self.ess_pl.clear()
        for i in range(10):
            self.ess_pl[i] = []

        ess = {0: [], 1: [], 2: [], 3: []}
        for i in self.ess_sym[0]:
            if self.ess_sym[0][i] != -1 and (i not in self.fic_pl):
                ess[self.ess_sym[0][i]].append(i)
            if (i == 2 and self.pl_sgn[i] == 5) or (i == 57 and self.pl_sgn[i] == 2):
                ess[0].append(i)

        for i in self.chain:
            if self.chain[i]:
                if ess[i]:
                    buf = []
                    for j in ess[i]:
                        if j in self.chain[i]:
                            buf.append(j)
                    if len(buf) in {1, 2}:
                        self.ess_pl[i] = buf
                elif self.pl_rec[i]:
                    buf = []
                    for j in self.pl_rec[i]:
                        if j[0] in self.chain[i] and j[1] in self.chain[i]:
                            buf.append(j)
                    if len(buf) == 1:
                        self.ess_pl[i] = buf[0]

        buf = []
        sun = 0
        for i in self.calc_pl:
            buf.append([self.pl_crd[i], i])
        buf.sort()
        for i in buf:
            if i[1] == 0:
                break
            sun += 1

        k1, k2 = 0, 0
        if sun == 10:
            k2 = -12
        elif sun == 11:
            k1 = -12
            k2 = -11
        d1 = buf[sun-1][1]
        d2 = buf[sun-2][1]
        a1 = buf[sun+1+k1][1]
        a2 = buf[sun+2+k2][1]
        as1 = self.tab_4pl[(min(d1, d2), max(d1, d2))]
        as2 = self.tab_4pl[(min(a1, a2), max(a1, a2))]

        zp = buf[sun][0]
        for i in range(12):
            if buf[i][1] != 0:
                crd = buf[i][0] - zp
                if crd < 0:
                    crd += 360
                if crd > 180:
                    self.ew_pl[0].add(buf[i][1])
                elif crd < 180:
                    self.ew_pl[1].add(buf[i][1])

        self.ess_pl[4].append(d1)
        self.ess_pl[5].append(a1)
        if as1[1] == 0 and as1[3] == 1:
            self.ess_pl[4].append(d2)
        if as2[1] == 0 and as2[3] == 1:
            self.ess_pl[5].append(a2)

        for i in self.calc_pl ^ {0} | self.fic_pl:
            asp = self.tab_4pl[(0, i)][0]
            if asp < 17/60:  # heart
                self.ess_pl[6].append(i)
            if 17/60 <= asp < 3 and i not in self.fic_pl:  # burning
                self.ess_pl[7].append(i)
            if i != 2 and 3 <= asp < 30:  # sun zone
                self.ess_pl[8].append(i)
            elif i == 2 and 15 <= asp < 19:
                self.ess_pl[8].append(i)
            if asp > 160:  # free zone
                self.ess_pl[9].append(i)
            elif i == 2 and asp >= 25:
                self.ess_pl[9].append(i)

    def calc_map_vw(self):
        self.map_vw.clear()

        sec = self.calc_sector(60)
        k = len(sec)

        if k == 1:
            con = sec[0][-1][0]
            if 70 < con < 190:
                p1 = sec[0][0][1]
                p2 = sec[0][-1][1]
                asp = self.tab_4pl[(min(p1, p2), max(p1, p2))][1]
                if asp in {180, 120, 144, 160, 80}:
                    for i in self.calc_pl ^ {p1, p2}:
                        k1 = (min(p1, i), max(p1, i))
                        k2 = (min(p2, i), max(p2, i))
                        if self.tab_4pl[k1][1] == self.tab_4pl[k2][1] == asp/2:
                            self.map_vw[0] = 57
                            self.calc_bed(sec[0])
                            break
            if not self.map_vw:
                if con < 150:
                    self.map_vw[0] = 6
                    self.calc_bed(sec[0])
                elif 150 <= con < 210:
                    self.map_vw[0] = 8
                    self.calc_bed(sec[0])
                elif 210 <= con < 270:
                    self.map_vw[0] = 5
        elif k == 2:
            k1 = len(sec[0])
            k2 = len(sec[1])
            ic, im = 0, 1
            if k1 > k2:
                ic = 1
                im = 0
            cnc = sec[ic][-1][0] - sec[ic][0][0]
            cnm = sec[im][-1][0] - sec[im][0][0]
            if k1 == 1 or k2 == 1:
                if cnm < 150:
                    self.map_vw[0] = 9
                    self.map_vw[1] = [sec[ic][0][1]]
                    self.calc_bed(sec[im])
                elif 150 <= cnm < 210:
                    self.map_vw[0] = 4
                    self.map_vw[1] = [sec[ic][0][1]]
                    self.calc_bed(sec[im])
            elif k1 == 2 or k2 == 2:
                p1 = sec[ic][0][1]
                p2 = sec[ic][1][1]
                asp = self.tab_4pl[(min(p1, p2), max(p1, p2))][1]
                if cnm < 150:
                    if asp == 0:
                        self.map_vw[0] = 9
                        self.map_vw[1] = [p1, p2]
                        self.calc_bed(sec[im])
                    elif cnc <= 50:
                        self.map_vw[0] = 15
                        self.calc_bed(sec[im])
                elif 150 <= cnm < 210:
                    if asp == 0:
                        self.map_vw[0] = 4
                        self.map_vw[1] = [p1, p2]
                        self.calc_bed(sec[im])
                    elif cnc <= 50:
                        self.map_vw[0] = 3
                        self.calc_bed(sec[im])
            else:
                if 40 <= cnm <= 80 and 40 <= cnc <= 80:
                    self.map_vw[0] = 2
                elif cnm < 150 and cnc <= 50:
                    self.map_vw[0] = 15
                    self.calc_bed(sec[im])
                elif 150 <= cnm < 210 and cnc <= 50:
                    self.map_vw[0] = 3
                    self.calc_bed(sec[im])
        elif k == 3:
            if len(sec[0]) >= 3 and len(sec[1]) >= 3 and len(sec[2]) >= 3:
                cn1 = sec[0][-1][0] - sec[0][0][0]
                cn2 = sec[1][-1][0] - sec[1][0][0]
                cn3 = sec[2][-1][0] - sec[2][0][0]
                if cn1 <= 50 and cn2 <= 50 and cn3 <= 50:
                    self.map_vw[0] = 7

        if not self.map_vw:
            sec = self.calc_sector(110)
            if len(sec) == 1:
                p1 = sec[0][0][1]
                p2 = sec[0][-1][1]
                asp = self.tab_4pl[(min(p1, p2), max(p1, p2))][0]
                if asp <= 110:
                    if self.get_maj_are():
                        self.map_vw[0] = 1
                    else:
                        self.map_vw[0] = 0

    def calc_sector(self, space):
        sec = []
        sq1, sq2 = [], []

        for i in self.calc_pl:
            sq1.append([self.pl_crd[i], i])
        sq1.sort()

        for i in range(len(sq1) - 1):
            p1 = sq1[i][1]
            p2 = sq1[i+1][1]
            asp = self.tab_4pl[(min(p1, p2), max(p1, p2))][0]
            if asp <= space:
                if sq1[i] not in sq2:
                    sq2.append(sq1[i])
                sq2.append(sq1[i+1])
            else:
                if sq1[i] not in sq2:
                    sq2.append(sq1[i])
                sec.append(sq2)
                sq2 = [sq1[i+1]]
        if sq2:
            sec.append(sq2)

        if len(sec) > 1:
            p1 = sec[0][0][1]
            p2 = sec[-1][-1][1]
            asp = self.tab_4pl[(min(p1, p2), max(p1, p2))][0]
            if asp <= space:
                sec[0] = sec[-1] + sec[0]
                sec.remove(sec[-1])

        k = sec[0][0][0]
        for i in range(len(sec)):
            for j in range(len(sec[i])):
                sec[i][j][0] -= k
                if sec[i][j][0] < 0:
                    sec[i][j][0] += 360

        return sec

    def calc_bed(self, sec):
        seq = []
        buf = []

        for i in range(len(sec) - 1):
            p1 = sec[i][1]
            p2 = sec[i+1][1]
            asp = self.tab_4pl[(min(p1, p2), max(p1, p2))][1]
            if asp == 0:
                if p1 not in buf:
                    buf.append(p1)
                buf.append(p2)
            else:
                if p1 not in buf:
                    buf.append(p1)
                seq.append(buf)
                buf = [p2]
        if buf:
            seq.append(buf)

        k = len(seq)
        if k % 2:
            self.map_vw[2] = seq[int(k/2)]

    def calc_csm_st(self):
        self.sum_st = 0
        pos_el = self.comp_el[0][0]
        neg_el = self.comp_el[0][1]
        cor_el = {0: 2, 1: 0, 2: 1, 3: 3}
        ali_el = {0: 3, 1: 2, 2: 1, 3: 0}
        dis = {
            0: {self.sg_rul[0][self.pl_sgn[0]], self.sg_rul[0][self.pl_sgn[56]], self.sg_det[0][self.pl_sgn[12]]},
            1: {self.sg_rul[0][self.pl_sgn[1]]} | {self.sg_rul[0][i] for i in self.stm_sgn},
            2: {self.sg_ess[0][self.pl_sgn[0]], self.sg_ess[0][self.pl_sgn[56]], self.sg_ess[1][self.pl_sgn[12]]},
            3: {self.sg_ess[0][self.pl_sgn[1]]} | {self.sg_ess[0][i] for i in self.stm_sgn}
        }
        opp = {
            0: {self.sg_det[0][self.pl_sgn[0]], self.sg_det[0][self.pl_sgn[56]], self.sg_rul[0][self.pl_sgn[12]]},
            1: {self.sg_det[0][self.pl_sgn[1]]} | {self.sg_det[0][i] for i in self.stm_sgn},
            2: {self.sg_ess[1][self.pl_sgn[0]], self.sg_ess[1][self.pl_sgn[56]], self.sg_ess[0][self.pl_sgn[12]]},
            3: {self.sg_ess[1][self.pl_sgn[1]]} | {self.sg_ess[1][i] for i in self.stm_sgn}
        }

        moon_ph = self.pl_crd[1] - self.pl_crd[0]
        if moon_ph < 0:
            moon_ph += 360
        mph_el = cor_el[int(moon_ph/90)]

        for i in self.calc_pl:
            self.csm_st[i] = [0, 0]
            pos, neg = 0, 0

            deg = int(self.pl_crd[i])
            trm = int(self.pl_crd[i]/5)
            dec = int(self.pl_crd[i]/10)
            ess = self.ess_sym[0][i]

            if ess == 0:
                pos += 5
            elif ess == 1:
                neg -= 5
            elif ess == 2:
                pos += 4
            elif ess == 3:
                neg -= 4
            if i == 2 and self.pl_sgn[i] == 5 or i == 57 and self.pl_sgn[i] == 2:
                pos += 3
            elif i == 2 and self.pl_sgn[i] == 11 or i == 57 and self.pl_sgn[i] == 8:
                neg -= 3

            if pos_el[i]:
                pos += 4
            elif neg_el[i]:
                neg -= 4

            for j in range(4):
                if i in self.ess_pl[j]:
                    if j in {0, 2}:
                        n, k = 0, 3
                    else:
                        n, k = 1, -3
                    if len(self.ess_pl[j]) == 2:
                        k /= 2
                    self.csm_st[i][n] += k

            if i in self.rex_pit[0]:
                k = 3
                if len(self.rex_pit[0]) == 2:
                    k /= 2
                pos += k
            elif i in self.rex_pit[1]:
                neg -= 3

            for t in self.pl_rec:
                for j in self.pl_rec[t]:
                    if i in j:
                        if t == 0:
                            n, k = 0, 2
                        elif t == 1:
                            n, k = 1, -2
                        elif t == 3:
                            n, k = 1, -1
                        else:
                            n, k = 0, 1
                        self.csm_st[i][n] += k

            for j in [0, 1, 2, 3]:
                if i in dis[j]:
                    pos += 4 - j
                if i in opp[j]:
                    neg -= 4 - j

            if self.bs_4pl[0][i] == 0:
                if i in self.ew_pl[0]:
                    pos += 3
                elif i in self.ew_pl[1]:
                    neg -= 3

                if deg == 0:
                    pos += 2
                elif deg == 29:
                    neg -= 2

                if self.asp_fld[1][1] == 1:
                    pos += 2
                elif self.asp_fld[1][1] == -1:
                    neg -= 2
                if self.asp_fld[3][1] == 1:
                    pos += 1
                elif self.asp_fld[3][1] == -1:
                    neg -= 1
            elif self.bs_4pl[0][i] == 1:
                if i in self.ew_pl[1]:
                    pos += 3
                elif i in self.ew_pl[0]:
                    neg -= 3

                if deg == 29:
                    pos += 2
                elif deg == 0:
                    neg -= 2

                if self.asp_fld[2][1] == 1:
                    pos += 2
                elif self.asp_fld[2][1] == -1:
                    neg -= 2
                if self.asp_fld[4][1] == 1:
                    pos += 1
                elif self.asp_fld[4][1] == -1:
                    neg -= 1
            else:
                if i in self.ess_pl[9]:
                    pos += 3
                elif i in self.ess_pl[8]:
                    neg -= 3

                if deg == 14:
                    pos += 2
                elif deg == 15:
                    neg -= 2

                if self.asp_fld[1][1] == 0:
                    pos += 2
                if self.asp_fld[3][1] == 0:
                    pos += 1

            if i in self.ess_pl[4]:
                k = 3 if len(self.ess_pl[4]) == 1 else 1.5
                pos += k
            elif i in self.ess_pl[5]:
                k = 3 if len(self.ess_pl[5]) == 1 else 1.5
                neg -= k

            if i in self.ess_pl[6]:
                pos += 3
            elif i in self.ess_pl[7]:
                neg -= 3

            if deg in self.kd_deg[0]:
                pos += 3
            elif deg in self.kd_deg[1]:
                neg -= 3

            if self.ess_deg[0][i] is not None:
                pos += 1
                if i == self.ess_deg[0][i]:
                    pos += 2
            elif self.ess_deg[1][i] is not None:
                neg -= 1
                if i == self.ess_deg[1][i]:
                    neg -= 2

            if self.dg_rul[deg] == i:
                pos += 2
            if self.dg_rul[deg] in self.rel_pl[0][i]:
                pos += 1
            elif self.dg_rul[deg] in self.rel_pl[1][i]:
                neg -= 1

            if i == 1:
                if self.el_4pl[0][i] == mph_el:
                    pos += 2
                elif self.el_4pl[0][i] == ali_el[mph_el]:
                    neg -= 2
                if i in self.ess_pl[9]:
                    pos += 1
                elif i in (self.ess_pl[6] + self.ess_pl[7] + self.ess_pl[8]):
                    neg -= 1
            else:
                if self.pl_elm[0][i] == mph_el:
                    pos += 1
                elif self.pl_elm[1][i] == mph_el:
                    neg -= 1

            if self.tr_rul[trm] == i:
                pos += 1
            elif self.tr_rul[trm] in self.rel_pl[1][i]:
                neg -= 1

            if self.dc_rul[dec] == i:
                pos += 1
            elif self.dc_rul[dec] in self.rel_pl[1][i]:
                neg -= 1

            if i in self.top_pln[0]:
                pos += 1
            elif i in self.top_pln[1]:
                neg -= 1

            if 1 in self.map_vw and i in self.map_vw[1]:
                pos += 1
            if 2 in self.map_vw and i in self.map_vw[2]:
                neg -= 1

            self.csm_st[i][0] += pos
            self.csm_st[i][1] += neg
            self.sum_st += self.csm_st[i][0] + self.csm_st[i][1]

    def __str__(self):
        buf = {i: self.csm_st[i][0] + self.csm_st[i][1] for i in self.csm_st}
        sc1 = max(buf.values())
        sc2 = min(buf.values())
        alc, ant = [], []

        res = 'Cosmic status of planets:\n\n'

        for i in self.csm_st:
            res += '%10s %3d (%+3d, %3d)\n' % (self.get_pl_name(i), buf[i], self.csm_st[i][0], self.csm_st[i][1])
            if buf[i] == sc1:
                alc.append(i)
            elif buf[i] == sc2:
                ant.append(i)

        res += '\n%9s: %+3d\n' % ('Total', self.sum_st)
        res += '%9s: ' % 'Max score'
        for i in alc:
            res += '%s ' % self.get_pl_name(i)
        res += '\n%9s: ' % 'Min score'
        for i in ant:
            res += '%s ' % self.get_pl_name(i)

        return res

# -------------------------------------------------------------------------------------------------------------------- #
