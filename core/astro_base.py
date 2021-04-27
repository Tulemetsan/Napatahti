# -------------------------------------------------------------------------------------------------------------------- #

import json
import swisseph as swe
import core.utilities as ut

# @formatter:off


class AstroBaseObject:
    base_pl = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 23, 12, 56, 57, 15]
    cat_pl = {
        0: 'Q', 1: 'W', 2: 'E', 3: 'R', 4: 'T', 5: 'Y', 6: 'U',
        7: 'I', 8: 'O', 9: 'P', 11: '{', 23: '}', 12: '`', 56: 'Ñ', 57: 'Ð', 15: 'M'
    }
    pl_crd_enb = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 23, 12, 56, 57, 15}
    pl_asp_enb = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 23, 12, 56, 57, 15}
    sg_sym = {0: 'a', 1: 's', 2: 'd', 3: 'f', 4: 'g', 5: 'h', 6: 'j', 7: 'k', 8: 'l', 9: 'z', 10: 'x', 11: 'c'}
    cs_sym = {0: 'Z', 1: '2', 2: '3', 3: '“', 4: '5', 5: '6', 6: '’', 7: '8', 8: '9', 9: 'X', 10: '11', 11: '12'}
    sp_sym = {0: '%', 1: '*', 2: '$'}
    mid_spd = {
        0: 0.985555, 1: 13.176388, 2: 1.303888, 3: 1.199166, 4: 0.524166, 5: 0.083055, 6: 0.033333, 7: 0.0116666,
        8: 0.006111, 9: 0.003888, 57: 0.001388, 15: 0.019444, 11: 0.053055, 23: 0.053055
    }
    jul_day, week_d = 0, 0
    flag = 0

    def __init__(self, pth, data):
        swe.set_ephe_path(pth)

        self.data = data
        self.cat_pl = {}
        self.show_pl = []
        self.pl_crd_enb, self.pl_asp_enb, self.pl_enb = set(), set(), set()
        self.pl_crd_s, self.pl_crd_h = {}, {}
        self.pl_spd_val, self.pl_spd_sym = {}, {}
        self.cs_crd_s, self.hs_len = {}, {}
        self.pl_sgn, self.cs_sgn, self.pl_hse = {}, {}, {}
        self.sg_sym, self.cs_sym, self.sp_sym = {}, {}, {}
        self.pl_str, self.cs_str = {}, {}
        self.moon_j = {}
        self.moon_d = {0: {}, 1: {}}
        self.moon_c = {0: {}, 1: {}}

        self.load_cat()
        self.reload()

    def get_bs_data(self): return self.data
    def get_jul_day(self): return self.jul_day

    def get_base_pl(self, mode=1): return set(self.base_pl) if mode else self.base_pl
    def get_cat_pl(self): return self.cat_pl
    def get_show_pl(self): return self.show_pl

    def get_pl_crd_enb(self): return self.pl_crd_enb
    def get_pl_asp_enb(self): return self.pl_asp_enb
    def get_pl_enb(self): return self.pl_enb

    def get_pl_crd(self): return self.pl_crd_s
    def get_cs_crd(self): return self.cs_crd_s
    def get_pl_sgn(self): return self.pl_sgn
    def get_pl_hse(self): return self.pl_hse
    def get_cs_sgn(self): return self.cs_sgn
    def get_pl_str(self): return self.pl_str
    def get_cs_str(self): return self.cs_str

    def get_sg_sym(self): return self.sg_sym
    def get_cs_sym(self): return self.cs_sym
    def get_sp_sym(self): return self.pl_spd_sym

    def get_moon_d(self): return self.moon_d
    def get_moon_c(self): return self.moon_c
    def get_week_d(self): return self.week_d

    def reload(self):
        self.pl_crd_s.clear()
        self.pl_spd_val.clear()
        self.pl_spd_sym.clear()
        self.cs_crd_s.clear()
        self.pl_sgn.clear()
        self.cs_sgn.clear()
        self.pl_hse.clear()
        self.pl_str.clear()
        self.cs_str.clear()

        data = self.data
        self.jul_day = swe.julday(
                data[1]['date'][0], data[1]['date'][1], data[1]['date'][2],
                data[1]['time'][0] + data[1]['time'][1]/60 + data[1]['time'][2]/3600 - data[1]['time'][3], 1
            )
        self.week_d = swe.day_of_week(self.jul_day)

        for i in self.cat_pl:
            if i == 23:
                continue
            buf = swe.calc_ut(self.jul_day, i)[0]
            if i == 11:
                self.pl_crd_s[23] = buf[0] + 180 if buf[0] < 180 else buf[0] - 180
                self.pl_spd_val[23] = buf[3]
            self.pl_crd_s[i] = buf[0]
            self.pl_spd_val[i] = buf[3]

        ns, ew = {'n': 1, 'N': 1, 's': -1, 'S': -1}, {'e': 1, 'E': 1, 'w': -1, 'W': -1}
        lat = (data[1]['lat'][0] + data[1]['lat'][1]/60 + data[1]['lat'][2]/3600) * ns[data[1]['lat'][3]]
        lon = (data[1]['lon'][0] + data[1]['lon'][1]/60 + data[1]['lon'][2]/3600) * ew[data[1]['lon'][3]]
        buf = dict(zip(range(12), swe.houses(self.jul_day, lat, lon, data[1]['sysHouse'].encode())[0]))
        for i in range(12):
            self.cs_crd_s[i] = buf[i]

        self.calc_pl_crd_h()

        for i in self.pl_crd_s:
            self.pl_sgn[i] = int(self.pl_crd_s[i]/30)
            self.pl_hse[i] = int(self.pl_crd_h[i]/30)
            self.set_spd_sym(i)
            self.pl_str[i] = self.format_crd(self.pl_crd_s[i], self.pl_sgn[i])

        for i in self.cs_crd_s:
            self.cs_sgn[i] = int(self.cs_crd_s[i]/30)
            self.cs_str[i] = self.format_crd(self.cs_crd_s[i], self.cs_sgn[i])

        self.calc_moon_day(lat, lon)

    def calc_pl_crd_h(self, ind=None):
        calc_seq = self.cat_pl if ind is None else [ind]
        if ind is None:
            self.pl_crd_h.clear()
            self.hs_len.clear()
            for i in range(12):
                if i == 11:
                    self.hs_len[i] = self.cs_crd_s[0] - self.cs_crd_s[i]
                else:
                    self.hs_len[i] = self.cs_crd_s[i+1] - self.cs_crd_s[i]
                if self.hs_len[i] < 0:
                    self.hs_len[i] = -360 - self.hs_len[i]

        for i in self.cs_crd_s:
            for j in calc_seq:
                asp = self.pl_crd_s[j] - self.cs_crd_s[i]
                if asp < 0:
                    asp = -360 - asp
                if asp == 0:
                    self.pl_crd_h[j] = i*30
                elif self.hs_len[i] > 0:
                    if 0 < asp < self.hs_len[i]:
                        self.pl_crd_h[j] = (i + asp/self.hs_len[i]) * 30
                else:  # cuspid, planet crossed 0 Ari: first, both
                    if 0 < asp < abs(self.hs_len[i]):
                        self.pl_crd_h[j] = (i + asp/abs(self.hs_len[i])) * 30
                    elif self.hs_len[i] < asp < 0:
                        self.pl_crd_h[j] = (i + asp/self.hs_len[i]) * 30

    def set_spd_sym(self, ind):
        enb = 1
        if ind in self.mid_spd:
            if abs(self.pl_spd_val[ind]) < self.mid_spd[ind]/10:
                self.pl_spd_sym[ind] = self.sp_sym[0]
                enb = 0
        else:
            if abs(self.pl_spd_val[ind]) < 1/3600:
                self.pl_spd_sym[ind] = self.sp_sym[0]
                enb = 0
        if enb:
            if self.pl_spd_val[ind] > 0:
                self.pl_spd_sym[ind] = self.sp_sym[1] if ind in {11, 23} else ''
            elif self.pl_spd_val[ind] < 0:
                self.pl_spd_sym[ind] = self.sp_sym[2] if ind not in {11, 23} else ''

    def calc_moon_day(self, lat, lon):
        self.moon_j.clear()
        self.moon_d[0].clear()
        self.moon_d[1].clear()
        self.moon_c[0].clear()
        self.moon_c[1].clear()
        data = self.data

        # jyotisa
        self.moon_j[1] = self.calc_moon_jd()
        self.moon_j[31] = self.calc_moon_jd(1)
        self.moon_d[0][3] = self.revjul_2d(self.moon_j[1], data[1]['time'][3])
        self.moon_d[0][4] = self.revjul_2d(self.moon_j[31], data[1]['time'][3])
        self.moon_d[1][3] = self.moon_d[0][3]
        self.moon_d[1][4] = self.moon_d[0][4]

        dj = self.pl_crd_s[1] - self.pl_crd_s[0]
        if dj < 0:
            dj += 360
        dj = int(1 + dj/12)
        self.moon_d[1][0] = dj

        if dj == 1:
            self.moon_d[1][1] = self.moon_d[1][3]
            self.moon_d[1][2] = self.revjul_2d(self.calc_moon_jd(1, dj=dj), data[1]['time'][3])
        elif dj == 30:
            self.moon_d[1][1] = self.revjul_2d(self.calc_moon_jd(dj=dj), data[1]['time'][3])
            self.moon_d[1][2] = self.moon_d[1][4]
        else:
            self.moon_d[1][1] = self.revjul_2d(self.calc_moon_jd(dj=dj), data[1]['time'][3])
            self.moon_d[1][2] = self.revjul_2d(self.calc_moon_jd(1, dj=dj), data[1]['time'][3])

        for i in range(1, 33):
            if i == 1:
                self.moon_c[1][i] = self.moon_d[1][3]
            elif i == dj:
                self.moon_c[1][i] = self.moon_d[1][1]
            elif i == 31:
                self.moon_c[1][i] = self.moon_d[1][4]
            elif i == 32:
                self.moon_c[1][i] = self.moon_c[1][16]
            else:
                rev = 1 if i > dj else -1
                day = i - 1 if i > dj else i
                self.moon_c[1][i] = self.revjul_2d(self.calc_moon_jd(rev, day), data[1]['time'][3])

        # western
        if -66.54 <= lat <= 66.54:
            cur = self.moon_j[1]
            self.moon_d[0][0] = 0
            for i in range(2, 31):  # rsmi 897 rise, 898 set
                nxt = swe.rise_trans(cur + 0.05, 1, lon, lat, rsmi=897)[1][0]
                if i < 30 or i == 30 and nxt < self.moon_j[31]:
                    self.moon_j[i] = nxt
                    if self.moon_j[i-1] < self.jul_day < nxt:
                        self.moon_d[0][0] = i - 1
                cur = nxt
            if not self.moon_d[0][0]:
                self.moon_d[0][0] = len(self.moon_j) - 1
            cur = self.moon_d[0][0]
            self.moon_d[0][1] = self.revjul_2d(self.moon_j[cur], data[1]['time'][3])
            if cur < 29:
                self.moon_d[0][2] = self.revjul_2d(self.moon_j[cur+1], data[1]['time'][3])
            elif cur == 29:
                self.moon_d[0][2] = 30 if 30 in self.moon_j else 31
                self.moon_d[0][2] = self.revjul_2d(self.moon_j[self.moon_d[0][2]], data[1]['time'][3])
            else:
                self.moon_d[0][2] = self.revjul_2d(self.moon_j[31], data[1]['time'][3])

            for i in sorted(self.moon_j):
                self.moon_c[0][i] = self.revjul_2d(self.moon_j[i], data[1]['time'][3])
            self.moon_c[0][32] = self.moon_c[1][16]
        else:
            self.moon_d[0][0] = self.moon_d[1][0]
            self.moon_d[0][1] = self.moon_d[1][1]
            self.moon_d[0][2] = self.moon_d[1][2]

    def calc_moon_jd(self, rev=-1, dj=0, acc=0.000001):
        k = 0 if rev == 1 else -1
        if dj:
            crd_sn = self.pl_crd_s[0] + (dj + k)*12
            if crd_sn >= 360:
                crd_sn -= 360
        else:
            crd_sn = self.pl_crd_s[0]

        as1 = rev*(crd_sn - self.pl_crd_s[1])
        if as1 < 0:
            as1 += 360
        if as1 < acc:
            return self.jul_day

        jds = as1/(self.pl_spd_val[1] - self.pl_spd_val[0])
        mjd = self.jul_day + rev*jds

        while 1:
            buf = swe.calc_ut(mjd, 0)[0]
            crd_sn = buf[0]
            spd_sn = buf[3]
            if dj:
                crd_sn += (dj + k)*12
            buf = swe.calc_ut(mjd, 1)[0]
            crd_mn = buf[0]
            spd_mn = buf[3]
            as2 = abs(crd_sn - crd_mn)
            if as2 > 180:
                as2 = 360 - as2
            if as2 < acc:
                return mjd
            else:
                jds = as2/(spd_mn - spd_sn)
                if as2 < as1:
                    mjd += rev*jds
                else:
                    mjd -= rev*jds
                as1 = as2

    @staticmethod
    def revjul_2d(jd, utc=0):
        jd = swe.revjul(jd + utc/24)
        hh = int(jd[3])
        mm = (jd[3] - hh)*60
        ss = (mm - int(mm))*60
        return {0: jd[0], 1: jd[1], 2: jd[2], 3: hh, 4: int(mm), 5: int(ss)}

    def dump_cat(self):
        if self.flag:
            enc = ['Catalog', json.dumps(list(self.cat_pl.items()))]
            enc += ['Planet crd enb', json.dumps(list(self.pl_crd_enb))]
            enc += ['Planet asp enb', json.dumps(list(self.pl_asp_enb))]
            enc += ['Sign symbol', json.dumps(list(self.sg_sym.items()))]
            enc += ['House symbol', json.dumps(list(self.cs_sym.items()))]
            enc += ['Speed symbol', json.dumps(list(self.sp_sym.items()))]
            with open('Planets.json', 'w') as fp:
                json.dump(enc, fp, separators=(',\n', ': '))
                fp.close()
            self.flag = 0

    def load_cat(self):
        check = 0
        try:
            with open('Planets.json') as fp:
                src_data = json.load(fp)
                fp.close()
            for i in range(1, len(src_data), 2):
                if src_data[i-1] == 'Catalog':
                    self.cat_pl.clear()
                    dec = dict(json.loads(src_data[i]))
                    for j in dec:
                        self.cat_pl[j] = dec[j]
                    check |= 1
                elif src_data[i-1] == 'Planet crd enb':
                    self.pl_crd_enb.clear()
                    self.pl_crd_enb |= set(json.loads(src_data[i]))
                    check |= 2
                elif src_data[i-1] == 'Planet asp enb':
                    self.pl_asp_enb.clear()
                    self.pl_asp_enb |= set(json.loads(src_data[i]))
                    check |= 4
                elif src_data[i-1] == 'Sign symbol':
                    self.sg_sym.clear()
                    dec = dict(json.loads(src_data[i]))
                    for j in dec:
                        self.sg_sym[j] = dec[j]
                    check |= 8
                elif src_data[i-1] == 'House symbol':
                    self.cs_sym.clear()
                    dec = dict(json.loads(src_data[i]))
                    for j in dec:
                        self.cs_sym[j] = dec[j]
                    check |= 16
                elif src_data[i-1] == 'Speed symbol':
                    self.sp_sym.clear()
                    dec = dict(json.loads(src_data[i]))
                    for j in dec:
                        self.sp_sym[j] = dec[j]
                    check |= 32
            self.calc_show_pl()
            self.pl_enb.clear()
            self.pl_enb |= self.pl_crd_enb & self.pl_asp_enb
        except BaseException as error:
            ut.error_log(error)

        if check != 63:
            self.cat_pl.clear()
            self.pl_crd_enb.clear()
            self.pl_asp_enb.clear()
            self.pl_enb.clear()
            self.sg_sym.clear()
            self.cs_sym.clear()
            self.sp_sym.clear()
            for i in AstroBaseObject.cat_pl:
                self.cat_pl[i] = AstroBaseObject.cat_pl[i]
            self.pl_crd_enb |= AstroBaseObject.pl_crd_enb
            self.pl_asp_enb |= AstroBaseObject.pl_asp_enb
            self.pl_enb |= self.pl_crd_enb & self.pl_asp_enb
            for i in AstroBaseObject.sg_sym:
                self.sg_sym[i] = AstroBaseObject.sg_sym[i]
                self.cs_sym[i] = AstroBaseObject.cs_sym[i]
            for i in AstroBaseObject.sp_sym:
                self.sp_sym[i] = AstroBaseObject.sp_sym[i]
            self.calc_show_pl()
            self.flag = 1

    def calc_show_pl(self):
        self.show_pl.clear()
        seq = set(self.base_pl) ^ set(self.cat_pl.keys())
        seq = self.base_pl + sorted(list(seq))
        for i in seq:
            if i in self.pl_crd_enb:
                self.show_pl.append(i)

    def upd_catalog(self, ind, sym=None, mode=1):
        if sym is None:
            del self.cat_pl[ind]
            del self.pl_spd_sym[ind]
            del self.pl_crd_s[ind]
            del self.pl_spd_val[ind]
            del self.pl_crd_h[ind]
            del self.pl_sgn[ind]
            del self.pl_hse[ind]
            del self.pl_str[ind]
            self.pl_crd_enb.discard(ind)
            self.pl_asp_enb.discard(ind)
            self.pl_enb.discard(ind)
            self.calc_show_pl()
        elif mode:
            self.cat_pl[ind] = sym
        else:
            self.cat_pl[ind] = sym
            buf = swe.calc_ut(self.jul_day, ind)[0]
            self.pl_crd_s[ind] = buf[0]
            self.pl_spd_val[ind] = buf[3]
            self.calc_pl_crd_h(ind)
            self.pl_sgn[ind] = int(self.pl_crd_s[ind]/30)
            self.pl_hse[ind] = int(self.pl_crd_h[ind]/30)
            self.set_spd_sym(ind)
            self.pl_str[ind] = self.format_crd(self.pl_crd_s[ind], self.pl_sgn[ind])
        self.flag = 1

    def swi_enb_sing(self, ind, mode=1):
        if mode:
            if ind in self.pl_asp_enb:
                self.pl_asp_enb.discard(ind)
            else:
                self.pl_asp_enb.add(ind)
        else:
            if ind in self.pl_crd_enb:
                self.pl_crd_enb.discard(ind)
            else:
                self.pl_crd_enb.add(ind)
            self.calc_show_pl()

        if ind in self.pl_crd_enb and ind in self.pl_asp_enb:
            self.pl_enb.add(ind)
        else:
            self.pl_enb.discard(ind)
        self.flag = 1

    def swi_enb_mast(self, mode=1):
        if mode:
            if self.pl_asp_enb:
                self.pl_asp_enb.clear()
                self.pl_enb.clear()
            else:
                self.pl_asp_enb |= set(self.cat_pl.keys())
                self.pl_enb.clear()
                self.pl_enb |= self.pl_crd_enb & self.pl_asp_enb
        else:
            if self.pl_crd_enb:
                self.pl_crd_enb.clear()
                self.pl_enb.clear()
                self.show_pl.clear()
            else:
                self.pl_crd_enb |= set(self.cat_pl.keys())
                self.pl_enb.clear()
                self.pl_enb |= self.pl_crd_enb & self.pl_asp_enb
                self.calc_show_pl()

    def swe_valid(self, ind):
        try:
            swe.calc_ut(self.jul_day, ind)
            return True
        except swe.Error:
            return False

    @staticmethod
    def get_eph_rng():
        min_y, year = 0, 0
        try:
            while True:
                jul_day = swe.julday(2020 - year, 1, 1, 1)
                swe.calc_ut(jul_day, 15)
                year += 1
        except swe.Error:
            min_y = 2021 - year
        try:
            year = 0
            while True:
                jul_day = swe.julday(2020 + year, 1, 1, 1)
                swe.calc_ut(jul_day, 15)
                year += 1
        except swe.Error:
            return min_y, 2017 + year

    @staticmethod
    def get_pl_name(ind, res_name=''):
        exc = {11: 'Rahu', 23: 'Ketu', 12: 'Lilit', 56: 'Selena'}
        if ind == '':
            return res_name
        if ind in exc:
            return exc[ind]
        else:
            name = swe.get_planet_name(ind)
            if name.isdigit():
                return 'name not found'
            return name

    def format_crd(self, crd, sgn):
        hh = crd - 30*sgn
        mm = (hh - int(hh)) * 60
        ss = (mm - int(mm)) * 60
        buf = '%2d; ' % hh if hh > 9 else ' %2d; ' % hh
        buf = buf + '%2d\' ' % mm if mm > 9 else buf + ' %2d\' ' % mm
        buf = buf + '%2d" ' % ss if ss > 9 else buf + ' %2d" ' % ss
        buf += ' %s' % self.sg_sym[sgn]
        return buf

# -------------------------------------------------------------------------------------------------------------------- #
