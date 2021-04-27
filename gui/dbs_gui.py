# -------------------------------------------------------------------------------------------------------------------- #

import os
import datetime
import tkinter as tk
import tkinter.ttk as ttk
import core.utilities as ut

# @formatter:off


class DataBaseGui:
    _w, _h, _x, _y = 0, 0, 0, 0
    buf = None
    app = None
    db_tree, db_tree_scr_cap = None, None
    db_tree_scr_ver, db_tree_scr_hor = None, None

    def __init__(self, dbs, conf, loc, ask_ent, db_edit, cont_render):
        self.tkw = loc.get_sample_tkw()
        self.skw = loc.get_sample_dbs()
        self.sex = loc.get_sample_sex()

        self.pth = conf.get_app_pth()
        self.var = conf.get_act_var()
        self.geo = conf.get_chd_geo(2)
        self.font = conf.get_src_font()

        self.set_app_chd = conf.set_app_chd
        self.set_ord_list = conf.set_ord_list
        self.set_chd_geo = conf.set_chd_geo
        self.set_act_var = conf.set_act_var
        self.set_wch_dbs = conf.set_wch_dbs

        self.data_buf = dbs.get_data_buf()

        self.create_db = dbs.create_dbase
        self.organize_db = dbs.organize_db
        self.set_data_buf = dbs.set_data_buf
        self.get_cur_ind = dbs.get_cur_ind
        self.get_rec_db = dbs.get_record
        self.upd_rec_db = dbs.upd_record
        self.del_rec_db = dbs.del_record

        self.db_list = [i.split('.')[0] for i in filter(lambda x: x.endswith('.db'), os.listdir(self.pth[2]))]
        self.db_var = tk.StringVar()

        self.ask_ent = ask_ent
        self.db_edit = db_edit
        self.db_edit.configure(upd_func=self.upd_record, del_func=self.del_record)

        self.cont_render = cont_render
        self.dbn_valid = ut.factory_valid(3, ext=self.db_list)

    def child_app(self):
        self.app = tk.Toplevel()

        self.set_app_chd(2, self.app)
        self.db_edit.configure(parent=self.app)

        self.app.geometry('%sx%s+%s+%s' % (self.geo['w'], self.geo['h'], self.geo['x'], self.geo['y']))
        self.app.minsize(400, 200)
        self.app.focus_set()

        self.db_var.set(self.var[2])
        fnt = {0: self.font['AppBsc'], 1: [self.font['AppBsc'][0], int(0.8*self.font['AppBsc'][1])]}

        ttk.Style().configure('dbs.Treeview', font=fnt[0])
        ttk.Style().configure('dbs.Treeview.Heading', font=fnt[1])

        self.db_tree = ttk.Treeview(self.app, selectmode='browse', style='dbs.Treeview')
        self.db_tree_scr_ver = ttk.Scrollbar(self.app, orient=tk.VERTICAL, command=self.db_tree.yview)
        self.db_tree_scr_hor = ttk.Scrollbar(self.app, orient=tk.HORIZONTAL, command=self.db_tree.xview)
        self.db_tree_scr_cap = tk.Label(self.app, text='●')

        self.db_tree.configure(yscrollcommand=self.db_tree_scr_ver.set)
        self.db_tree.configure(xscrollcommand=self.db_tree_scr_hor.set)
        self.db_tree['columns'] = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
        self.db_tree.column('#0', width=50, minwidth=50, stretch=False)
        self.db_tree.column('A', width=200, minwidth=50, stretch=False)
        self.db_tree.column('B', width=100, minwidth=50, stretch=False, anchor=tk.CENTER)
        self.db_tree.column('C', width=100, minwidth=50, stretch=False, anchor=tk.CENTER)
        self.db_tree.column('D', width=35, minwidth=35, stretch=False, anchor=tk.CENTER)
        self.db_tree.column('E', width=100, minwidth=50, stretch=False, anchor=tk.CENTER)
        self.db_tree.column('F', width=100, minwidth=50, stretch=False, anchor=tk.CENTER)
        self.db_tree.column('G', width=350, minwidth=100)
        self.db_tree.column('H', width=50, minwidth=50, stretch=False, anchor=tk.CENTER)
        self.db_tree.heading('#0', text=self.skw['ind'], command=self.pm_organize_db)
        self.db_tree.heading('A', text=self.skw['name'], anchor=tk.W)
        self.db_tree.heading('B', text=self.skw['date'])
        self.db_tree.heading('C', text=self.skw['time'])
        self.db_tree.heading('D', text=self.skw['utc'])
        self.db_tree.heading('E', text=self.skw['lat'])
        self.db_tree.heading('F', text=self.skw['lon'])
        self.db_tree.heading('G', text=self.skw['place'], anchor=tk.W)
        self.db_tree.heading('H', text=self.skw['sex'])
        self.db_tree_reload()

        self.wdg_set_pos()

        self.app.bind('<Configure>', self.on_config)
        self.app.bind('<FocusIn>', lambda *args: self.on_focus())
        self.db_tree.bind('<Destroy>', lambda *args: self.on_destroy())
        self.db_tree.bind('<Double-Button-1>', self.on_click_tree)
        self.db_tree.bind('<Button-3>', self.on_click_tree)

    def set_app_title(self): self.app.title('%s - %s' % (self.skw['title'], self.var[2]))

    def apply_cfg(self):
        fnt = {0: self.font['AppBsc'], 1: [self.font['AppBsc'][0], int(0.8*self.font['AppBsc'][1])]}
        ttk.Style().configure('dbs.Treeview', font=fnt[0])
        ttk.Style().configure('dbs.Treeview.Heading', font=fnt[1])

    def on_config(self, event):
        if self.app.wm_state() == 'zoomed':
            self.app.wm_state('normal')
            self.app.geometry('%sx%s' % (1110, 600))
        else:
            widget = str(event.widget).split('.!')[-1]
            if 'toplevel' in widget:
                self._x, self._y = event.x, event.y
                if self._w != event.width or self._h != event.height:
                    self._w, self._h = event.width, event.height
                    self.wdg_set_pos()

    def on_focus(self):
        self.set_ord_list(2, 1)
        self.ask_ent.configure(parent=self.app)

    def on_destroy(self):
        self.set_app_chd(2, None)
        self.set_ord_list(2, 0)
        self.set_chd_geo(2, w=self._w, h=self._h, x=self._x, y=self._y)
        self.db_edit.configure(parent=None)

    def wdg_set_pos(self):
        if self._w and self._h:
            self.db_tree.place(x=0, y=0, width=(self._w - 19), height=(self._h - 19))
            self.db_tree_scr_ver.place(x=(self._w - 20), y=0, width=20, height=(self._h - 20))
            self.db_tree_scr_hor.place(x=0, y=(self._h - 20), width=(self._w - 20), height=20)
            self.db_tree_scr_cap.place(x=(self._w - 20), y=(self._h - 20), width=20, height=20)

    def db_tree_reload(self):
        self.db_tree.delete(*self.db_tree.get_children())
        self.set_act_var(2, self.db_var.get())
        for i in self.get_rec_db(0):
            sex = self.sex[i[1]['sex']][0]
            self.db_tree.insert(
                '', 'end', text=i[0], values=(
                    i[1]['name'], '%d/%d/%d' % (i[1]['date'][0], i[1]['date'][1], i[1]['date'][2]),
                    '%02d:%02d' % (i[1]['time'][0], i[1]['time'][1]), round(i[1]['time'][3], 2),
                    '%02d%s%02d' % (i[1]['lat'][0], i[1]['lat'][3], i[1]['lat'][1]),
                    '%02d%s%02d' % (i[1]['lon'][0], i[1]['lon'][3], i[1]['lon'][1]), i[1]['place'], sex)
            )
        self.set_app_title()

    def on_click_tree(self, event):
        item = self.db_tree.identify('item', event.x, event.y)
        ind = self.db_tree.item(item, 'text')

        if event.num == 1:
            if ind:
                self.apply_data(self.get_rec_db(ind))
                self.app.destroy()
        elif event.num == 3:
            values = self.db_tree.item(item)['values']

            self.db_tree.selection_remove(self.db_tree.focus())
            self.db_tree.focus(item)
            self.db_tree.selection_add(item)

            self.db_list.clear()
            self.db_var.set(self.var[2])
            for i in filter(lambda x: x.endswith('.db'), os.listdir(self.pth[2])):
                self.db_list.append(i.split('.')[0])

            sm_db = tk.Menu(self.app, tearoff=0)
            for i in self.db_list:
                sm_db.add_radiobutton(label=i, value=i, variable=self.db_var, command=self.pm_load_db)
            sm_db.add_separator()
            sm_db.add_command(label=self.skw['org'], command=self.pm_organize_db)
            sm_db.add_command(
                label=self.tkw['new'],
                command=lambda: self.ask_ent.mb(self.tkw['new'], '', self.create_db, self.dbn_valid))
            sm_db.add_command(
                label=self.tkw['rename'],
                command=lambda: self.ask_ent.mb(self.tkw['rename'], self.var[2], self.pm_rename_db, self.dbn_valid))
            sm_db.add_command(
                label=self.tkw['delete'], command=lambda: self.ask_ent.mb(self.var[2], 'qwsDel', self.pm_delete_db))

            pm = tk.Menu(self.app, tearoff=0)

            pm.add_cascade(label=self.skw['title'], menu=sm_db)
            pm.add_separator()
            pm.add_command(
                label=self.tkw['new'], command=lambda: self.mb_upd_record(0, ex=event.x_root, ey=event.y_root))
            pm.add_command(
                label=self.tkw['src'], command=lambda: self.mb_upd_record(1, ex=event.x_root, ey=event.y_root))
            pm.add_separator()
            pm.add_command(label=self.tkw['apply'], command=lambda: self.apply_data(self.get_rec_db(ind)))
            pm.add_command(
                label=self.tkw['edit'], command=lambda: self.mb_upd_record(0, ind, event.x_root, event.y_root))
            pm.add_command(label=self.tkw['copy'], command=lambda: self.pm_copy(ind))
            pm.add_command(label=self.tkw['cut'], command=lambda: self.pm_cut(ind, item))
            state = tk.NORMAL if self.buf else tk.DISABLED
            pm.add_command(label=self.tkw['insert'], state=state, command=self.pm_insert)
            pm.add_command(label=self.tkw['delete'], command=lambda: self.mb_upd_record(2, ind, title=values[0]))

            if ind:
                for i in {5, 6, 7, 8, 10}:
                    pm.entryconfig(i, state=tk.NORMAL)
            else:
                for i in {5, 6, 7, 8, 10}:
                    pm.entryconfig(i, state=tk.DISABLED)

            pm.tk_popup(event.x_root, event.y_root)

    def apply_data(self, data):
        self.set_data_buf(data)
        self.set_act_var(10, 1)
        self.cont_render(31, 2015)
        self.set_wch_dbs(self.data_buf[0])

    def pm_load_db(self):
        self.db_tree_reload()
        self.set_wch_dbs(self.data_buf[0])

    def pm_delete_db(self):
        self.db_list.remove(self.var[2])
        os.remove('%s/%s.db' % (self.pth[2], self.var[2]))
        if self.db_list:
            self.set_act_var(2, self.db_list[0])
            self.db_var.set(self.db_list[0])
            self.db_tree_reload()
        else:
            name = self.skw['dbName']
            self.create_db(name)
            self.set_act_var(2, name)
            self.db_list.append(name)
            self.db_var.set(name)
            self.db_tree_reload()
        self.set_wch_dbs(self.data_buf[0])

    def pm_rename_db(self, name):
        os.rename(
            '%s/%s.db' % (self.pth[2], self.var[2]), '%s/%s.db' % (self.pth[2], name))
        self.set_act_var(2, name)
        self.set_app_title()

    def pm_copy(self, ind):
        self.buf = self.get_rec_db(ind)

    def pm_cut(self, ind, item):
        self.buf = self.get_rec_db(ind)
        self.del_rec_db(ind)
        self.db_tree.delete(item)
        self.set_wch_dbs(self.data_buf[0])

    def pm_insert(self):
        self.buf[0] = self.var[6]
        self.upd_rec_db(self.buf)
        self.db_tree_reload()
        self.buf = None
        self.set_wch_dbs(self.data_buf[0])

    def pm_organize_db(self):
        self.organize_db()
        self.db_tree_reload()
        self.set_wch_dbs(self.data_buf[0])

    def upd_record(self, data, mode=1):
        self.upd_rec_db(data)
        if mode:
            self.db_tree_reload()

    def del_record(self, ind, mode=1):
        self.del_rec_db(ind)
        self.set_wch_dbs(self.data_buf[0])
        if mode:
            self.db_tree_reload()

    def mb_upd_record(self, mode, ind=None, ex=0, ey=0, title=''):
        self.db_tree.selection_remove(self.db_tree.focus())
        if mode == 2:
            self.ask_ent.mb(title, 'qwsDel', lambda: self.del_record(ind))
        elif mode == 1:
            cur = self.get_cur_ind(self.data_buf)
            self.data_buf[0] = cur if cur else self.var[6]
            self.db_edit.mb(self.data_buf, ex, ey)
        else:
            self.db_edit.mb(self.get_rec_db(ind), ex, ey)


