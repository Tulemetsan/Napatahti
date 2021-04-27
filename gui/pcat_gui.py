# -------------------------------------------------------------------------------------------------------------------- #

import tkinter as tk
import tkinter.ttk as ttk
import core.utilities as ut

# @formatter:off


class PlanCatGui:
    _w, _h = 0, 0
    _x, _y = 0, 0
    app, cat_tree = None, None
    cat_tree_scr = None

    def __init__(self, abo,  conf, loc, ask_ent, cont_render):
        self.tkw = loc.get_sample_tkw()
        self.skw = loc.get_sample_pct()

        self.geo = conf.get_chd_geo(4)
        self.font = conf.get_src_font()

        self.set_app_chd = conf.set_app_chd
        self.set_ord_list = conf.set_ord_list
        self.set_chd_geo = conf.set_chd_geo

        self.base_pl = abo.get_base_pl()
        self.show_pl = abo.get_show_pl()
        self.cat_pl = abo.get_cat_pl()
        self.pl_crd_enb = abo.get_pl_crd_enb()
        self.pl_asp_enb = abo.get_pl_asp_enb()
        self.pl_str = abo.get_pl_str()

        self.get_pl_name = abo.get_pl_name
        self.upd_catalog = abo.upd_catalog
        self.swi_enb_sing = abo.swi_enb_sing
        self.swi_enb_mast = abo.swi_enb_mast
        self.dump_cat = abo.dump_cat

        self.ask_ent = ask_ent
        self.edit_pl = ModalBoxEditPlanet(abo, self.upd_record, self.font, loc.get_sample_pce())

        self.cont_render = cont_render

    def child_app(self):
        self.app = tk.Toplevel()
        self.set_app_chd(4, self.app)
        self.app.title(self.skw['title'])
        self.app.geometry('%sx%s+%s+%s' % (self.geo['w'], self.geo['h'], self.geo['x'], self.geo['y']))
        self.app.minsize(350, 170)
        self.app.focus_set()

        self.edit_pl.configure(parent=self.app)

        fnt = {0: self.font['AppSym'], 1: [self.font['AppBsc'][0], int(0.8*self.font['AppBsc'][1])]}

        ttk.Style().configure('plCat.Treeview', font=fnt[0])
        ttk.Style().configure('plCat.Treeview.Heading', font=fnt[1])

        self.cat_tree = ttk.Treeview(self.app, selectmode='browse', style='plCat.Treeview')
        self.cat_tree_scr = ttk.Scrollbar(self.app, orient=tk.VERTICAL, command=self.cat_tree.yview)

        self.cat_tree.configure(yscrollcommand=self.cat_tree_scr.set)
        self.cat_tree['columns'] = ('A', 'B', 'C', 'D')
        self.cat_tree.column('#0', width=60, stretch=False, minwidth=60)
        self.cat_tree.column('A', width=60, minwidth=60, stretch=False, anchor=tk.CENTER)
        self.cat_tree.column('B', width=35, minwidth=35, stretch=False, anchor=tk.CENTER)
        self.cat_tree.column('C', width=35, minwidth=35, stretch=False, anchor=tk.CENTER)
        self.cat_tree.column('D', width=140, minwidth=140, anchor=tk.CENTER)
        self.cat_tree.heading('#0', text=self.skw['id'])
        self.cat_tree.heading('A', text=self.skw['sym'])
        self.cat_tree.heading('B', text=self.skw['enbDis'], command=lambda: self.chg_enb_mast(0))
        self.cat_tree.heading('C', text=self.skw['asp'], command=lambda: self.chg_enb_mast(1))
        self.cat_tree.heading('D', text=self.skw['crd'])
        self.cat_tree_reload(0)

        self.wdg_set_pos()

        self.app.bind('<Configure>', self.on_config)
        self.app.bind('<FocusIn>', lambda *args: self.on_focus())
        self.cat_tree.bind('<Destroy>', lambda *args: self.on_destroy())
        self.cat_tree.bind('<Double-Button-1>', self.on_click_tree)
        self.cat_tree.bind('<Double-Button-2>', self.on_click_tree)
        self.cat_tree.bind('<Button-3>', self.on_click_tree)

    def apply_cfg(self):
        fnt = {0: self.font['AppSym'], 1: [self.font['AppBsc'][0], int(0.8*self.font['AppBsc'][1])]}
        ttk.Style().configure('plCat.Treeview', font=fnt[0])
        ttk.Style().configure('plCat.Treeview.Heading', font=fnt[1])

    def on_config(self, event):
        if self.app.wm_state() == 'zoomed':
            self.app.wm_state('normal')
            self.app.geometry('%sx%s' % (350, 410))
        else:
            widget = str(event.widget).split('.!')[-1]
            if 'toplevel' in widget:
                if self._w != event.width or self._h != event.height:
                    self._w, self._h = event.width, event.height
                    self.wdg_set_pos()
                self._x, self._y = event.x, event.y

    def on_focus(self):
        self.set_ord_list(4, 1)
        self.ask_ent.configure(parent=self.app)

    def on_destroy(self):
        self.set_app_chd(4, None)
        self.set_ord_list(4, 0)
        self.set_chd_geo(4, w=self._w, h=self._h, x=self._x, y=self._y)
        self.dump_cat()

    def wdg_set_pos(self):
        self.cat_tree.place(x=0, y=0, width=(self._w - 19), height=self._h)
        self.cat_tree_scr.place(x=(self._w - 20), y=0, width=20, height=self._h)

    def cat_tree_reload(self, mode=1):
        if mode:
            self.cat_tree.delete(*self.cat_tree.get_children())

        for i in sorted(self.cat_pl):
            c_enb = '|' if i in self.pl_crd_enb else '-'
            a_enb = '|' if i in self.pl_asp_enb else '-'
            self.cat_tree.insert('', 'end', text=i, values=(self.cat_pl[i], c_enb, a_enb, self.pl_str[i]))

    def on_click_tree(self, event):
        item = self.cat_tree.identify('item', event.x, event.y)
        ind = self.cat_tree.item(item, 'text')

        self.cat_tree.selection_remove(self.cat_tree.focus())
        self.cat_tree.focus(item)
        self.cat_tree.selection_add(item)

        if event.num == 1:
            self.chg_enb_sing(item, 0)
        elif event.num == 2:
            self.chg_enb_sing(item, 1)
        elif event.num == 3:
            pm = tk.Menu(self.app, tearoff=0)
            pm.add_command(label='< %s %s >' % (self.get_pl_name(ind, self.skw['pmTitle']), ind), state=tk.DISABLED)
            pm.add_separator()
            pm.add_command(
                label=self.tkw['new'],
                command=lambda: self.edit_pl.mb(self.skw['newTitle'], None, event.x_root, event.y_root)
            )
            if ind != '':
                label = self.tkw['disable'] if ind in self.pl_crd_enb else self.tkw['enable']
                pm.add_command(label=label, command=lambda: self.chg_enb_sing(item, 0))
                label = self.skw['aspOff'] if ind in self.pl_asp_enb else self.skw['aspOn']
                pm.add_command(label=label, command=lambda: self.chg_enb_sing(item, 1))
                pm.add_command(
                    label=self.tkw['edit'],
                    command=lambda: self.edit_pl.mb(self.get_pl_name(ind), ind, event.x_root, event.y_root)
                )
                state = tk.DISABLED if ind in self.base_pl else tk.NORMAL
                pm.add_command(
                    label=self.tkw['delete'], state=state,
                    command=lambda: self.ask_ent.mb(
                        '%s %s' % (self.get_pl_name(ind), ind), 'qwsDel', lambda: self.upd_record(ind))
                )
            pm.tk_popup(event.x_root, event.y_root)

    def chg_enb_sing(self, item, mode=1):
        ind = self.cat_tree.item(item, 'text')
        if ind != '':
            self.swi_enb_sing(ind, mode)
            values = self.cat_tree.item(item)['values']
            if mode:
                calc = 4
                rend = 288
                values[mode+1] = '|' if ind in self.pl_asp_enb else '-'
            else:
                calc = 20
                rend = 464
                values[mode+1] = '|' if ind in self.pl_crd_enb else '-'
            self.cat_tree.item(item, text=ind, values=values)
            self.cont_render(calc, rend)

    def chg_enb_mast(self, mode=1):
        self.swi_enb_mast(mode)
        self.cat_tree_reload()
        self.cont_render(4, 288) if mode else self.cont_render(20, 464)

    def upd_record(self, ind, sym=None, mode=1):
        self.upd_catalog(ind, sym, mode)
        self.cat_tree_reload()
        if sym is None:
            calc = 20  # del
            rend = 336
        elif mode:
            calc = 0  # upd
            rend = 348
        else:
            calc = 4  # new
            rend = 0
        self.cont_render(calc, rend)


