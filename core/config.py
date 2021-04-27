# -------------------------------------------------------------------------------------------------------------------- #

import json
import core.utilities as ut

# @formatter:off


class ConfigKeys:
    ini = 'Config/config.ini'
    cfg = ''
    svc = 0
    """
        ----------------------------------------------------------------------------------------------------------------
        act_var:
            2 cur_db, 3 cur_apg, 4 acc, 5 bit 1/2/3/4 zp/deg/spd/csp enb,
            8 acf b1/b2 ast/ext, 9 cell_enb, 11 core_calc_meth, 12 stb_inv, 14 core_cos_hor_swi,
            15 core_det_st, 16 stb_calc_meth, 17 esd_show_str, 19 moon_day_meth, 20 cst_det_st, 21 ash_det_st,
            22 fix_star_enb, 24 app_state, 25 lang, others indexes for data exchanging
        
        rep_var: technical data for map positioning
        ----------------------------------------------------------------------------------------------------------------
    """
    act_var = {
        2: 'Current', 3: '', 4: 2, 5: 15, 8: 0, 9: 4095, 11: 0, 12: 1, 14: 3, 15: 2, 16: 0, 17: 15,
        19: 0, 20: 1, 21: 0, 22: 1, 24: 'normal', 25: 'English'
    }
    path = {0: 'Swiss', 2: 'DataBase', 3: 'AspectPages', 5: 'AspectConfigs'}
    cur_plc = {
        'place': 'Krasnodar, Krasnodar Territory, Russia', 'lat': (45, 2, 0, 'n'), 'lon': (39, 0, 0, 'e'), 'utc': 3
    }

    font = {
        'AppBsc': ['Arial', 12], 'AppSym': ['HamburgSymbols', 12], 'AppSpc': ['Arial', 9], 'AppCns': ['Arial', 12],
        'CellText': ['Arial', 12], 'CellSym': ['HamburgSymbols', 12], 'PnSym': ['HamburgSymbols', 15],
        'SgSym': ['HamburgSymbols', 14], 'CsSym': ['Arial', 11], 'AsMrk1': ['Arial', 8],
        'AsMrk2': ['HamburgSymbols', 12], 'StbMrk': ['Arial', 10]
    }
    app_dim = {'TopHgtNr': 51, 'TopHgtZm': 43, 'OsFootHgt': 92, 'PyFrmTop': 0}
    app_col = {
        'ToolBkg': '#F0F0F0', 'ToolFrg': '#000000', 'FootBkg': '#F0F0F0', 'FootFrg': '#000000', 'CellBkg': '#FFFFFF',
        'CellFont': '#000000', 'AcfMrk': '#A000FF'
    }

    dtc_geo = {'w': 400, 'h': 80, 'x': 0, 'y': 0, 'mnw': 100, 'mxw': 800, 'mnh': 33, 'mxh': 300, 'mnx': 0, 'mny': 0}
    dtc_dim = {'PadX': 13, 'PadY': 40}

    edt_geo = {'w': 120, 'h': 80, 'x': 0, 'y': 80, 'mnw': 100, 'mxw': 300, 'mnh': 23, 'mxh': 200, 'mnx': 0, 'mny': 0}
    edt_dim = {'PadX': 13, 'PadY': 10}

    rec_geo = {'w': 210, 'h': 110, 'x': 0, 'y': 0, 'mnw': 100, 'mxw': 800, 'mnh': 23, 'mxh': 500, 'mnx': 0, 'mny': 0}
    rec_dim = {'PadX': 13, 'PadY': 13, 'Count': 4, 'Step': 21}

    esd_geo = {'w': 210, 'h': 90, 'x': 0, 'y': 0, 'mnw': 100, 'mxw': 450, 'mnh': 23, 'mxh': 700, 'mnx': 0, 'mny': 0}
    esd_dim = {
        'PadX': 13, 'PadY': 13, 'Step': 21, 'InHeart': 53, 'InBurn': 70, 'SunZone': 68, 'FreeZone': 75,
        'Antaeus': 63, 'Icarus': 45, 'Atlas': 40, 'Sisyphus': 68, 'RexAsp': 117, 'InPit': 38,
        'Doriph': 82, 'Auriga': 50, 'Anareta': 60, 'Alcocoden': 80, 'DGenitura': 130
    }

    map_geo = {'w': 0, 'h': 0, 'x': 0, 'y': 0, 'mnw': 800, 'mxw': 1500, 'mnh': 800, 'mxh': 1500, 'mnx': 0, 'mny': 0}
    map_dim = {
        'BkgOval': 430, 'SgRad': 370, 'SgWid': 25, 'InsOval': 242, 'PnCirRad': 280, 'PnMrkRad': 3, 'PnLineExt': 20,
        'AsUniRad': 25, 'AsMrkRad': 7, 'BtwPnSpc': 6, 'CsLineExt': 225, 'CsSymExt': 215, 'CsSymRot': 2, 'PnDegPx': 14,
        'PnDegPy': 5, 'PnSpdPx': 14, 'PnSpdPy': 3,  'CsDegPx': 18, 'CsDegPy': 4
    }
    map_col = {
        'BkgOval': '#E2EDFA', 'Border': '#808080', 'SgSym': '#000000', 'SgFire': '#E66159', 'SgLand': '#008000',
        'SgAir': '#FFFF00', 'SgWater': '#0080FF', 'PnSym': '#000000', 'PnLine': '#2F97BB', 'CsSym': '#000000',
        'CsLine': '#808080'
    }

    crd_geo = {'w': 200, 'h': 660, 'x': 0, 'y': 0, 'mnw': 100, 'mxw': 600, 'mnh': 33, 'mxh': 1200, 'mnx': 0, 'mny': 0}
    crd_dim = {
        'PadX': 5, 'PadY': 30, 'Step': 21, 'PnSymPx': 10, 'PnCrdPx': 130, 'KdMrkPx': 143, 'StarPx': 145, 'StarDy': -1
    }
    crd_col = {
        'Ruler': '#228B22', 'Detriment': '#DC143C', 'Exaltation': '#0000CD', 'Fall': '#9932CC',
        'Neutral': '#000000', 'KngDgMrk': '#EE0000', 'DesDgMrk': '#000000'
    }

    stb_geo = {'w': 150, 'h': 660, 'x': 0, 'y': 0, 'mnw': 100, 'mxw': 500, 'mnh': 37, 'mxh': 800, 'mnx': 0, 'mny': 0}
    stb_dim = {'PadX': 10, 'StLineW': 5, 'StLineDy': 3, 'StatMul': 10, 'AshMul': 22, 'MrkLineW': 1}
    stb_col = {
        'PosStat': '#00A800', 'NegStat': '#FF0000', 'AshPow': '#D9D9D9', 'AshCre': '#0080FF', 'MrkLine': '#606060'
    }

    acf_geo = {'w': 250, 'h': 250, 'x': 0, 'y': 0, 'mnw': 200, 'mxw': 450, 'mnh': 33, 'mxh': 800, 'mnx': 0, 'mny': 0}
    acf_dim = {'ZeroPnt': 85, 'Step': 23, 'PnPadX': 20, 'PadX': 20, 'PadY': 20, 'SnsZnScl': 6}

    asc_geo = {'w': 150, 'h': 70, 'x': 0, 'y': 0, 'mnw': 170, 'mxw': 300, 'mnh': 33, 'mxh': 150, 'mnx': 0, 'mny': 0}
    asc_dim = {'PadX': 20, 'PadY': 20, 'Step': 26}
    asc_col = {'Dominant': '#00BB00', 'Weak': '#D0D0D0', 'Neutral': '#000000'}

    cor_geo = {'w': 550, 'h': 250, 'x': 0, 'y': 0, 'mnw': 150, 'mxw': 800, 'mnh': 33, 'mxh': 450, 'mnx': 0, 'mny': 0}
    cor_dim = {'Step': 26, 'PxCos': 20, 'PxHor': 280, 'PadY': 20, 'TitleDx': -2}
    cor_col = {'Dominant': '#00BB00', 'Weak': '#D0D0D0', 'Neutral': '#000000'}

    apg_geo = {'w': 1551, 'h': 621, 'x': 150, 'y': 150}
    apg_dim = {'CellWid': 60, 'CellHgt': 30, 'TreeWid': 210}
    apg_col = {
        'BkgCol': '#FFFFFF', 'FrgCol': '#000000', 'CellFrm': '#D0D0D0',
        'AspEnb': '#0000FF', 'AspDis': '#D0D0D0',  'EntMrk': '#FF0000'
    }
    ase_col = {
        'Unions': '#008000', 'InsAsp': '#000000', 'HrmAsp': '#F00000', 'CrvAsp': '#00C800', 'KrmAsp': '#0080FF',
        'SprAsp': '#9400D3', 'ErsAsp': '#DAA520'
    }

    atb_geo = {'w': 1040, 'h': 530, 'x': 150, 'y': 150}
    atb_dim = {'CellWid': 60, 'CellHgt': 30}
    atb_col = {
        'BkgCol': '#FFFFFF', 'FrgCol': '#000000', 'CellFrm': '#D0D0D0', 'EmpCell': '#E2EDFA', 'NonAsp': '#A0A0A0',
        'EntMrk': '#FF0000', 'PchCell': '#E0E0E0', 'ResBkg': '#DC143C', 'ResFrg': '#FFFFFF'
    }

    dbs_geo = {'w': 1110, 'h': 600, 'x': 150, 'y': 150}
    pct_geo = {'w': 350, 'h': 410, 'x': 150, 'y': 150}
    tmc_geo = {'x': 200, 'y': 200}
    cfg_geo = {'x': 200, 'y': 200}

    rep_var = {
        0: 25, 1: 0, 2: 0.17, 3: 0, 4: 400, 5: 80, 6: 0, 7: 0, 8: 120, 9: 80, 10: 0, 11: 80, 12: 210, 13: 110,
        14: 0, 15: 13, 16: 200, 17: 352, 18: 0, 19: 352, 20: 485, 21: 210, 22: 530, 23: 210, 24: 280, 25: 660,
        26: 280, 27: 0, 28: 150, 29: 18, 30: 430, 31: 1, 32: 250, 33: 250, 34: 530, 35: 530, 36: 170, 37: 70,
        38: 523, 39: 280
    }

    def __init__(self):
        self.ord_list = []
        self.child = {i: None for i in range(1, 8)}
        self.wch_dbs = None
        self.act_var = {23: 1}
        self.path = {}
        self.cur_plc = {}

        self.font = {}
        self.app_dim = {}
        self.app_col = {}
        self.dtc_geo = {}
        self.dtc_dim = {}
        self.edt_geo = {}
        self.edt_dim = {}
        self.rec_geo = {}
        self.rec_dim = {}
        self.esd_geo = {}
        self.esd_dim = {}
        self.map_geo = {}
        self.map_dim = {}
        self.map_col = {}
        self.crd_geo = {}
        self.crd_dim = {}
        self.crd_col = {}
        self.stb_geo = {}
        self.stb_dim = {}
        self.stb_col = {}
        self.acf_geo = {}
        self.acf_dim = {}
        self.asc_geo = {}
        self.asc_dim = {}
        self.asc_col = {}
        self.cor_geo = {}
        self.cor_dim = {}
        self.cor_col = {}

        self.apg_geo = {}
        self.apg_dim = {}
        self.apg_col = {}
        self.ase_col = {}
        self.atb_geo = {}
        self.atb_dim = {}
        self.atb_col = {}
        self.dbs_geo = {}
        self.pct_geo = {}
        self.tmc_geo = {}
        self.cfg_geo = {}
        self.rep_var = {}

        self.sam_act = {
            'act_var': self.act_var, 'path': self.path, 'cur_plc': self.cur_plc, 'font': self.font,
            'app_dim': self.app_dim, 'app_col': self.app_col, 'dtc_geo': self.dtc_geo, 'dtc_dim': self.dtc_dim,
            'edt_geo': self.edt_geo, 'edt_dim': self.edt_dim, 'rec_geo': self.rec_geo, 'rec_dim': self.rec_dim,
            'esd_geo': self.esd_geo, 'esd_dim': self.esd_dim, 'map_geo': self.map_geo, 'map_dim': self.map_dim,
            'map_col': self.map_col, 'crd_geo': self.crd_geo, 'crd_dim': self.crd_dim, 'crd_col': self.crd_col,
            'stb_geo': self.stb_geo, 'stb_dim': self.stb_dim, 'stb_col': self.stb_col, 'acf_geo': self.acf_geo,
            'acf_dim': self.acf_dim, 'asc_geo': self.asc_geo, 'asc_dim': self.asc_dim, 'asc_col': self.asc_col,
            'cor_geo': self.cor_geo, 'cor_dim': self.cor_dim, 'cor_col': self.cor_col,
            'apg_geo': self.apg_geo, 'apg_dim': self.apg_dim, 'apg_col': self.apg_col, 'ase_col': self.ase_col,
            'atb_geo': self.atb_geo, 'atb_dim': self.atb_dim, 'atb_col': self.atb_col, 'dbs_geo': self.dbs_geo,
            'pct_geo': self.pct_geo, 'tmc_geo': self.tmc_geo, 'cfg_geo': self.cfg_geo, 'rep_var': self.rep_var
        }
        self.sam_pas = {
            'act_var': ConfigKeys.act_var, 'path': ConfigKeys.path, 'cur_plc': ConfigKeys.cur_plc,
            'font': ConfigKeys.font, 'app_dim': ConfigKeys.app_dim, 'app_col': ConfigKeys.app_col,
            'dtc_geo': ConfigKeys.dtc_geo, 'dtc_dim': ConfigKeys.dtc_dim, 'edt_geo': ConfigKeys.edt_geo,
            'edt_dim': ConfigKeys.edt_dim, 'rec_geo': ConfigKeys.rec_geo, 'rec_dim': ConfigKeys.rec_dim,
            'esd_geo': ConfigKeys.esd_geo, 'esd_dim': ConfigKeys.esd_dim, 'map_geo': ConfigKeys.map_geo,
            'map_dim': ConfigKeys.map_dim, 'map_col': ConfigKeys.map_col, 'crd_geo': ConfigKeys.crd_geo,
            'crd_dim': ConfigKeys.crd_dim, 'crd_col': ConfigKeys.crd_col, 'stb_geo': ConfigKeys.stb_geo,
            'stb_dim': ConfigKeys.stb_dim, 'stb_col': ConfigKeys.stb_col, 'acf_geo': ConfigKeys.acf_geo,
            'acf_dim': ConfigKeys.acf_dim, 'asc_geo': ConfigKeys.asc_geo, 'asc_dim': ConfigKeys.asc_dim,
            'asc_col': ConfigKeys.asc_col, 'cor_geo': ConfigKeys.cor_geo, 'cor_dim': ConfigKeys.cor_dim,
            'cor_col': ConfigKeys.cor_col, 'apg_geo': ConfigKeys.apg_geo, 'apg_dim': ConfigKeys.apg_dim,
            'apg_col': ConfigKeys.apg_col, 'ase_col': ConfigKeys.ase_col, 'atb_geo': ConfigKeys.atb_geo,
            'atb_dim': ConfigKeys.atb_dim, 'atb_col': ConfigKeys.atb_col, 'dbs_geo': ConfigKeys.dbs_geo,
            'pct_geo': ConfigKeys.pct_geo, 'tmc_geo': ConfigKeys.tmc_geo, 'cfg_geo': ConfigKeys.cfg_geo,
            'rep_var': ConfigKeys.rep_var
        }

        try:
            with open(self.ini) as fp:
                cfg = fp.read()
                fp.close()
        except BaseException as error:
            ut.error_log(error)
            cfg = ''

        self.reload(cfg, 0)

    def reload(self, cfg, mode=1):
        cnt = 0
        try:
            with open('Config/%s.json' % cfg) as fp:
                src = json.load(fp)
                fp.close()

            for i in range(1, len(src), 2):
                key = src[i-1]
                if mode and key == 'act_var':
                    cnt += 19
                    continue
                dec = dict(json.loads(src[i]))
                if key == 'cur_plc':
                    dec['lat'] = tuple(dec['lat'])
                    dec['lon'] = tuple(dec['lon'])
                for j in dec:
                    self.sam_act[key][j] = dec[j]
                    cnt += 1
        except BaseException as error:
            ut.error_log(error)

        if cnt == 338:
            self.cfg = cfg
            self.svc = mode
            self.act_var[13] = 0
        else:
            self.cfg = 'Builtin'
            self.svc = 1
            self.act_var[13] = 1

            for i in self.sam_pas:
                if mode and i == 'act_var':
                    continue
                if i == 'font':
                    for j in self.sam_pas[i]:
                        self.sam_act[i][j] = self.sam_pas[i][j].copy()
                else:
                    for j in self.sam_pas[i]:
                        self.sam_act[i][j] = self.sam_pas[i][j]

        with open(self.ini, 'w') as fp:
            fp.write(self.cfg)
            fp.close()

    def dump(self):
        if self.svc:
            self.svc = 0
            enc = []
            for i in self.sam_act:
                if i == 'act_var':
                    buf = {j: self.act_var[j] for j in self.act_var if j not in {1, 6, 7, 10, 13, 18, 23}}
                    buf = list(buf.items())
                else:
                    buf = list(self.sam_act[i].items())
                enc += [i, json.dumps(buf)]

            with open('Config/%s.json' % self.cfg, 'w') as fp:
                json.dump(enc, fp, separators=(',\n', ': '))
                fp.close()

    def calc_repos(self, width, height):
        self.svc = 1
        self.act_var[13] = 0
        rep = self.rep_var

        self.map_geo['w'] = height + rep[0]
        self.map_geo['h'] = height - rep[1]
        self.map_geo['x'] = round(rep[2]*width)
        self.map_geo['y'] = rep[3]

        self.dtc_geo['w'] = rep[4]
        self.dtc_geo['h'] = rep[5]
        self.dtc_geo['x'] = rep[6]
        self.dtc_geo['y'] = rep[7]

        self.edt_geo['w'] = rep[8]
        self.edt_geo['h'] = rep[9]
        self.edt_geo['x'] = rep[10]
        self.edt_geo['y'] = rep[11]

        self.rec_geo['w'] = rep[12]
        self.rec_geo['h'] = rep[13]
        self.rec_geo['x'] = rep[14]
        self.rec_geo['y'] = 0.5*height - rep[15]

        self.esd_geo['w'] = rep[16]
        self.esd_geo['h'] = rep[17]
        self.esd_geo['x'] = rep[18]
        self.esd_geo['y'] = height - rep[19]

        self.cor_geo['w'] = rep[20]
        self.cor_geo['h'] = rep[21]
        self.cor_geo['x'] = width - rep[22]
        self.cor_geo['y'] = height - rep[23]

        self.crd_geo['w'] = rep[24]
        self.crd_geo['h'] = rep[25]
        self.crd_geo['x'] = width - rep[26]
        self.crd_geo['y'] = rep[27]

        self.stb_geo['w'] = rep[28]
        self.stb_geo['h'] = self.crd_dim['Step'] * rep[29]
        self.stb_geo['x'] = width - rep[30]
        self.stb_geo['y'] = self.crd_geo['y']
        self.act_var[12] = rep[31]

        self.acf_geo['w'] = rep[32]
        self.acf_geo['h'] = rep[33]
        self.acf_geo['x'] = width - rep[34]
        self.acf_geo['y'] = height - rep[35]

        self.asc_geo['w'] = rep[36]
        self.asc_geo['h'] = rep[37]
        self.asc_geo['x'] = width - rep[38]
        self.asc_geo['y'] = height - rep[39]

    def save_repos(self, width, height):
        self.svc = 1
        rep = self.rep_var

        rep[0] = self.map_geo['w'] - height
        rep[1] = height - self.map_geo['h']
        rep[2] = self.map_geo['x'] / width
        rep[3] = self.map_geo['y']

        rep[4] = self.dtc_geo['w']
        rep[5] = self.dtc_geo['h']
        rep[6] = self.dtc_geo['x']
        rep[7] = self.dtc_geo['y']

        rep[8] = self.edt_geo['w']
        rep[9] = self.edt_geo['h']
        rep[10] = self.edt_geo['x']
        rep[11] = self.edt_geo['y']

        rep[12] = self.rec_geo['w']
        rep[13] = self.rec_geo['h']
        rep[14] = self.rec_geo['x']
        rep[15] = 0.5*height - self.rec_geo['y']

        rep[16] = self.esd_geo['w']
        rep[17] = self.esd_geo['h']
        rep[18] = self.esd_geo['x']
        rep[19] = height - self.esd_geo['y']

        rep[20] = self.cor_geo['w']
        rep[21] = self.cor_geo['h']
        rep[22] = width - self.cor_geo['x']
        rep[23] = height - self.cor_geo['y']

        rep[24] = self.crd_geo['w']
        rep[25] = self.crd_geo['h']
        rep[26] = width - self.crd_geo['x']
        rep[27] = self.crd_geo['y']

        rep[28] = self.stb_geo['w']
        rep[29] = self.stb_geo['h'] / self.crd_dim['Step']
        rep[30] = width - self.stb_geo['x']
        self.stb_geo['y'] = self.crd_geo['y']
        rep[31] = self.act_var[12]

        rep[32] = self.acf_geo['w']
        rep[33] = self.acf_geo['h']
        rep[34] = width - self.acf_geo['x']
        rep[35] = height - self.acf_geo['y']

        rep[36] = self.asc_geo['w']
        rep[37] = self.asc_geo['h']
        rep[38] = width - self.asc_geo['x']
        rep[39] = height - self.asc_geo['y']

    def set_cfg_name(self, name):
        self.cfg = name
        with open(self.ini, 'w') as fp:
            fp.write(self.cfg)
            fp.close()

    def get_cur_cfg(self): return self.cfg
    def set_save_flag(self, val): self.svc = val
    def get_app_pth(self): return self.path
    def get_cur_plc(self): return self.cur_plc
    def get_src_font(self): return self.font
    def get_act_var(self): return self.act_var

    def set_act_var(self, ind, val):
        self.act_var[ind] = val
        if ind not in {13, 23}:
            self.svc = 1

    def get_app_chd(self): return self.child
    def set_app_chd(self, ind, chd): self.child[ind] = chd

    def lnk_wch_dbs(self, var): self.wch_dbs = var
    def get_wch_dbs(self): return self.wch_dbs
    def set_wch_dbs(self, val): self.wch_dbs.set(val)

    def get_ord_list(self): return self.ord_list

    def set_ord_list(self, ind, mode=1):
        if ind in self.ord_list:
            self.ord_list.remove(ind)
        if mode:
            self.ord_list.append(ind)

    def get_c_geo(self, ind):
        if ind == 1:
            return self.map_geo
        elif ind == 2:
            return self.dtc_geo
        elif ind == 4:
            return self.edt_geo
        elif ind == 8:
            return self.cor_geo
        elif ind == 16:
            return self.crd_geo
        elif ind == 32:
            return self.stb_geo
        elif ind == 256:
            return self.acf_geo
        elif ind == 512:
            return self.asc_geo
        elif ind == 1024:
            return self.esd_geo
        elif ind == 2048:
            return self.rec_geo

    def set_c_geo(self, ind, **kwargs):
        if ind == 1:
            geo = self.map_geo
        elif ind == 2:
            geo = self.dtc_geo
        elif ind == 4:
            geo = self.edt_geo
        elif ind == 8:
            geo = self.cor_geo
        elif ind == 16:
            geo = self.crd_geo
        elif ind == 32:
            geo = self.stb_geo
        elif ind == 256:
            geo = self.acf_geo
        elif ind == 512:
            geo = self.asc_geo
        elif ind == 1024:
            geo = self.esd_geo
        elif ind == 2048:
            geo = self.rec_geo
        else:
            return None

        for i in kwargs:
            geo[i] = kwargs[i]

        self.svc = 1

    def get_c_col(self, ind):
        if ind == 0:
            return self.app_col
        elif ind == 1:
            return self.map_col
        elif ind == 3:
            return self.crd_col
        elif ind == 4:
            return self.stb_col
        elif ind == 5:
            return self.cor_col
        elif ind == 6:
            return self.asc_col

    def get_c_dim(self, ind):
        if ind == 0:
            return self.app_dim
        elif ind == 1:
            return self.map_dim
        elif ind == 2:
            return self.dtc_dim
        elif ind == 3:
            return self.crd_dim
        elif ind == 4:
            return self.stb_dim
        elif ind == 5:
            return self.cor_dim
        elif ind == 6:
            return self.asc_dim
        elif ind == 7:
            return self.acf_dim
        elif ind == 8:
            return self.esd_dim
        elif ind == 9:
            return self.rec_dim
        elif ind == 10:
            return self.edt_dim

    def get_chd_geo(self, ind):
        if ind == 2:
            return self.dbs_geo
        elif ind == 3:
            return self.apg_geo
        elif ind == 4:
            return self.pct_geo
        elif ind == 5:
            return self.atb_geo
        elif ind == 6:
            return self.tmc_geo
        elif ind == 7:
            return self.cfg_geo

    def set_chd_geo(self, ind, **kwargs):
        if ind == 2:
            geo = self.dbs_geo
        elif ind == 3:
            geo = self.apg_geo
        elif ind == 4:
            geo = self.pct_geo
        elif ind == 5:
            geo = self.atb_geo
        elif ind == 6:
            geo = self.tmc_geo
        elif ind == 7:
            geo = self.cfg_geo
        else:
            return None

        for i in kwargs:
            geo[i] = kwargs[i]

        self.svc = 1

    def get_apg_dim(self): return self.apg_dim
    def get_apg_col(self): return self.apg_col
    def get_ase_col(self): return self.ase_col

    def get_atb_dim(self): return self.atb_dim
    def get_atb_col(self): return self.atb_col

# -------------------------------------------------------------------------------------------------------------------- #
