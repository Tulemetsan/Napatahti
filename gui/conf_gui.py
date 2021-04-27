# -------------------------------------------------------------------------------------------------------------------- #

import tkinter as tk
import tkinter.ttk as ttk
import core.utilities as ut
from tkinter.font import families
from tkinter.colorchooser import askcolor

# @formatter:off


class ConfigGui:
    _x, _y = 0, 0
    _m, _s = 0, 0
    _c, _f = None, None
    app = None
    prt_tr, prt_lb = None, None
    dim_sc, dim_cb, dim_lb = None, None, None
    col_bt, col_cb = None, None
    ffm_cb, fnt_sb, fnt_cb = None, None, None
    plc_cb = None
    sav_bt = None

    def __init__(self, conf, loc, cont_render):
        self.res = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}}

        self.tkw = loc.get_sample_tkw()
        self.mkw = loc.get_sample_mkw()

        self.var = conf.get_act_var()
        self.geo = conf.get_chd_geo(7)

        self.set_app_chd = conf.set_app_chd
        self.set_ord_list = conf.set_ord_list
        self.set_chd_geo = conf.set_chd_geo
        self.set_save_flag = conf.set_save_flag

        self.dim = {
            1: conf.get_c_dim(2), 2: conf.get_c_dim(10), 3: conf.get_c_dim(9), 4: conf.get_c_dim(8),
            5: conf.get_c_dim(1), 6: conf.get_c_dim(3), 7: conf.get_c_dim(4), 8: conf.get_c_dim(7),
            9: conf.get_c_dim(6), 10: conf.get_c_dim(5), 11: conf.get_c_dim(0)
        }
        self.col = {
            0: conf.get_c_col(0), 5: conf.get_c_col(1), 6: conf.get_c_col(3), 7: conf.get_c_col(4),
            8: conf.get_c_col(0), 9: conf.get_c_col(6), 10: conf.get_c_col(5), 11: conf.get_c_col(0),
            12: conf.get_apg_col(), 13: conf.get_atb_col()
        }
        self.exc = {12: conf.get_ase_col()}
        self.fnt = conf.get_src_font()
        self.plc = conf.get_cur_plc()

        self.msk = {
            0: 4063, 1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 64, 7: 128, 8: 256, 9: 512, 10: 1024,
            11: 4096, 12: 4096, 13: 4096
        }
        self.key = {
            0: 'genTit', 1: 'dtcTit', 2: 'edtTit', 3: 'recTit', 4: 'esdTit', 5: 'mapTit', 6: 'crdTit',
            7: 'stbTit', 8: 'acfTit', 9: 'astTit', 10: 'corTit', 11: 'genTit', 12: 'apgTit', 13: 'atbTit'
        }
        self.font_list = [i for i in families() if not i.startswith('@')]
        self.atlas = ut.SmartDictJson('./Atlas.json', 1)

        self.sel_var = {0: tk.StringVar(), 1: tk.StringVar(), 2: tk.StringVar(), 3: tk.StringVar(), 4: tk.StringVar()}
        self.dim_var = tk.IntVar()
        self.ffm_var = tk.StringVar()
        self.fsz_var = tk.IntVar()

        self.cont_render = cont_render

    def child_app(self, mode):
        self._m = mode
        self.app = tk.Toplevel()
        self.set_app_chd(7, self.app)
        self.app.focus_set()

        self.app.geometry('+%d+%d' % (self.geo['x'], self.geo['y']))
        self.app.resizable(width=False, height=False)
        self.app.title(self.tkw['set'])

        px, py = 10, 10
        ft = self.fnt['AppCns']
        fnt = {1: [ft[0], int(0.75*ft[1])], 2: [ft[0], int(1.084*ft[1])], 3: [ft[0], int(0.667*ft[1])]}

        ttk.Style().configure('cfg.TButton', font=ft)
        ttk.Style().configure('cfg.Treeview', font=ft)
        self.app.option_add('*TCombobox*Listbox.font', ft)

        crutch = tk.Frame(self.app, width=200, height=360)
        self.prt_tr = ttk.Treeview(crutch, show='tree', selectmode='browse', style='cfg.Treeview', height=16)
        self.prt_lb = tk.Label(self.app, width=42, font=ft, justify=tk.LEFT, anchor=tk.W)

        self.dim_sc = tk.Scale(
            self.app, variable=self.dim_var, length=250, resolution=1, font=fnt[3],
            orient=tk.HORIZONTAL, command=lambda *args: self.apply_set(0))
        self.dim_cb = ttk.Combobox(self.app, textvariable=self.sel_var[0], font=ft, width=9, state='readonly')
        self.dim_lb = tk.Label(self.app, width=27, font=ft, anchor=tk.W)

        self.col_bt = {
            0: tk.Button(self.app, text='       ▼', width=5, font=fnt[1], command=lambda: self.apply_set(3)),
            1: tk.Button(self.app, text='       ▼', width=5, font=fnt[1], command=lambda: self.apply_set(1))
        }
        self.col_cb = {
            0: ttk.Combobox(self.app, textvariable=self.sel_var[3], font=ft, width=9, state='readonly'),
            1: ttk.Combobox(self.app, textvariable=self.sel_var[1], font=ft, width=9, state='readonly')
        }

        self.ffm_cb = ttk.Combobox(
            self.app, values=self.font_list, textvariable=self.ffm_var, font=ft, width=18, state='readonly')
        self.fnt_sb = tk.Spinbox(
            self.app, from_=5, to=25, textvariable=self.fsz_var, command=lambda: self.apply_set(2),
            width=3, font=fnt[2], state='readonly', justify=tk.CENTER)
        self.fnt_cb = ttk.Combobox(self.app, textvariable=self.sel_var[2], font=ft, width=9, state='readonly')
        self.plc_cb = ttk.Combobox(
            self.app, values=self.atlas.keys(), textvariable=self.sel_var[4], font=ft, width=40, state='readonly')

        self.sav_bt = ttk.Button(
            self.app, text=self.tkw['save'], width=10, style='cfg.TButton', state=tk.DISABLED, command=self.save_var)
        res_bt = ttk.Button(
            self.app, text=self.tkw['reset'], width=10, style='cfg.TButton', command=lambda: self.reset_var())
        cnc_bt = ttk.Button(
            self.app, text=self.tkw['close'], width=10, style='cfg.TButton', command=lambda: self.app.destroy())

        crutch.grid(row=0, column=0, rowspan=6, padx=px, pady=py)
        self.prt_tr.place(x=1, y=1, width=200, height=360)
        self.prt_lb.grid(row=0, column=1, columnspan=2, padx=px, sticky=tk.W)

        self.dim_sc.grid(row=1, column=1, padx=px)
        self.dim_cb.grid(row=1, column=2, padx=px, sticky=tk.E)
        self.dim_lb.grid(row=1, column=1, padx=px)

        self.col_bt[0].grid(row=2, column=1, padx=px, sticky=tk.W)
        self.col_cb[0].grid(row=2, column=1, padx=px)
        self.col_bt[1].grid(row=2, column=1, padx=px, sticky=tk.E)
        self.col_cb[1].grid(row=2, column=2, padx=px, sticky=tk.E)

        self.ffm_cb.grid(row=3, column=1, padx=px, sticky=tk.W)
        self.fnt_sb.grid(row=3, column=1, padx=px, sticky=tk.E)
        self.fnt_cb.grid(row=3, column=2, padx=px, sticky=tk.E)

        self.plc_cb.grid(row=4, column=1, columnspan=2, padx=px, sticky=tk.E)

        self.sav_bt.grid(row=5, column=1, columnspan=2, padx=px, pady=py, sticky=tk.W+tk.S)
        res_bt.grid(row=5, column=1, columnspan=2, padx=px, pady=py, sticky=tk.S)
        cnc_bt.grid(row=5, column=1, columnspan=2, padx=px, pady=py, sticky=tk.E+tk.S)

        self.part_tr_set()
        self.set_wdg_cfg()
        self.set_ini_var()

        self.app.bind('<Configure>', self.on_config)
        self.app.bind('<FocusIn>', lambda *args: self.set_ord_list(7, 1))
        self.prt_tr.bind('<Button-1>', self.on_tree_click)
        self.dim_cb.bind('<Destroy>', lambda *args: self.on_destroy())
        self.dim_cb.bind('<<ComboboxSelected>>', lambda *args: self.cbx_select(0))
        self.col_cb[1].bind('<<ComboboxSelected>>', lambda *args: self.cbx_select(1))
        self.col_cb[0].bind('<<ComboboxSelected>>', lambda *args: self.cbx_select(3))
        self.fnt_cb.bind('<<ComboboxSelected>>', lambda *args: self.cbx_select(2))
        self.ffm_cb.bind('<<ComboboxSelected>>', lambda *args: self.apply_set(2))
        self.plc_cb.bind('<<ComboboxSelected>>', lambda *args: self.apply_set(4))

    def on_config(self, event):
        widget = str(event.widget).split('.!')[-1]
        if 'toplevel' in widget:
            self._x = event.x
            self._y = event.y

    def on_destroy(self):
        self.set_app_chd(7, None)
        self.set_ord_list(7, 0)
        self.set_chd_geo(7, x=self._x, y=self._y)
        if self._s:
            self.reset_var(0)

    def on_tree_click(self, event):
        itm = self.prt_tr.identify('item', event.x, event.y)
        tag = self.prt_tr.item(itm, 'tag')
        mod = int(tag[0]) if tag else -1

        if 0 <= mod != self._m:
            if self._s:
                self.reset_var(0)
            self._m = mod
            self.set_wdg_cfg()
            self.set_ini_var()

    def part_tr_set(self):
        p1 = self.prt_tr.insert('', 1, text=self.mkw['appCfg'], open=True)
        p2 = self.prt_tr.insert('', 2, text=self.mkw['mpcCfg'], open=True)
        for i in [11, 12, 13]:
            self.prt_tr.insert(p1, 'end', text=self.mkw[self.key[i]], tag='%d' % i)
        for i in self.key:
            if i in {11, 12, 13}:
                continue
            self.prt_tr.insert(p2, 'end', text=self.mkw[self.key[i]], tag='%d' % i)

        brk = 0
        for i in self.prt_tr.get_children():
            if brk:
                break
            for j in self.prt_tr.get_children(i):
                if int(self.prt_tr.item(j, 'tag')[0]) == self._m:
                    self.prt_tr.selection_set(j)
                    brk = 1
                    break

    def set_wdg_cfg(self):
        self._c, self._f = [], []

        if self._m == 0:
            self._c = ['CellBkg', 'CellFont']
            self._f = ['CellText', 'CellSym']
        elif self._m == 5:
            self._f = ['PnSym', 'SgSym', 'CsSym', 'AsMrk1', 'AsMrk2']
        elif self._m == 7:
            self._f = ['StbMrk']
        elif self._m == 8:
            self._c = ['AcfMrk']
        elif self._m == 11:
            self._c = ['ToolBkg', 'ToolFrg', 'FootBkg', 'FootFrg']
            self._f = ['AppBsc', 'AppSym', 'AppSpc', 'AppCns']

        des = self.mkw['appCfg'] if self._m > 10 else self.mkw['mpcCfg']
        des = '%s / %s / %s' % (self.tkw['set'], des, self.mkw[self.key[self._m]])

        self.prt_lb.configure(text=des)
        self.sav_bt.configure(state=tk.DISABLED)

        if self._m not in {0, 12, 13}:
            self.dim_sc.grid()
            self.dim_cb.grid()
            self.dim_lb.grid_remove()
            self.dim_cb.configure(values=list(self.dim[self._m].keys()))
        else:
            self.dim_sc.grid_remove()
            self.dim_cb.grid_remove()
            self.dim_lb.grid()

        if self._m not in {1, 2, 3, 4}:
            self.col_bt[1].grid()
            self.col_cb[1].grid()
            if self._c:
                self.col_cb[1].configure(values=self._c)
            else:
                self.col_cb[1].configure(values=list(self.col[self._m].keys()))
            if self._m == 12:
                self.col_bt[0].grid()
                self.col_cb[0].grid()
                self.col_cb[0].configure(values=list(self.exc[self._m].keys()))
            else:
                self.col_bt[0].grid_remove()
                self.col_cb[0].grid_remove()
        else:
            self.col_bt[1].grid_remove()
            self.col_cb[1].grid_remove()
            self.col_bt[0].grid_remove()
            self.col_cb[0].grid_remove()

        if self._f:
            self.ffm_cb.grid()
            self.fnt_sb.grid()
            self.fnt_cb.grid()
            self.fnt_cb.configure(values=self._f)
        else:
            self.ffm_cb.grid_remove()
            self.fnt_sb.grid_remove()
            self.fnt_cb.grid_remove()

        if self._m == 11:
            self.plc_cb.grid()
        else:
            self.plc_cb.grid_remove()

    def set_scl_rng(self, sel):
        rng = []

        if self._m == 1:
            rng = [0, 100, 10]
        elif self._m == 2:
            rng = [0, 50, 5] if sel == 'PadY' else [0, 100, 10]
        elif self._m == 3:
            if sel == 'Count':
                rng = [1, 10, 1]
            elif sel == 'Step':
                rng = [10, 40, 5]
            else:
                rng = [0, 50, 5]
        elif self._m == 4:
            if sel in {'PadX', 'PadY'}:
                rng = [0, 50, 5]
            elif sel == 'Step':
                rng = [10, 40, 5]
            else:
                rng = [0, 300, 30]
        elif self._m == 5:
            if sel in {'BkgOval', 'SgRad'}:
                rng = [300, 600, 30]
            elif sel in {'CsLineExt', 'CsSymExt'}:
                rng = [0, 500, 50]
            elif sel in {'PnMrkRad', 'BtwPnSpc'}:
                rng = [1, 10, 1]
            elif sel == 'CsSymRot':
                rng = [0, 10, 1]
            elif sel == 'PnCirRad':
                rng = [200, 600, 40]
            elif sel == 'InsOval':
                rng = [170, 500, 40]
            elif sel == 'SgWid':
                rng = [10, 150, 15]
            elif sel == 'AsUniRad':
                rng = [10, 100, 10]
            else:
                rng = [0, 30, 3]
        elif self._m == 6:
            if sel in {'PnCrdPx', 'KdMrkPx', 'StarPx'}:
                rng = [50, 350, 30]
            elif sel == 'Step':
                rng = [10, 40, 5]
            elif sel == 'StarDy':
                rng = [-10, 10, 2]
            else:
                rng = [0, 50, 5]
        elif self._m == 7:
            if sel == 'PadX':
                rng = [0, 50, 5]
            elif sel == 'StLineDy':
                rng = [0, 10, 1]
            elif sel == 'StatMul':
                rng = [5, 15, 1]
            elif sel == 'AshMul':
                rng = [10, 50, 5]
            else:
                rng = [1, 10, 1]
        elif self._m == 8:
            if sel == 'SnsZnScl':
                rng = [1, 10, 1]
            elif sel == 'Step':
                rng = [10, 40, 5]
            elif sel == 'ZeroPnt':
                rng = [0, 250, 25]
            else:
                rng = [0, 50, 5]
        elif self._m == 9:
            if sel == 'Step':
                rng = [10, 40, 5]
            else:
                rng = [0, 50, 5]
        elif self._m == 10:
            if sel in {'PxCos', 'PxHor'}:
                rng = [0, 500, 50]
            elif sel == 'Step':
                rng = [10, 40, 5]
            elif sel == 'TitleDx':
                rng = [-25, 25, 5]
            else:
                rng = [0, 100, 10]
        elif self._m == 11:
            rng = [0, 150, 15]

        self.dim_sc.configure(from_=rng[0], to=rng[1], tickinterval=rng[2])

    def set_ini_var(self):
        self._s = 0
        for i in self.res:
            self.res[i].clear()

        if self._m not in {0, 12, 13}:
            ind = list(self.dim[self._m].keys())[0]
            self.res[0] = self.dim[self._m].copy()
            self.set_scl_rng(ind)
            self.sel_var[0].set(ind)
            self.dim_var.set(self.dim[self._m][ind])

        if self._m not in {1, 2, 3, 4}:
            ext = 0
            if self._c:
                ind = self._c[0]
                self.res[1] = {i: self.col[self._m][i] for i in self._c}
            else:
                ind = list(self.col[self._m].keys())[0]
                self.res[1] = self.col[self._m].copy()
                if self._m == 12:
                    ext = list(self.exc[self._m].keys())[0]
                    self.res[3] = self.exc[self._m].copy()
            self.sel_var[1].set(ind)
            self.col_bt[1].configure(bg=self.col[self._m][ind])
            if self._m == 12:
                self.sel_var[3].set(ext)
                self.col_bt[0].configure(bg=self.exc[self._m][ext])

        if self._f:
            ind = self._f[0]
            self.res[2] = {i: self.fnt[i].copy() for i in self._f}
            self.sel_var[2].set(ind)
            self.ffm_var.set(self.fnt[ind][0])
            self.fsz_var.set(self.fnt[ind][1])

        if self._m == 11:
            self.res[4] = self.plc.copy()
            self.sel_var[4].set(self.plc['place'])

    def cbx_select(self, swi):
        ind = self.sel_var[swi].get()

        if swi == 3:
            self.col_bt[0].configure(bg=self.exc[self._m][ind])
        elif swi == 2:
            self.ffm_var.set(self.fnt[ind][0])
            self.fsz_var.set(self.fnt[ind][1])
        elif swi == 1:
            self.col_bt[1].configure(bg=self.col[self._m][ind])
        else:
            self.set_scl_rng(ind)
            self.dim_var.set(self.dim[self._m][ind])

    def apply_set(self, swi):
        ind = self.sel_var[swi].get()
        rend = self.msk[self._m]
        calc = 0

        if swi == 4:
            plc = self.sel_var[4].get()
            self.plc['place'] = plc
            for i in self.atlas[plc]:
                if i != 'utc':
                    self.plc[i] = tuple(self.atlas[plc][i])
                else:
                    self.plc[i] = self.atlas[plc][i]
        elif swi == 3:
            ini = self.exc[self._m][ind]
            col = askcolor(parent=self.app, initialcolor=ini)[1]
            if col:
                self.exc[self._m][ind] = col.upper()
                self.col_bt[0].configure(bg=col)
        elif swi == 2:
            self.fnt[ind] = [self.ffm_var.get(), self.fsz_var.get()]
        elif swi == 1:
            ini = self.col[self._m][ind]
            col = askcolor(parent=self.app, initialcolor=ini)[1]
            if col:
                self.col[self._m][ind] = col.upper()
                if self._m == 6 and self.var[5] & 16:
                    rend |= 16
                self.col_bt[1].configure(bg=col)
        else:
            val = self.dim_var.get()
            if self.dim[self._m][ind] == val:
                return None

            self.dim[self._m][ind] = val
            if self._m == 5 and ind == 'BtwPnSpc':
                calc |= 16
            elif self._m == 6 and ind in {'PadY', 'Step'}:
                rend |= 128

        self._s = 1
        self.sav_bt.configure(state=tk.NORMAL)
        if swi != 3:
            self.cont_render(calc, rend)

    def save_var(self):
        if self._m in self.dim:
            self.res[0] = self.dim[self._m].copy()
        if self._m in self.col:
            if self._c:
                self.res[1] = {i: self.col[self._m][i] for i in self._c}
            else:
                self.res[1] = self.col[self._m].copy()
            if self._m == 12:
                self.res[3] = self.exc[self._m].copy()
        if self._f:
            self.res[2] = {i: self.fnt[i].copy() for i in self._f}
        if self._m == 11:
            self.res[4] = self.plc.copy()
        self._s = 0
        self.sav_bt.configure(state=tk.DISABLED)
        self.set_save_flag(1)

    def reset_var(self, swi=1):
        if self._m in self.dim:
            for i in self.res[0]:
                self.dim[self._m][i] = self.res[0][i]
            if swi:
                self.cbx_select(0)
        if self._m in self.col:
            for i in self.res[1]:
                self.col[self._m][i] = self.res[1][i]
            if self._m == 12:
                for i in self.res[3]:
                    self.exc[self._m][i] = self.res[3][i]
                if swi:
                    self.cbx_select(3)
            if swi:
                self.cbx_select(1)
        if self._f:
            for i in self.res[2]:
                self.fnt[i] = self.res[2][i].copy()
            if swi:
                self.cbx_select(2)
        if self._m == 11:
            self.sel_var[4].set(self.res[4]['place'])
            for i in self.res[4]:
                self.plc[i] = self.res[4][i]

        self._s = 0
        if self.var[23]:
            calc = 0
            rend = self.msk[self._m]
            self.sav_bt.configure(state=tk.DISABLED)
            if self._m == 6:
                rend |= 128
                if self.var[5] & 16:
                    rend |= 16
            elif self._m == 5:
                calc |= 16
            self.cont_render(calc, rend)

# -------------------------------------------------------------------------------------------------------------------- #