class ModalBoxEditPlanet:
    _w, _h = 0, 0
    flag = 0
    sym_var_r, ind_var_r = None, None
    sym_en, ind_en = None, None
    app, sav_bt = None, None
    parent = None
    mode = 0

    def __init__(self, abo, upd_func, font, kwd):
        self.base_pl = abo.get_base_pl()
        self.cat_pl = abo.get_cat_pl()

        self.sym_var = tk.StringVar()
        self.ind_var = tk.StringVar()

        self.upd_func = upd_func

        self.swe_valid = abo.swe_valid
        self.ind_valid = ut.factory_valid(1, 0, 1000000, ext=self.cat_pl)
        self.sym_valid = ut.factory_valid(4, max_len=1)

        self.font = font
        self.kwd = kwd

    def mb(self, title='', ind=None, cx=None, cy=None):
        self.flag = 1
        self.create_app()

        self._w = self.app.winfo_screenwidth()
        self._h = self.app.winfo_screenheight()
        if cx is None:
            cx = 0.5*self._w - 100
        if cy is None:
            cy = 0.5*self._h - 50

        self.app.geometry('+%d+%d' % (cx, cy))
        self.app.resizable(width=False, height=False)
        self.app.title(title)

        if ind is None:
            self.mode = 0
            state = {0: tk.NORMAL, 1: tk.DISABLED}
        else:
            self.mode = 1
            state = {0: tk.DISABLED}
            if ind in self.base_pl:
                state[1] = tk.DISABLED
            else:
                state[1] = tk.NORMAL

        fnt = {0: self.font['AppBsc'], 1: self.font['AppSym']}

        ttk.Style().configure('plEdit.TButton', font=fnt[0])

        res_bt = ttk.Button(self.app, width=2, style='plEdit.TButton', text='R', command=self.reset)
        sym_lb = tk.Label(self.app, font=fnt[0], text=self.kwd['sym'])
        self.sym_en = ttk.Entry(self.app, width=4, font=fnt[1], textvariable=self.sym_var, justify=tk.CENTER)
        self.ind_en = ttk.Entry(
            self.app, width=8, font=fnt[0], textvariable=self.ind_var, state=state[0], justify=tk.CENTER)
        ind_lb = tk.Label(self.app, font=fnt[0], text=self.kwd['ind'])
        self.sav_bt = ttk.Button(self.app, width=9, style='plEdit.TButton', text=self.kwd['save'], command=self.update)
        del_bt = ttk.Button(
            self.app, width=9, style='plEdit.TButton', text=self.kwd['delete'], state=state[1], command=self.delete)
        clo_bt = ttk.Button(
            self.app, width=9, style='plEdit.TButton', text=self.kwd['close'], command=lambda: self.app.destroy())

        px, py = 10, 10
        res_bt.grid(row=0, column=0, padx=px, pady=py)
        sym_lb.grid(row=0, column=1, sticky=tk.E)
        self.sym_en.grid(row=0, column=2, padx=px, pady=py)
        ind_lb.grid(row=0, column=3, sticky=tk.E)
        self.ind_en.grid(row=0, column=4, padx=px, pady=py)
        self.sav_bt.grid(row=1, column=0, columnspan=2, padx=px, pady=py, sticky=tk.W)
        del_bt.grid(row=1, column=2, columnspan=2, padx=px, pady=py, sticky=tk.E+tk.W)
        clo_bt.grid(row=1, column=4, columnspan=2, padx=px, pady=py, sticky=tk.E)

        self.ind_var.trace_add('write', lambda *args: self.validate())
        self.sym_var.trace_add('write', lambda *args: self.validate())

        if self.mode:
            self.ind_var.set(ind)
            self.sym_en.focus_set()
        else:
            self.ind_en.focus_set()
            self.ind_var.set('')
        sym = self.cat_pl[ind] if ind in self.cat_pl else '¾'
        self.sym_var.set(sym)

        self.ind_var_r = self.ind_var.get()
        self.sym_var_r = self.sym_var.get()

        self.app.bind('<Configure>', self.on_config)
        self.app.bind('<Escape>', lambda *args: self.app.destroy())
        self.app.bind('<Return>', lambda *args: self.on_return())

    def configure(self, **kwargs):
        if 'parent' in kwargs:
            self.parent = kwargs['parent']

    def create_app(self):
        self.app = tk.Toplevel(self.parent)
        self.app.transient(self.parent)
        self.app.grab_set()
        self.app.focus_set()

    def on_config(self, event):
        if self.flag:
            widget = str(event.widget).split('.!')[-1]
            if 'toplevel' in widget:
                x = self._w - event.width - 12 if event.x + event.width > self._w - 2 else event.x
                y = self._h - event.height - 75 if event.y + event.height > self._h - 75 else event.y
                self.app.geometry('+%d+%d' % (x, y))
                self.flag = 0

    def on_return(self):
        if str(self.sav_bt.cget('state')) == tk.NORMAL:
            self.update()

    def reset(self):
        self.sym_var.set(self.sym_var_r)
        self.ind_var.set(self.ind_var_r)
        self.sym_en.focus_set() if self.mode else self.ind_en.focus_set()

    def update(self):
        self.upd_func(int(self.ind_var.get()), self.sym_var.get(), self.mode)
        self.app.destroy()

    def delete(self):
        self.upd_func(int(self.ind_var.get()))
        self.app.destroy()

    def validate(self):
        if not self.mode:
            if not self.ind_valid(self.ind_var.get()):
                self.sav_bt.configure(state=tk.DISABLED)
                return False
            if not self.swe_valid(int(self.ind_var.get())):
                self.sav_bt.configure(state=tk.DISABLED)
                return False

        if not self.sym_valid(self.sym_var.get()):
            self.sav_bt.configure(state=tk.DISABLED)
            return False

        self.sav_bt.configure(state=tk.NORMAL)
        return True

# -------------------------------------------------------------------------------------------------------------------- #
