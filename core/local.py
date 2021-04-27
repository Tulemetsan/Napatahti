# -------------------------------------------------------------------------------------------------------------------- #

import json
import core.utilities as ut

# @formatter:off


class LocalKeywords:
    tkw = {
        'new': 'New', 'edit': 'Edit', 'apply': 'Apply', 'close': 'Close', 'save': 'Save', 'delete': 'Delete',
        'open': 'Open', 'rename': 'Rename', 'ok': 'Ok', 'cancel': 'Cancel', 'qwsDel': 'Do you want to delete?',
        'saveAs': 'Save as', 'copy': 'Copy', 'insert': 'Insert', 'enable': 'Enable', 'disable': 'Disable', 'cut': 'Cut',
        'reset': 'Reset', 'set': 'Settings', 'src': 'Source', 'about': 'About', 'conf': 'Config', 'lang': 'Language',
        'qwsRep': 'Save current position as\ndefault?', 'qwsLoc': 'Needs restart program for\nfull apply new language.'
    }
    mkw = {
        'quit': 'Quit', 'file': 'File', 'view': 'View', 'options': 'Options', 'tools': 'Tools',
        'stbTit': 'Status bar', 'stbBoth': 'View both', 'stbCos': 'Cosmogram', 'stbHor': 'Horoscope',
        'stMethGlo': 'Globa PP', 'stMethSch': 'Schitov BB',
        'acfTit': 'Aspect config', 'acfCls': 'Classic only', 'acfBnd': 'Bonds only', 'acfAst': 'Use asteroids',
        'dtcTit': 'Data header', 'edtTit': 'Extended data', 'mapTit': 'Zodiac circle', 'corTit': 'Core statistics',
        'crdTit': 'Coordinates', 'tBar': 'Tools bar', 'repMap': 'Reposition', 'fBar': 'Footer bar',
        'astTit': 'Aspect statistic', 'stbCalc': 'Calculate', 'priSt': 'Prime status', 'ashSt': 'Asha status',
        'ashKn': 'Normal KD', 'ashCr': 'Normal CR', 'ashDet': 'Detailed', 'esdTit': 'Essential data',
        'apg': 'Aspect pages', 'cat': 'Planet catalog', 'dbs': 'Data base', 'atb': 'Aspect table',
        'inv': 'Invert', 'sync': 'Synchronize', 'mdWest': 'Western', 'mdJyot': 'Jyotisa', 'recTit': 'Receptions tree',
        'essTit': 'Essential status', 'r&pTit': 'Aspect status', 'd&aTit': 'Doriphoros/Auriga',
        'sunTit': 'Sun relation zones', 'csmSt': 'Cosmic status', 'csmSum': 'Summary', 'csmDet': 'Detailed',
        'degEnb': 'Degree symbol', 'spdEnb': 'Speed symbol', 'zpAri': 'Zero point Ari', 'zpAsc': 'Zero point Asc',
        'cspEnb': 'Show cuspids', 'tmc': 'Time counter', 'fxs': 'Fixed stars', 'genTit': 'General',
        'apgTit': 'Aspect page', 'atbTit': 'Aspect table', 'appCfg': 'Application', 'mpcCfg': 'Map cells',
        'essCol': 'Essential colors'
    }
    fkw = {'dbsNew': 'NEW', 'dbsRec': 'REC'}

    w_day = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    month = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'july',
        8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    ckw = {
        'md': 'm.d.', 'cosTit': 'Cosmogram', 'horTit': 'Horoscope', 'coreTit': 'Core', 2: 'S', 1: 'F', 0: 'A',
        'mdFull': 'Moon day', 'beg': 'Begin', 'end': 'End', 'sum': 'Total', 'fullMon': 'Full moon',
        'InHeart': 'In heart', 'InBurn': 'In burning', 'SunZone': 'Sun zone', 'FreeZone': 'Free zone',
        'Atlas': 'Atlas', 'Sisyphus': 'Sisyphus', 'Antaeus': 'Antaeus', 'Icarus': 'Icarus', 'RexAsp': 'Rex aspectarius',
        'InPit': 'In pit', 'Doriph': 'Doriphoros', 'Auriga': 'Auriga', 'Anareta': 'Anareta', 'Alcocoden': 'Alcocoden',
        'DGenitura': 'Dominus Genitura', 'defName': 'Today'
    }
    acf_name = {
        0: 'Core', 1: 'Stellium', 2: 'Cross', 3: 'Tau-quadrat', 4: 'Pole-axe', 5: 'Dart',
        6: 'Big trine', 7: 'Bisextile', 8: 'Forks', 9: 'Roof',
        10: 'Prism', 11: 'Palm', 12: 'Ship', 13: 'Boat',
        14: 'Arcan', 15: 'Tunnel', 16: 'Wedge', 17: 'Lock', 18: 'Leash', 19: 'Case',
        20: 'Sword', 21: 'Springboard', 22: 'Staff', 23: 'Bell', 24: 'Carriage', 25: 'Flute', 26: 'Sphinx',
        27: 'Veil', 28: 'Liana', 29: 'Torch',  30: 'Geyser', 31: 'Envelope', 32: 'Shield', 33: 'Crossbow', 34: 'Tyn',
        35: 'Arch', 36: 'Loom', 37: 'Nectar',
        38: 'Anvil', 39: 'Iron', 40: 'Stretching',
        41: 'Source', 42: 'Airship', 43: 'Sprout', 44: 'Bridge', 45: 'Parrot', 46: 'Statue', 47: 'Lifts',
        48: 'Boomerang', 49: 'Hawk',
        50: 'Trail', 51: 'Diary', 52: 'Pump', 53: 'Mill',
        54: 'Spring', 55: 'Fortress', 56: 'Insulator', 57: 'Hole', 58: 'Gyroscope', 59: 'Quagmire',
        60: 'Tower', 61: 'Collar', 62: 'Oasis', 63: 'Stigma', 64: 'Trap', 65: 'Template', 66: 'Vase', 67: 'Bonds',
        68: 'Chest', 69: 'Petrov cross', 70: 'Laser', 71: 'Biseptile', 72: 'Tree', 73: 'Shuttle'
    }

    dbs_kwd = {
        'dbName': 'Current', 'title': 'Data base', 'ind': 'Ind', 'name': 'Name', 'date': 'Date', 'time': 'Time',
        'utc': 'UTC', 'place': 'Place', 'lat': 'Lat', 'lon': 'Lon', 'sex': 'Sex', 'org': 'Organize'
    }
    sex_kwd = {'E': 'Event', 'M': 'Male', 'F': 'Female'}
    hss_kwd = {
        'P': 'Placidus', 'K': 'Koch', 'D': 'Equal MC', 'A': 'Equal AC', 'S': 'Sripati',
        'O': 'Porphyrius', 'C': 'Campanus', 'B': 'Alcabitus'
    }

    apg_kwd = {
        'title': 'Aspect pages and samples', 'treePg': 'Pages', 'treeSm': 'Samples', 'bltPg': 'Builtin',
        'bltSm': 'All aspects', 'pmStatOn': 'Status On', 'pmStatOff': 'Status Off', 'pmTitle': 'Aspect',
        'pmAccTit': 'Accuracy', 'pmAccAll': 'View all', 'pmAccN': 'Normal', 'pmAcc+': 'Accurate+',
        'pmAcc-': 'Accurate-', 'enb': 'E', 'dis': 'D'
    }
    apg_head = {
        0: '+', 1: 'Value', 2: 'Style', 3: 'E/D', 4: 'Q', 5: 'W', 6: 'E', 7: 'R', 8: 'T', 9: 'Y', 10: 'U', 11: 'I',
        12: 'O', 13: 'P', 14: '{', 15: '}', 16: '`', 17: 'Ñ', 18: 'Ð', 19: 'M', 20: 't', 21: 'Cuspid',
        22: 'm0', 23: 'm1', 24: 'm2', 25: 'm3', 26: 'm4', 27: 'Point'
    }
    ase_kwd = {
        'save': 'Save', 'delete': 'Delete', 'close': 'Close', 'val': 'Index', 'sym': 'Symbol',
        'newAsp': 'New aspect', 'editAsp': 'Edit aspect'
    }

    pct_kwd = {
        'title': 'Planet catalog', 'crd': 'Coordinate', 'pmTitle': 'Catalog', 'newTitle': 'New planet',
        'asp': 'Asp', 'aspOn': 'Aspect On', 'aspOff': 'Aspect Off', 'id': 'ID',  'enbDis': 'E/D', 'sym': 'Symbol'
    }
    pce_kwd = {'save': 'Save', 'delete': 'Delete', 'close': 'Close', 'ind': 'Index', 'sym': 'Symbol'}

    avw_kwd = {
        'key': 'Aspect', 'val': 'Value', 'asp': 'Aspect', 'acc': 'Accuracy',
        'add': 'Add', 'delete': 'Delete', 'patch': 'patch', 'atbTit': 'Aspect table'
    }

    tmc_kwd = {
        0: 'Second', 1: 'Minute', 2: 'Hour', 3: 'Day', 4: 'Month', 5: 'Year', 6: 'Time counter', 7: 'Now', 8: 'Reset'
    }

    def __init__(self, conf):
        self.var = conf.get_act_var()
        self.set_act_var = conf.set_act_var

        self.tkw = {}
        self.mkw = {}
        self.fkw = {}
        self.ckw = {}
        self.w_day = {}
        self.month = {}
        self.acf_name = {}
        self.dbs_kwd = {}
        self.sex_kwd = {}
        self.hss_kwd = {}
        self.apg_kwd = {}
        self.apg_head = {}
        self.ase_kwd = {}
        self.pct_kwd = {}
        self.pce_kwd = {}
        self.avw_kwd = {}
        self.tmc_kwd = {}

        self.sam_act = {
            'tkw': self.tkw, 'mkw': self.mkw, 'fkw': self.fkw, 'ckw': self.ckw, 'w_day': self.w_day,
            'month': self.month, 'acf_name': self.acf_name, 'dbs_kwd': self.dbs_kwd, 'sex_kwd': self.sex_kwd,
            'hss_kwd': self.hss_kwd, 'apg_kwd': self.apg_kwd, 'apg_head': self.apg_head, 'ase_kwd': self.ase_kwd,
            'pct_kwd': self.pct_kwd, 'pce_kwd': self.pce_kwd, 'avw_kwd': self.avw_kwd, 'tmc_kwd': self.tmc_kwd
        }
        self.sam_pas = {
            'tkw': LocalKeywords.tkw, 'mkw': LocalKeywords.mkw, 'fkw': LocalKeywords.fkw, 'ckw': LocalKeywords.ckw,
            'w_day': LocalKeywords.w_day, 'month': LocalKeywords.month, 'acf_name': LocalKeywords.acf_name,
            'dbs_kwd': LocalKeywords.dbs_kwd, 'sex_kwd': LocalKeywords.sex_kwd, 'hss_kwd': LocalKeywords.hss_kwd,
            'apg_kwd': LocalKeywords.apg_kwd, 'apg_head': LocalKeywords.apg_head, 'ase_kwd': LocalKeywords.ase_kwd,
            'pct_kwd': LocalKeywords.pct_kwd, 'pce_kwd': LocalKeywords.pce_kwd, 'avw_kwd': LocalKeywords.avw_kwd,
            'tmc_kwd': LocalKeywords.tmc_kwd
        }

        self.reload(self.var[25])

    def reload(self, lang=''):
        cnt = 0
        try:
            with open('Local/%s.json' % lang) as fp:
                src = json.load(fp)
                fp.close()
            for i in range(1, len(src), 2):
                key = src[i-1]
                dec = dict(json.loads(src[i]))
                for j in dec:
                    self.sam_act[key][j] = dec[j]
                    cnt += 1
                self.set_act_var(25, lang)
        except BaseException as error:
            if cnt == 1:
                ut.error_log(error)

        if cnt != 313:
            self.set_act_var(25, 'English')
            for i in self.sam_pas:
                for j in self.sam_pas[i]:
                    self.sam_act[i][j] = self.sam_pas[i][j]
            self.dump()
        self.set_act_var(7, self.ckw['defName'])

    def dump(self):
        enc = []
        for i in self.sam_act:
            buf = list(self.sam_act[i].items())
            enc += [i, json.dumps(buf)]

        with open('Local/%s.json' % self.var[25], 'w') as fp:
            json.dump(enc, fp, separators=(',\n', ': '))
            fp.close()

    def get_sample_tkw(self): return self.tkw
    def get_sample_mkw(self): return self.mkw
    def get_sample_fkw(self): return self.fkw

    def get_month(self): return self.month
    def get_week_day(self): return self.w_day
    def get_sample_cell(self): return self.ckw
    def get_acf_name(self): return self.acf_name

    def get_sample_dbs(self): return self.dbs_kwd
    def get_sample_sex(self): return self.sex_kwd
    def get_sample_hss(self): return self.hss_kwd

    def get_sample_apg(self): return self.apg_kwd
    def get_hd_kwd_apg(self): return self.apg_head
    def get_sample_ase(self): return self.ase_kwd

    def get_sample_pct(self): return self.pct_kwd
    def get_sample_pce(self): return self.pce_kwd

    def get_sample_avw(self): return self.avw_kwd
    def get_sample_tmc(self): return self.tmc_kwd

# -------------------------------------------------------------------------------------------------------------------- #
