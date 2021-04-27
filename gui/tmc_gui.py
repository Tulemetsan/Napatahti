# -------------------------------------------------------------------------------------------------------------------- #

import datetime as tm
import tkinter as tk
import tkinter.ttk as ttk
import core.utilities as ut

# @formatter:off


class TimeCountGui:
    _x, _y = 0, 0
    _k = {0: 1, 1: 60, 2: 3600, 3: 86400}
    flg = 0
    stp_bt, bck_bt, nxt_bt = None, None, None
    app = None

    def __init__(self, abo, conf, kwd, cont_render):
        self.res_dt = {}
        self.data = abo.get_bs_data()

        self.var = conf.get_act_var()
        self.geo = conf.get_chd_geo(6)
        self.font = conf.get_src_font()

        self.set_app_chd = conf.set_app_chd
        self.set_ord_list = conf.set_ord_list
        self.set_chd_geo = conf.set_chd_geo
        self.set_act_var = conf.set_act_var
        self.set_wch_dbs = conf.set_wch_dbs

        self.kwd = kwd
        self.stp_var = {
            0: tk.StringVar(), 1: tk.StringVar(), 2: tk.StringVar(),
            3: tk.StringVar(), 4: tk.StringVar(), 5: tk.StringVar()
        }

        for i in self.stp_var:
            self.stp_var[i].trace_add('write', lambda *args: self.validate())

        self.cont_render = cont_render
        self.spb_vf = ut.factory_valid(1, 0, 100)

    def child_app(self):
        self.app = tk.Toplevel()
        self.set_app_chd(6, self.app)
        self.app.resizable(width=False, height=False)
        self.app.geometry('+%d+%d' % (self.geo['x'], self.geo['y']))
        self.app.title(self.kwd[6])
        self.app.focus_set()

        self.flg = 0
        self.set_act_var(10, 1)
        self.set_reset()

        stp_lb = {}
        stp_sb = {}
        self.stp_bt = {0: {}, 1: {}}

        fnt = self.font['AppCns']

        ttk.Style().configure('tmc.TButton', font=fnt)

        self.bck_bt = ttk.Button(
            self.app, text='<<<', width=7, style='tmc.TButton', command=lambda: self.step_apply(-1))
        mm1_bt = ttk.Button(
            self.app, text='M1', width=3, style='tmc.TButton', command=lambda: self.set_step_fr_memory(1))
        self.nxt_bt = ttk.Button(self.app, text='>>>', width=7, style='tmc.TButton', command=lambda: self.step_apply(1))

        for i in self.stp_var:
            self.stp_var[i].set(1)
            stp_lb[i] = tk.Label(self.app, text=self.kwd[i], font=fnt, justify=tk.CENTER)
            stp_sb[i] = tk.Spinbox(
                self.app, from_=0, to=100, textvariable=self.stp_var[i], width=3, font=fnt, justify=tk.CENTER)
            self.stp_bt[0][i] = ttk.Button(self.app, text='<', width=3, style='tmc.TButton')
            self.stp_bt[1][i] = ttk.Button(self.app, text='>', width=3, style='tmc.TButton')
        self.flg = 1

        now_bt = ttk.Button(self.app, text=self.kwd[7], width=7, style='tmc.TButton', command=self.now_apply)
        mm0_bt = ttk.Button(
            self.app, text='M0', width=3, style='tmc.TButton', command=lambda: self.set_step_fr_memory(0))
        res_bt = ttk.Button(self.app, text=self.kwd[8], width=7, style='tmc.TButton', command=self.get_reset)

        self.stp_bt[0][0].configure(command=lambda: self.step_apply(-1, 0))
        self.stp_bt[1][0].configure(command=lambda: self.step_apply(1, 0))
        self.stp_bt[0][1].configure(command=lambda: self.step_apply(-1, 1))
        self.stp_bt[1][1].configure(command=lambda: self.step_apply(1, 1))
        self.stp_bt[0][2].configure(command=lambda: self.step_apply(-1, 2))
        self.stp_bt[1][2].configure(command=lambda: self.step_apply(1, 2))
        self.stp_bt[0][3].configure(command=lambda: self.step_apply(-1, 3))
        self.stp_bt[1][3].configure(command=lambda: self.step_apply(1, 3))
        self.stp_bt[0][4].configure(command=lambda: self.step_apply(-1, 4))
        self.stp_bt[1][4].configure(command=lambda: self.step_apply(1, 4))
        self.stp_bt[0][5].configure(command=lambda: self.step_apply(-1, 5))
        self.stp_bt[1][5].configure(command=lambda: self.step_apply(1, 5))

        px = 10
        py = 10

        self.bck_bt.grid(row=0, column=0, padx=px, pady=py, sticky=tk.W)
        mm1_bt.grid(row=0, column=1, padx=px, pady=py, sticky=tk.E+tk.W)
        self.nxt_bt.grid(row=0, column=2, columnspan=2, padx=px, pady=py, sticky=tk.E)

        for i in range(6):
            stp_lb[i].grid(row=i+1, column=0, padx=px, sticky=tk.E)
            stp_sb[i].grid(row=i+1, column=1, padx=px, pady=1, sticky=tk.N+tk.S+tk.E+tk.W)
            self.stp_bt[0][i].grid(row=i+1, column=2, sticky=tk.E)
            self.stp_bt[1][i].grid(row=i+1, column=3, sticky=tk.W)

        now_bt.grid(row=7, column=0, padx=px, pady=py, sticky=tk.W)
        mm0_bt.grid(row=7, column=1, padx=px, pady=py, sticky=tk.E+tk.W)
        res_bt.grid(row=7, column=2, columnspan=2, padx=px, pady=py, sticky=tk.E)

        self.app.bind('<Configure>', self.on_config)
        now_bt.bind('<Destroy>', lambda *args: self.on_destroy())
        self.app.bind('<FocusIn>', lambda *args: self.set_ord_list(6, 1))

    def on_config(self, event):
        if 'toplevel' in str(event.widget).split('.!')[-1]:
            self._x, self._y = event.x, event.y

    def on_destroy(self):
        self.set_app_chd(6, None)
        self.set_ord_list(6, 0)
        self.set_chd_geo(6, x=self._x, y=self._y)

    def step_apply(self, rev, ind=None):
        if ind is None or ind == 4:
            mm = self.data[1]['date'][1] if rev == 1 else self.data[1]['date'][1] - 1
            if mm == 0:
                mm = 12
            self._k[4] = 86400 * ut.get_max_day(self.data[1]['date'][0], mm)
        if ind is None or ind == 5:
            self._k[5] = 365
            mm = self.data[1]['date'][1]
            y1 = self.data[1]['date'][0]
            y2 = self.data[1]['date'][0] + rev
            if ut.get_max_day(y1, 2) == 29:
                if (rev == 1 and mm < 3) or (rev == -1 and mm > 2):
                    self._k[5] = 366
            elif ut.get_max_day(y2, 2) == 29:
                if (rev == 1 and mm > 2) or (rev == -1 and mm < 3):
                    self._k[5] = 366
            self._k[5] *= 86400

        dd = 0
        seq = self.stp_var if ind is None else [ind]
        for i in seq:
            dd += rev * self._k[i] * int(self.stp_var[i].get())

        if dd:
            ztm = tm.datetime(
                self.data[1]['date'][0], self.data[1]['date'][1], self.data[1]['date'][2],
                self.data[1]['time'][0], self.data[1]['time'][1], self.data[1]['time'][2]
            )
            ntm = tm.datetime.fromtimestamp(ztm.timestamp() + dd)
            self.data[1]['date'][0] = ntm.year
            self.data[1]['date'][1] = ntm.month
            self.data[1]['date'][2] = ntm.day
            self.data[1]['time'][0] = ntm.hour
            self.data[1]['time'][1] = ntm.minute
            self.data[1]['time'][2] = ntm.second
            self.data[2] = {}
            self.set_wch_dbs(self.data[0])
            self.cont_render(31, 2015)

    def set_step_fr_memory(self, mode):
        for i in self.stp_var:
            self.stp_var[i].set(mode)

    def now_apply(self):
        now = tm.datetime.now()

        self.data[1]['name'] = self.var[7]
        self.data[1]['date'][0] = now.year
        self.data[1]['date'][1] = now.month
        self.data[1]['date'][2] = now.day
        self.data[1]['time'][0] = now.hour
        self.data[1]['time'][1] = now.minute
        self.data[1]['time'][2] = now.second
        self.data[2] = {}
        self.set_wch_dbs(self.data[0])
        self.cont_render(31, 2015)

    def get_reset(self):
        self.data[1]['date'] = self.res_dt[0].copy()
        self.data[1]['time'] = self.res_dt[1].copy()
        self.data[1]['name'] = self.res_dt[2]
        self.data[2] = self.res_dt[3].copy()
        self.set_wch_dbs(self.data[0])
        self.cont_render(31, 2015)

    def set_reset(self):
        if self.var[10]:
            self.res_dt[0] = self.data[1]['date'].copy()
            self.res_dt[1] = self.data[1]['time'].copy()
            self.res_dt[2] = self.data[1]['name']
            self.res_dt[3] = self.data[2].copy()
            self.set_act_var(10, 0)

    def validate(self):
        if self.flg:
            cnt = 0
            for i in self.stp_var:
                if not self.spb_vf(self.stp_var[i].get()):
                    self.stp_bt[0][i].configure(state=tk.DISABLED)
                    self.stp_bt[1][i].configure(state=tk.DISABLED)
                    self.bck_bt.configure(state=tk.DISABLED)
                    self.nxt_bt.configure(state=tk.DISABLED)
                else:
                    self.stp_bt[0][i].configure(state=tk.NORMAL)
                    self.stp_bt[1][i].configure(state=tk.NORMAL)
                    cnt += 1
            if cnt == 6:
                self.bck_bt.configure(state=tk.NORMAL)
                self.nxt_bt.configure(state=tk.NORMAL)

# -------------------------------------------------------------------------------------------------------------------- #
