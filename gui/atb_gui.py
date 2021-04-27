# -------------------------------------------------------------------------------------------------------------------- #

import tkinter as tk
import tkinter.ttk as ttk
from .src_class import GuiSmartTable

# @formatter:off


class AspTabGui(GuiSmartTable):
    _x, _y = 0, 0
    _cn = 0
    sam_pl = None

    def __init__(self, atb, apg, abo, conf, loc, data, cont_render):
        self.data = data
        self.kwd = loc.get_sample_tkw()
        self.akw = loc.get_sample_avw()

        self.var = conf.get_act_var()
        self.geo = conf.get_chd_geo(5)
        self.dim = conf.get_atb_dim()
        self.col = conf.get_atb_col()
        self.font = conf.get_src_font()

        self.set_app_chd = conf.set_app_chd
        self.set_ord_list = conf.set_ord_list
        self.set_chd_geo = conf.set_chd_geo
        self.set_act_var = conf.set_act_var
        self.set_wch_dbs = conf.set_wch_dbs

        self.tab_4pl = atb.get_tab_4pl()
        self.asp_sym = apg.get_asp_prop(mode=1)
        self.asp_col = apg.get_asp_prop(mode=2)
        self.asp_ftp = apg.get_asp_prop(mode=3)

        self.base_lt = abo.get_base_pl(0)
        self.base_st = abo.get_base_pl(1)
        self.cat_pl = abo.get_cat_pl()

        self.get_pl_name = abo.get_pl_name
        self.apply_cfg = self.tab_render
        self.cont_render = cont_render

        self.asp_view = AspectViewer(
            atb, apg, abo, conf, self.akw, self.del_patch, self.tab_render, cont_render)

    def child_app(self):
        GuiSmartTable.child_app(self)

        self.update(1)
        self.set_app_chd(5, self.app)
        self.asp_view.configure(parent=self.app)
        self.app.title(self.akw['atbTit'])

        cw = self.dim['CellWid']
        ch = self.dim['CellHgt']

        self.app.geometry('%dx%d+%d+%d' % (self.geo['w'], self.geo['h'], self.geo['x'], self.geo['y']))
        self.app.minsize(5*cw + 21, 3*ch + 21)
        self.app.maxsize(self.var[18]*cw + 21, self.var[18]*ch + 21)
        self.app.focus_set()

        self.wdg_set_pos(3)
        self.tab_render()

        self.app.bind('<Configure>', self.on_config)
        self.app.bind('<FocusIn>', lambda *args: self.set_ord_list(5, 1))
        self.m_frame.bind('<Destroy>', lambda *args: self.on_destroy())
        self.cnv.bind('<Double-Button-1>', self.on_click)
        self.cnv.bind('<Button-3>', self.on_click)
        self.cnv.bind('<MouseWheel>', self.on_cnv_mouse_wheel)
        self.cnv.bind('<Motion>', lambda event: self.on_motion_src(event, self.col['EntMrk']))
        self.cnv.bind('<Leave>', lambda *args: self.cnv.delete('mark'))

    def cnv_scr_upd(self): self.cnv_scr_upd_src(self.var[18], self.var[18], 0)
    def tab_upd(self, mode=0): self.tab_upd_src(self.var[18], self.var[18], 0, mode)

    def on_config(self, event):
        cw = self.dim['CellWid']
        ch = self.dim['CellHgt']

        if self.app.wm_state() == 'zoomed':
            self.app.wm_state('normal')
            self.app.geometry('%dx%d' % (17*cw + 21, 17*ch + 21))
            self._sx, self._sy = 0, 0
            self._nc, self._nr = 0, 0
            self.tab_render()
        else:
            widget = str(event.widget).split('.!')[-1]
            if 'toplevel' in widget:
                self._x, self._y = event.x, event.y
            elif 'frame' in widget:
                self._w = event.width
                self._h = event.height
                nw = int((self._w - 20)/cw)
                nh = int((self._h - ch - 20)/ch)
                nw = nw*cw + 20
                nh = (nh + 1)*ch + 20
                self.app.geometry('%dx%d' % (nw, nh))

                self.wdg_set_pos(28)
                self.cnv_scr_upd()
                self.tab_upd()

    def on_destroy(self):
        self.set_app_chd(5, None)
        self.set_ord_list(5, 0)
        self.set_chd_geo(5, w=self._w, h=self._h, x=self._x, y=self._y)
        self._sx, self._sy = 0, 0
        self._nc, self._nr = 0, 0

    def on_cnv_mouse_wheel(self, event):
        GuiSmartTable.on_cnv_mouse_wheel(self, event)
        self.on_motion_src(event, self.col['EntMrk'])

    def wdg_set_pos(self, mask):
        if mask & 1:
            self.m_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        if mask & 2:
            self.cnv.place(
                x=0, y=0, width=self.var[18]*self.dim['CellWid'] + 1, height=self.var[18]*self.dim['CellHgt'] + 1)
        if mask & 4:
            self.cnv_scr_ver.place(x=self._w - 20, y=0, width=20, height=self._h - 20)
        if mask & 8:
            self.cnv_scr_hor.place(x=0, y=self._h - 20, width=self._w - 20, height=20)
        if mask & 16:
            self.cnv_scr_cap.place(x=self._w - 20, y=self._h - 20, width=20, height=20)

    def update(self, mask=3):
        if mask & 1:
            self.set_act_var(18, len(self.cat_pl) + 1)
            self._cn = self.var[18]
            buf = self.base_st ^ set(self.cat_pl.keys())
            buf = self.base_lt + sorted(list(buf))
            self.sam_pl = dict(zip(range(self.var[18] - 1), buf))
        if mask & 2:
            self.app.maxsize(self.var[18]*self.dim['CellWid'] + 21, self.var[18]*self.dim['CellHgt'] + 21)
            self.wdg_set_pos(2)
            self.tab_upd(1)
            self.cnv_scr_upd()

    def tab_render(self):
        col = self.col
        fnt = {
            0: self.font['AppBsc'], 1: self.font['AppSym'],
            2: [self.font['AppBsc'][0], int(0.75*self.font['AppBsc'][1])]
        }
        cw = self.dim['CellWid']
        ch = self.dim['CellHgt']
        px = cw/2
        py = ch/2

        self.cnv.delete('all')

        for i in range(self.var[18]):
            for j in range(self.var[18]):
                sx, sy = self._sx, self._sy
                key, asp = 0, 0
                flag = 0
                cont = ''
                font = fnt[0]
                col1 = col['FrgCol']
                col2 = col['BkgCol']

                if i != j > 0 and i > 0:
                    p1 = self.sam_pl[i-1]
                    p2 = self.sam_pl[j-1]
                    key = (p1, p2) if (p1, p2) in self.tab_4pl else (p2, p1)
                    asp = self.tab_4pl[key][1]

                if i == j == 0:
                    cont = 'RES'
                    col1 = col['NonAsp']
                    if self.data[2]:
                        col1 = col['ResFrg']
                        col2 = col['ResBkg']
                    flag = 2
                    sx, sy = 0, 0
                elif i == 0 and i != j and j > sx:
                    cont = self.cat_pl[self.sam_pl[j-1]]
                    font = fnt[1]
                    flag = 2
                    sy = 0
                elif j == 0 and i != j and i > sy:
                    cont = self.cat_pl[self.sam_pl[i-1]]
                    font = fnt[1]
                    flag = 2
                    sx = 0
                elif i == j and i > sy and j > sx:
                    col2 = col['EmpCell']
                    flag = 1
                elif j > i > sy and j > sx:
                    cont = round(self.tab_4pl[key][0], 2)
                    col1 = self.asp_col[asp] if asp != -1 else col['NonAsp']
                    if self.data[2] and key in self.data[2]:
                        col2 = col['PchCell']
                    flag = 2
                elif i > j > sx and i > sy:
                    cont = self.asp_sym[asp] if asp != -1 else ''
                    font = fnt[1] if self.asp_ftp[asp] else fnt[2]
                    col1 = self.asp_col[asp]
                    if self.data[2] and key in self.data[2]:
                        col2 = col['PchCell']
                    flag = 2

                x = cw * (j - sx)
                y = ch * (i - sy)
                if flag:
                    self.cnv.create_rectangle(x, y, x + cw, y + ch, fill=col2, outline=col['CellFrm'])
                if flag == 2:
                    self.cnv.create_text(x + px, y + py, text=cont, fill=col1, font=font)

    def on_click(self, event):
        self.on_click_src(event, 1, 1)
        key = None
        if 0 < self._ix != self._iy and self._iy > 0:
            p1 = self.sam_pl[self._ix-1]
            p2 = self.sam_pl[self._iy-1]
            key = (p1, p2) if (p1, p2) in self.tab_4pl else (p2, p1)
        if event.num == 1:
            if self._ix == self._iy == 0:
                if self.data[2]:
                    self.del_patch()
            elif 0 < self._ix != self._iy and self._iy > 0:
                self.asp_view.mb(key, event.x_root, event.y_root)
        else:
            pm = tk.Menu(self.app, tearoff=0)
            if key:
                title = '%s : %s' % (self.get_pl_name(key[0]), self.get_pl_name(key[1]))
                pm.add_command(label=title, state=tk.DISABLED)
                pm.add_separator()
                pm.add_command(
                    label=self.kwd['open'], command=lambda: self.asp_view.mb(key, event.x_root, event.y_root))
                if key in self.data[2]:
                    pm.add_command(label=self.kwd['delete'], command=lambda: self.del_patch(key))
            pm.tk_popup(event.x_root, event.y_root)

    def del_patch(self, key=None):
        if key is None:
            self.data[2].clear()
        else:
            del self.data[2][key]
        self.set_wch_dbs(self.data[0])
        self.cont_render(4, 936)
        self.tab_render()