class ModalBoxDbaseEdit:
    _w, _h = 0, 0
    flag = 0
    wch_var = None
    name_var_r, date_var_r = None, None
    time_var_r, sex_var_r = None, None
    plc_var_r, crd_var_r = None, None
    nsew_var_r, hs_var_r = None, None
    app, plc_cb = None, None
    save_r_bt, save_p_bt = None, None
    apply_bt, del_r_bt = None, None
    parent = None
    upd_func, del_func = None, None
    data = None
    mode = 0

    def __init__(self, dbs, conf, loc, cont_render):
        self.data_buf = dbs.get_data_buf()
        self.set_data_buf = dbs.set_data_buf

        self.kwd = loc.get_sample_tkw()
        self.sex = {0: loc.get_sample_sex()}
        self.hss = {0: loc.get_sample_hss()}

        self.var = conf.get_act_var()
        self.cur_plc = conf.get_cur_plc()
        self.font = conf.get_src_font()

        self.set_app_chd = conf.set_app_chd
        self.set_ord_list = conf.set_ord_list
        self.set_act_var = conf.set_act_var
        self.get_wch_dbs = conf.get_wch_dbs
        self.set_wch_dbs = conf.set_wch_dbs

        self.atlas = ut.SmartDictJson('./Atlas.json', 1)

        self.name_var = tk.StringVar()
        self.date_var = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.time_var = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.sex_var = tk.StringVar()
        self.plc_var = tk.StringVar()
        self.crd_var = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.nsew_var = [tk.StringVar(), tk.StringVar()]
        self.hs_var = tk.StringVar()

        self.cont_render = cont_render

        self.date_vf = {
            0: ut.factory_valid(1, self.var[1][0], self.var[1][1]), 1: ut.factory_valid(1, 1, 12),
            28: ut.factory_valid(1, 1, 28), 29: ut.factory_valid(1, 1, 29),
            30: ut.factory_valid(1, 1, 30), 31: ut.factory_valid(1, 1, 31)
        }
        self.time_vf = {
            0: ut.factory_valid(1, 0, 23), 1: ut.factory_valid(1, 0, 59),
            2: ut.factory_valid(1, 0, 59), 3: ut.factory_valid(2, -12, 14)
        }
        self.crd_vf = {
            0: ut.factory_valid(1, 0, 90), 3: ut.factory_valid(1, 0, 180),
            1: ut.factory_valid(1, 0, 59), 2: ut.factory_valid(1, 0, 0)
        }

    def mb(self, data, cx=None, cy=None, mode=1):
        self.flag = 1
        self.mode = mode
        self.data = data
        if data[0] != self.var[6]:
            self.mode |= 2
        if not self.wch_var:
            self.wch_var = self.get_wch_dbs()

        self.sex[1] = {self.sex[0][i]: i for i in self.sex[0]}
        self.hss[1] = {self.hss[0][i]: i for i in self.hss[0]}

        self.create_app()
        self._w = self.app.winfo_screenwidth()
        self._h = self.app.winfo_screenheight()
        if cx is None:
            cx = 0.5*self._w - 400
        if cy is None:
            cy = 0.5*self._h - 200
        self.app.geometry('+%d+%d' % (cx, cy))
        self.app.resizable(width=False, height=False)
        self.set_app_title()

        fnt = self.font['AppCns']

        self.app.option_add('*TCombobox*Listbox.font', fnt)
        ttk.Style().configure('dbe.TButton', font=fnt)

        cap_lb = [tk.Label(self.app, text='  '), tk.Label(self.app, text='  ')]
        res_bt = ttk.Button(self.app, text='R', width=2, style='dbe.TButton', command=self.reset_form)
        name_en = ttk.Entry(self.app, font=fnt, textvariable=self.name_var)

        tod_bt = ttk.Button(self.app, text='N', width=2, style='dbe.TButton', command=self.change_time)
        date_en = []
        for i in [0, 1, 2]:
            width = 4 if i else 6
            date_en.append(ttk.Entry(self.app, font=fnt, width=width, justify=tk.CENTER, textvariable=self.date_var[i]))
        time_en = []
        for i in range(4):
            time_en.append(ttk.Entry(self.app, font=fnt, width=4, justify=tk.CENTER, textvariable=self.time_var[i]))
        sym_dt_ls = ['/', '/', ',', ':', ':', 'UTC']
        sym_dt_lb = []
        for i in range(6):
            sym_dt_lb.append(tk.Label(self.app, font=fnt, text=sym_dt_ls[i]))
        sex_cb = ttk.Combobox(
            self.app, values=list(self.sex[0].values()), textvariable=self.sex_var,
            font=fnt, width=8, state='readonly', justify=tk.CENTER
        )

        this_bt = ttk.Button(self.app, text='T', width=2, style='dbe.TButton', command=lambda: self.change_place(0))
        self.plc_cb = ttk.Combobox(
            self.app, values=self.atlas.keys(), textvariable=self.plc_var, justify=tk.LEFT, font=fnt)

        self.save_p_bt = ttk.Button(self.app, text='S', width=2, style='dbe.TButton', command=self.save_place)
        crd_var_dt = data[1]['lat'][0:3] + data[1]['lon'][0:3]
        sym_crd_ls = ['°', '\'', ',', '°', '\'']
        sym_crd_lb = []
        crd_en, ns_cb, ew_cb = [], None, None
        for i in range(6):
            if i == 3:
                ns_cb = ttk.Combobox(
                    self.app, values=['N', 'S'], textvariable=self.nsew_var[0],
                    width=3, state='readonly', justify=tk.CENTER, font=fnt
                )
            crd_en.append(ttk.Entry(self.app, font=fnt, width=3, justify=tk.CENTER, textvariable=self.crd_var[i]))
            if i < 5:
                sym_crd_lb.append(tk.Label(self.app, text=sym_crd_ls[i], font=fnt))
            if i == 5:
                ew_cb = ttk.Combobox(
                    self.app, values=['E', 'W'], textvariable=self.nsew_var[1],
                    width=3, state='readonly', justify=tk.CENTER, font=fnt
                )
        hs_cb = ttk.Combobox(
            self.app, values=list(self.hss[0].values()), textvariable=self.hs_var,
            font=fnt, width=8, state='readonly', justify=tk.CENTER
        )

        self.apply_bt = ttk.Button(
            self.app, width=9, style='dbe.TButton', text=self.kwd['apply'], command=self.apply_data
        )
        close_bt = ttk.Button(
            self.app, width=9, style='dbe.TButton', text=self.kwd['close'], command=lambda: self.app.destroy()
        )
        self.save_r_bt = ttk.Button(
            self.app, width=9, style='dbe.TButton', text=self.kwd['save'], command=self.upd_record
        )
        state = tk.NORMAL if self.mode & 2 else tk.DISABLED
        self.del_r_bt = ttk.Button(
            self.app, width=9, style='dbe.TButton', state=state, text=self.kwd['delete'], command=self.del_record
        )

        sa = tk.E + tk.W + tk.N + tk.S
        sv = tk.N + tk.S
        px, py = 10, 10

        res_bt.grid(row=0, column=0, padx=px, pady=py)
        name_en.grid(row=0, column=1, columnspan=17, pady=py, sticky=sa)
        cap_lb[0].grid(row=0, column=18)

        tod_bt.grid(row=1, column=0, padx=px, pady=py)
        date_en[0].grid(row=1, column=1, columnspan=2, pady=py, sticky=sa)
        sym_dt_lb[0].grid(row=1, column=3, pady=py)
        date_en[1].grid(row=1, column=4, pady=py, sticky=sa)
        sym_dt_lb[1].grid(row=1, column=5, pady=py)
        date_en[2].grid(row=1, column=6, pady=py, sticky=sa)
        sym_dt_lb[2].grid(row=1, column=7, padx=px/2, pady=py, sticky=tk.W)
        time_en[0].grid(row=1, column=8, pady=py, sticky=sa)
        sym_dt_lb[3].grid(row=1, column=9, pady=py)
        time_en[1].grid(row=1, column=10, pady=py, sticky=sa)
        sym_dt_lb[4].grid(row=1, column=11, pady=py)
        time_en[2].grid(row=1, column=12, pady=py, sticky=sa)
        cap_lb[1].grid(row=1, column=13)
        sym_dt_lb[5].grid(row=1, column=14, pady=py)
        time_en[3].grid(row=1, column=15, padx=px, pady=py, sticky=sa)
        sex_cb.grid(row=1, column=16, columnspan=2, pady=py, sticky=sa)

        this_bt.grid(row=2, column=0, padx=px, pady=py)
        self.plc_cb.grid(row=2, column=1, columnspan=17, pady=py, sticky=sa)

        self.save_p_bt.grid(row=3, column=0, pady=py)
        crd_en[0].grid(row=3, column=1, columnspan=2, pady=py, sticky=sa)
        sym_crd_lb[0].grid(row=3, column=3)
        crd_en[1].grid(row=3, column=4, pady=py, sticky=sa)
        sym_crd_lb[1].grid(row=3, column=5)
        crd_en[2].grid(row=3, column=6, pady=py, sticky=sa)
        ns_cb.grid(row=3, column=7, padx=px/2, pady=py, sticky=sv)
        sym_crd_lb[2].grid(row=3, column=8, sticky=tk.W)
        crd_en[3].grid(row=3, column=9, columnspan=2, pady=py, sticky=sa)
        sym_crd_lb[3].grid(row=3, column=11)
        crd_en[4].grid(row=3, column=12, pady=py, sticky=sa)
        sym_crd_lb[4].grid(row=3, column=13)
        crd_en[5].grid(row=3, column=14, pady=py, sticky=sa)
        ew_cb.grid(row=3, column=15, pady=py, sticky=sv)
        hs_cb.grid(row=3, column=16, columnspan=2, pady=py, sticky=sa)

        self.apply_bt.grid(row=4, column=0, columnspan=2, padx=px, pady=py, sticky=sa)
        close_bt.grid(row=4, column=3, columnspan=3, pady=py)
        self.save_r_bt.grid(row=4, column=13, columnspan=3, pady=py)
        self.del_r_bt.grid(row=4, column=16, columnspan=2, pady=py, sticky=sa)

        self.name_var.set(data[1]['name'])
        self.sex_var.set(self.sex[0][data[1]['sex']])
        self.plc_var.set(data[1]['place'])
        self.nsew_var[0].set(data[1]['lat'][3].upper())
        self.nsew_var[1].set(data[1]['lon'][3].upper())
        self.hs_var.set(self.hss[0][data[1]['sysHouse']])

        self.hs_var.trace_add('write', lambda *args: self.validate())
        for i in range(6):
            self.crd_var[i].set(crd_var_dt[i])
            self.crd_var[i].trace_add('write', lambda *args: self.validate())
            if i < 3:
                self.date_var[i].set(data[1]['date'][i])
                self.date_var[i].trace_add('write', lambda *args: self.validate())
            if i < 4:
                time = round(data[1]['time'][i], 2) if i == 3 else data[1]['time'][i]
                self.time_var[i].set(time)
                self.time_var[i].trace_add('write', lambda *args: self.validate())

        self.set_res_var()

        if self.mode & 1:
            self.app.bind('<Escape>', lambda *args: self.app.destroy())
        else:
            self.app.bind('<FocusIn>', lambda *args: self.set_ord_list(1, 1))
        self.app.bind('<Configure>', self.on_config)
        self.app.bind('<Shift-Control-T>', self.swi_tech_mode)
        self.app.bind('<Control-Up>', self.swi_tech_mode)
        self.app.bind('<Control-Down>', self.swi_tech_mode)
        self.app.bind('<Alt-Left>', self.swi_save_plc_bt)
        self.app.bind('<Alt-Right>', self.swi_save_plc_bt)
        self.plc_cb.bind('<<ComboboxSelected>>', lambda *args: self.change_place())
        self.plc_cb.bind('<Destroy>', lambda *args: self.on_destroy())

    def configure(self, **kwargs):
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        if 'upd_func' in kwargs:
            self.upd_func = kwargs['upd_func']
        if 'del_func' in kwargs:
            self.del_func = kwargs['del_func']

    def create_app(self):
        self.app = tk.Toplevel()
        if self.mode & 1:
            self.app.transient(self.parent)
            self.app.grab_set()
        else:
            self.set_app_chd(1, self.app)
        self.app.focus_set()

    def on_config(self, event):
        if self.flag:
            widget = str(event.widget).split('.!')[-1]
            if 'toplevel' in widget:
                x = self._w - event.width - 12 if event.x + event.width > self._w - 2 else event.x
                y = self._h - event.height - 75 if event.y + event.height > self._h - 75 else event.y
                self.app.geometry('+%d+%d' % (x, y))
                self.flag = 0

    def on_destroy(self):
        self.atlas.dump()
        self.crd_var[0].set(0)
        if not self.mode & 1:
            self.set_app_chd(1, None)
            self.set_ord_list(1, 0)

    def set_app_title(self):
        if self.mode & 2:
            title = self.kwd['edit']
        else:
            title = self.kwd['new']
        if self.mode & 4:
            self.app.title('%s - №%s < ATTENTION TECH MODE! USE WITH CAUTION! >' % (title, self.data[0]))
        else:
            self.app.title('%s - №%s' % (title, self.data[0]))

    def set_bt_state(self, mask, state):
        if mask & 1:
            self.apply_bt.configure(state=state)
        if mask & 2:
            self.save_r_bt.configure(state=state)
        if mask & 4:
            self.save_p_bt.configure(state=state)
        if mask & 8:
            self.del_r_bt.configure(state=state)

    def swi_tech_mode(self, event):
        if event.keysym == 'T':
            self.mode ^= 4
        if self.mode & 4:
            if event.keysym == 'Up':
                self.data[0] += 1
            elif event.keysym == 'Down':
                self.data[0] = self.data[0] - 1 if self.data[0] > 1 else 1
        self.set_app_title()

    def swi_save_plc_bt(self, event):
        if event.keysym == 'Left':
            self.save_p_bt.configure(text='D')
        elif event.keysym == 'Right':
            self.save_p_bt.configure(text='S')

    def proc_form(self):
        utc = float(self.time_var[3].get())
        utc = round(utc, 2) if utc % 1 else round(utc)
        return {
            0: self.data[0],
            1: {
                'name': self.name_var.get(), 'place': self.plc_var.get(),
                'date': [int(self.date_var[0].get()), int(self.date_var[1].get()), int(self.date_var[2].get())],
                'time': [
                    int(self.time_var[0].get()), int(self.time_var[1].get()),
                    int(self.time_var[2].get()), utc
                ],
                'lat': [
                    int(self.crd_var[0].get()), int(self.crd_var[1].get()),
                    int(self.crd_var[2].get()), self.nsew_var[0].get().lower()
                ],
                'lon': [
                    int(self.crd_var[3].get()), int(self.crd_var[4].get()),
                    int(self.crd_var[5].get()), self.nsew_var[1].get().lower()
                ],
                'sysHouse': self.hss[1][self.hs_var.get()], 'sex': self.sex[1][self.sex_var.get()]
            },
            2: self.data[2]
        }

    def set_res_var(self):
        self.name_var_r = self.name_var.get()
        self.date_var_r = [self.date_var[0].get(), self.date_var[1].get(), self.date_var[2].get()]
        self.time_var_r = [
            self.time_var[0].get(), self.time_var[1].get(), self.time_var[2].get(), self.time_var[3].get()
        ]
        self.sex_var_r = self.sex_var.get()
        self.plc_var_r = self.plc_var.get()
        self.crd_var_r = [
            self.crd_var[0].get(), self.crd_var[1].get(), self.crd_var[2].get(),
            self.crd_var[3].get(), self.crd_var[4].get(), self.crd_var[5].get()
        ]
        self.nsew_var_r = [self.nsew_var[0].get(), self.nsew_var[1].get()]
        self.hs_var_r = self.hs_var.get()

    def reset_form(self):
        self.name_var.set(self.name_var_r)
        self.sex_var.set(self.sex_var_r)
        self.plc_var.set(self.plc_var_r)
        self.hs_var.set(self.hs_var_r)
        for i in range(6):
            self.crd_var[i].set(self.crd_var_r[i])
            if i < 4:
                self.time_var[i].set(self.time_var_r[i])
            if i < 3:
                self.date_var[i].set(self.date_var_r[i])
            if i < 2:
                self.nsew_var[i].set(self.nsew_var_r[i])

    def change_time(self):
        now = datetime.datetime.now()
        date = {0: now.year, 1: now.month, 2: now.day}
        time = {0: now.hour, 1: now.minute, 2: now.second}
        for i in {0, 1, 2}:
            self.date_var[i].set(date[i])
            self.time_var[i].set(time[i])

    def change_place(self, mode=1):
        if mode:
            select = self.plc_cb.get()
            place = self.atlas[select].copy()
            place['place'] = select
        else:
            place = self.cur_plc

        for i in range(8):
            if i < 3:
                self.crd_var[i].set(place['lat'][i])
            elif i == 3:
                self.nsew_var[0].set(place['lat'][3].upper())
            elif i < 7:
                self.crd_var[i-1].set(place['lon'][i-4])
            else:
                self.plc_var.set(place['place'])
                self.nsew_var[1].set(place['lon'][3].upper())
                self.time_var[3].set(place['utc'])

    def save_place(self):
        select = self.plc_var.get()
        if self.save_p_bt.cget('text') == 'S':
            if select not in self.atlas:
                utc = float(self.time_var[3].get())
                utc = round(utc, 2) if utc % 1 else round(utc)
                self.atlas[select] = {
                    'lat': [int(self.crd_var[0].get()), int(self.crd_var[1].get()),
                            int(self.crd_var[2].get()), self.nsew_var[0].get().lower()],
                    'lon': [int(self.crd_var[3].get()), int(self.crd_var[4].get()),
                            int(self.crd_var[5].get()), self.nsew_var[1].get().lower()],
                    'utc': utc
                }
                self.plc_cb.configure(values=self.atlas.keys())
        else:
            if select in self.atlas:
                del self.atlas[select]
                self.plc_cb.configure(values=self.atlas.keys())

    def apply_data(self):
        data = self.proc_form()
        if self.data[1]['date'] != data[1]['date'] or self.data[1]['time'] != data[1]['time']:
            data[2] = {}
        self.set_data_buf(data)
        self.set_act_var(10, 1)
        self.cont_render(31, 2015)
        self.set_wch_dbs(self.data_buf[0])
        self.app.destroy()

    def upd_record(self):
        data = self.proc_form()
        if self.data[1]['date'] != data[1]['date'] or self.data[1]['time'] != data[1]['time']:
            data[2] = {}
        self.upd_func(data, self.mode & 1)
        if not self.mode & 1 or self.wch_var.get() == self.data[0] and self.mode & 2:
            self.set_data_buf(data)
            self.set_act_var(10, 1)
            self.cont_render(31, 2015)
            self.set_wch_dbs(self.data_buf[0])
        else:
            self.set_wch_dbs(self.data_buf[0])
        self.app.destroy()

    def del_record(self):
        self.del_func(self.data[0], self.mode & 1)
        self.app.destroy()

    def validate(self):
        for i in [0, 3]:
            if not self.crd_vf[i](self.crd_var[i].get()):
                self.set_bt_state(7, tk.DISABLED)
                return False

        lat = int(self.crd_var[0].get())
        lon = int(self.crd_var[3].get())
        for i in [1, 2, 4, 5]:
            if i in {1, 2}:
                din_vf = self.crd_vf[1] if lat < 90 else self.crd_vf[2]
            else:
                din_vf = self.crd_vf[1] if lon < 180 else self.crd_vf[2]
            if not din_vf(self.crd_var[i].get()):
                self.set_bt_state(7, tk.DISABLED)
                return False

        lat += int(self.crd_var[1].get())/60 + int(self.crd_var[2].get())/3600
        h_sys = self.hss[1][self.hs_var.get()]
        if lat >= 66.5625 and h_sys in 'PKSOCB':
            self.hs_var.set(self.hss[0]['D'])

        if not self.time_vf[3](self.time_var[3].get()):
            self.set_bt_state(7, tk.DISABLED)
            return False

        self.set_bt_state(4, tk.NORMAL)

        for i in [0, 1, 2]:
            if i == 2:
                max_day = ut.get_max_day(int(self.date_var[0].get()), int(self.date_var[1].get()))
                if not self.date_vf[max_day](self.date_var[2].get()):
                    self.set_bt_state(3, tk.DISABLED)
                    return False
            elif not self.date_vf[i](self.date_var[i].get()):
                self.set_bt_state(3, tk.DISABLED)
                return False

        for i in range(3):
            if not self.time_vf[i](self.time_var[i].get()):
                self.set_bt_state(3, tk.DISABLED)
                return False

        self.set_bt_state(3, tk.NORMAL)
        return True

# -------------------------------------------------------------------------------------------------------------------- #
