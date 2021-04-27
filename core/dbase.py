# -------------------------------------------------------------------------------------------------------------------- #

import datetime
import json
import sqlite3 as sq
import core.utilities as ut

# @formatter:off


class DataBaseSQLite:

    def __init__(self, conf):
        self.pth = conf.get_app_pth()
        self.var = conf.get_act_var()
        self.cur_plc = conf.get_cur_plc()

        self.set_act_var = conf.set_act_var

        self.calc_free_ind()
        self.data_buf = self.get_record()

    def get_data_buf(self): return self.data_buf

    def set_data_buf(self, data):
        self.data_buf.clear()
        for i in data:
            self.data_buf[i] = data[i]

    def calc_free_ind(self):
        try:
            conn = sq.connect('%s/%s.db' % (self.pth[2], self.var[2]))
            cur = conn.cursor()
            cur.execute('SELECT * FROM clients')
            buf = cur.fetchall()
            val = buf[-1][0] + 1 if buf else 1
            self.set_act_var(6, val)
            conn.close()
        except sq.OperationalError as error:
            ut.error_log(error)
            self.create_dbase(self.var[2])
            self.calc_free_ind()

    def get_record(self, ind=None):
        if ind is None:
            now = datetime.datetime.now()
            data = {
                0: self.var[6],
                1: {
                    'name': self.var[7], 'place': self.cur_plc['place'],
                    'date': [now.year, now.month, now.day],
                    'time': [now.hour, now.minute, now.second, self.cur_plc['utc']],
                    'lat': self.cur_plc['lat'], 'lon': self.cur_plc['lon'], 'sysHouse': 'P', 'sex': 'E'
                },
                2: {}
            }
        elif ind:
            conn = sq.connect('%s/%s.db' % (self.pth[2], self.var[2]))
            cur = conn.cursor()
            cur.execute('SELECT * FROM clients WHERE ind=%d' % ind)
            data = cur.fetchone()
            data = {0: data[0], 1: json.loads(data[1]), 2: self.patch_loads(data[2])}
            conn.close()
        else:
            conn = sq.connect('%s/%s.db' % (self.pth[2], self.var[2]))
            cur = conn.cursor()
            cur.execute('SELECT * FROM clients')
            data = []
            for i in cur.fetchall():
                data.append({0: i[0], 1: json.loads(i[1]), 2: self.patch_loads(i[2])})
            val = data[-1][0] + 1 if data else 1
            self.set_act_var(6, val)
            conn.close()
        return data

    def get_cur_ind(self, data):
        conn = sq.connect('%s/%s.db' % (self.pth[2], self.var[2]))
        cur = conn.cursor()
        cur.execute('SELECT * FROM clients')
        ind = 0
        for i in cur.fetchall():
            if data[1] == json.loads(i[1]) and data[2] == self.patch_loads(i[2]):
                ind = i[0]
                break
        conn.close()
        return ind

    def upd_record(self, data):
        conn = sq.connect('%s/%s.db' % (self.pth[2], self.var[2]))
        cur = conn.cursor()
        if cur.execute('SELECT * FROM clients WHERE ind=%d' % data[0]).fetchone() is None:
            cur.execute(
                'INSERT INTO clients VALUES(?, ?, ?);', (data[0], json.dumps(data[1]), self.patch_dumps(data[2])))
            self.set_act_var(6, self.var[6] + 1)
        else:
            cur.execute(
                'UPDATE clients SET data = ?, atb = ? WHERE ind = ?;',
                (json.dumps(data[1]), self.patch_dumps(data[2]), data[0])
            )
        conn.commit()
        conn.close()

    def del_record(self, ind):
        conn = sq.connect('%s/%s.db' % (self.pth[2], self.var[2]))
        cur = conn.cursor()
        cur.execute('DELETE FROM clients WHERE ind=%d' % ind)
        conn.commit()
        conn.close()
        self.calc_free_ind()

    def create_dbase(self, name):
        conn = sq.connect('%s/%s.db' % (self.pth[2], name))
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS clients(
                ind INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                data BLOB NOT NULL,
                atb BLOB);
        ''')
        conn.commit()
        conn.close()

    def organize_db(self):
        conn = sq.connect('%s/%s.db' % (self.pth[2], self.var[2]))
        cur = conn.cursor()
        cur.execute('SELECT ind from clients')
        ind = cur.fetchall()
        for i in range(1, len(ind) + 1):
            if ind[i-1][0] != i:
                cur.execute('UPDATE clients SET ind=? WHERE ind=?', (i, ind[i-1][0]))
        conn.commit()
        conn.close()

    @staticmethod
    def patch_dumps(patch):
        res = {}
        for i in patch:
            res[json.dumps(i)] = patch[i]
        return json.dumps(res)

    @staticmethod
    def patch_loads(patch):
        res = {}
        dec = json.loads(patch)
        for i in dec:
            res[tuple(json.loads(i))] = dec[i]
        return res

# -------------------------------------------------------------------------------------------------------------------- #