class AspectViewer:
    _w, _h = 0, 0
    flag, mode = 0, 0
    acc_sym = {0: '▬', 1: '▲', -1: '▼'}
    key, sam = None, None
    parent = None
    app, sav_bt = None, None

    def __init__(self, atb, apg, abo, conf, kwd, d_func, p_rend, c_rend):
        self.kwd = kwd
        self.data = abo.get_bs_data()

        self.var = conf.get_act_var()
        self.font = conf.get_src_font()

        self.tab_4pl = atb.get_tab_4pl()
        self.asp_src = apg.get_asp_src()
        self.orb_4pl = apg.get_asp_orb()
        self.base_st = abo.get_base_pl()

        self.val_var = tk.StringVar()
        self.orb_var = {0: tk.StringVar(), 1: tk.StringVar()}
        self.asp_var = tk.StringVar()
        self.acc_var = tk.StringVar()

        self.get_pl_name = abo.get_pl_name
        self.d_func = d_func
        self.p_rend = p_rend
        self.c_rend = c_rend
        self.set_wch_dbs = conf.set_wch_dbs

    def mb(self, key, cx=None, cy=None):
        self.key = key
        self.flag = 1
        self.mode = 1 if key in self.data[2] else 0

        self.create_app()
        self._w = self.app.winfo_screenwidth()
        self._h = self.app.winfo_screenheight()
        if cx is None:
            cx = 0.5*self._w - 200
        if cy is None:
            cy = 0.5*self._h - 100
        self.app.geometry('+%d+%d' % (cx, cy))
        self.app.resizable(width=False, height=False)
        self.set_app_title()

        fnt = self.font['AppBsc']

        ttk.Style().configure('asv.TButton', font=fnt)
        self.app.option_add('*TCombobox*Listbox.font', fnt)

        self.sam = self.tab_4pl[key]
        self.val_var.set(round(self.sam[0], 2))
        if self.sam[1] != -1:
            asp_list = [round(self.sam[1], 2)]
            self.asp_var.set(asp_list[0])
            p1 = key[0] if key[0] in self.base_st else -4
            p2 = key[1] if key[1] in self.base_st else -4
            orb = max(self.orb_4pl[(self.sam[1], p1)], self.orb_4pl[(self.sam[1], p2)])
            self.orb_var[0].set('%sº' % round(self.sam[2], 2))
            self.orb_var[1].set('%s%%' % round(100*abs(self.sam[0] - self.sam[1])/orb))
            self.acc_var.set(self.acc_sym[self.sam[3]])
        else:
            asp_list = ['']
            buf = list(self.asp_src.values())
            buf.append(self.sam[0])
            buf.sort()
            k = len(buf)
            for i in range(k):
                if self.sam[0] == buf[i]:
                    if i == 0:
                        asp_list.append(buf[i+1])
                    elif i == k - 1:
                        asp_list.append(buf[i-1])
                    else:
                        asp_list.append(buf[i-1])
                        asp_list.append(buf[i+1])
            self.asp_var.set('')
            self.orb_var[0].set('')
            self.orb_var[1].set('')
            self.acc_var.set('')

        val_lb = tk.Label(self.app, text=self.kwd['val'], font=fnt)
        val_en = ttk.Entry(self.app, textvariable=self.val_var, width=7, font=fnt, state=tk.DISABLED, justify=tk.CENTER)
        orb_en = {
            0: ttk.Entry(
                self.app, textvariable=self.orb_var[0], width=7, font=fnt, state=tk.DISABLED, justify=tk.CENTER),
            1: ttk.Entry(
                self.app, textvariable=self.orb_var[1], width=7, font=fnt, state=tk.DISABLED, justify=tk.CENTER)
        }
        self.sav_bt = ttk.Button(
            self.app, text=self.kwd['add'], width=9, style='asv.TButton', state=tk.DISABLED, command=self.add_patch)

        asp_lb = tk.Label(self.app, text=self.kwd['asp'], font=fnt)
        asp_cb = ttk.Combobox(
            self.app, values=asp_list, textvariable=self.asp_var, font=fnt, width=5, state='readonly', justify=tk.CENTER
        )
        acc_lb = tk.Label(self.app, text=self.kwd['acc'], font=fnt)
        acc_en = ttk.Entry(self.app, textvariable=self.acc_var, width=7, font=fnt, state=tk.DISABLED, justify=tk.CENTER)
        state = tk.NORMAL if self.mode else tk.DISABLED
        del_bt = ttk.Button(
            self.app, text=self.kwd['delete'], width=9, style='asv.TButton', state=state, command=self.del_patch)

        px, py = 10, 10
        ens = tk.E+tk.N+tk.S

        val_lb.grid(row=0, column=0, padx=px, pady=py, sticky=tk.E)
        val_en.grid(row=0, column=1, pady=py, sticky=ens)
        orb_en[0].grid(row=0, column=2, padx=px, pady=py, sticky=ens)
        orb_en[1].grid(row=0, column=3, pady=py, sticky=ens)
        self.sav_bt.grid(row=0, column=4, padx=px, pady=py, sticky=tk.E)
        asp_lb.grid(row=1, column=0, padx=px, sticky=tk.W)
        asp_cb.grid(row=1, column=1, sticky=ens)
        acc_lb.grid(row=1, column=2, padx=px, sticky=tk.E)
        acc_en.grid(row=1, column=3, sticky=ens)
        del_bt.grid(row=1, column=4, padx=px, sticky=tk.E)

        self.app.bind('<Escape>', lambda *args: self.app.destroy())
        self.app.bind('<Configure>', self.on_config)
        asp_cb.bind('<<ComboboxSelected>>', lambda *args: self.asp_select())

    def configure(self, **kwargs):
        if 'parent' in kwargs:
            self.parent = kwargs['parent']

    def create_app(self):
        self.app = tk.Toplevel()
        self.app.transient(self.parent)
        self.app.grab_set()
        self.app.focus_set()

    def on_config(self, event):
        if self.flag:
            widget = str(event.widget).split('.!')[-1]
            if 'toplevel' in widget:
                x = self._w - event.width - 12 if event.x + event.width > self._w - 2 else event.x
                y = self._h - event.height - 85 if event.y + event.height + 10 > self._h - 75 else event.y
                self.app.geometry('%dx%d+%d+%d' % (event.width, event.height + 10, x, y))
                self.flag = 0

    def set_app_title(self):
        title = '%s < %s : %s >' % (self.kwd['key'], self.get_pl_name(self.key[0]), self.get_pl_name(self.key[1]))
        if self.mode:
            title += ' < %s >' % self.kwd['patch']
        self.app.title(title)

    def asp_select(self):
        buf = self.asp_var.get()
        if buf == '':
            self.orb_var[0].set('')
            self.orb_var[1].set('')
            self.acc_var.set('')
            self.sav_bt.configure(state=tk.DISABLED)
        else:
            asp = float(self.asp_var.get())
            p1 = self.key[0] if self.key[0] in self.base_st else -4
            p2 = self.key[1] if self.key[1] in self.base_st else -4
            orb = max(self.orb_4pl[(asp, p1)], self.orb_4pl[(asp, p2)])
            buf = abs(self.sam[0] - asp)
            self.orb_var[0].set('%sº' % round(buf, 2))
            self.orb_var[1].set('%s%%' % round(100*buf/orb))
            if self.sam[1] == -1:
                acc = self.acc_sym[-1]
                self.sav_bt.configure(state=tk.NORMAL)
            else:
                acc = self.acc_sym[self.sam[3]]
            self.acc_var.set(acc)

    def add_patch(self):
        asp = float(self.asp_var.get())
        self.data[2][self.key] = [self.sam[0], asp, abs(asp - self.sam[0]), -1, self.sam[4]]
        self.set_wch_dbs(self.data[0])
        self.c_rend(4, 936)
        self.p_rend()
        self.app.destroy()

    def del_patch(self):
        self.d_func(self.key)
        self.app.destroy()

# -------------------------------------------------------------------------------------------------------------------- #
