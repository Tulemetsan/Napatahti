# -------------------------------------------------------------------------------------------------------------------- #

import os
import shutil
import tkinter as tk
import tkinter.ttk as ttk
import core.utilities as ut
from tkinter.colorchooser import askcolor
from .src_class import GuiSmartTable

# @formatter:off


class AspPageGui(GuiSmartTable):
    _x, _y = 0, 0
    flag = 1
    tree_pg, tree_sm = None, None
    tree, ent_c = None, None
    tree_scr_ver, tree_scr_cap = None, None

    def __init__(self, apg, conf, loc, ask_ent, cont_render):
        self.tkw = loc.get_sample_tkw()
        self.skw = loc.get_sample_apg()
        self.hkw = loc.get_hd_kwd_apg()

        self.pth = conf.get_app_pth()
        self.var = conf.get_act_var()
        self.geo = conf.get_chd_geo(3)
        self.dim = conf.get_apg_dim()
        self.col = conf.get_apg_col()
        self.font = conf.get_src_font()

        self.set_app_chd = conf.set_app_chd
        self.set_ord_list = conf.set_ord_list
        self.set_chd_geo = conf.set_chd_geo
        self.set_act_var = conf.set_act_var

        self.pl_src = apg.get_pl_src()
        self.asp_src = apg.get_asp_src()
        self.asp_enb = apg.get_asp_enb()
        self.orb_4pl = apg.get_asp_orb()
        self.orb_4cs = apg.get_asp_orb(1)
        self.orb_4mx = apg.get_asp_orb(2)
        self.asp_sym = apg.get_asp_prop(mode=1)
        self.asp_col = apg.get_asp_prop(mode=2)
        self.asp_ftp = apg.get_asp_prop(mode=3)
        self.asp_dsh = apg.get_asp_prop(mode=4)
        self.asp_pnt = apg.get_asp_pnt()

        self.get_st_flag = apg.get_st_flag
        self.swi_st_flag = apg.swi_st_flag
        self.apply_stat = apg.apply_stat
        self.get_pg_tit = apg.get_pg_tit
        self.set_pg_tit = apg.set_pg_tit
        self.use_sam = apg.use_sam
        self.dump_apg = apg.dump_apg
        self.load_apg = apg.load_apg

        self.del_asp = apg.del_asp
        self.set_asp_enb = apg.set_asp_enb
        self.set_asp_pnt = apg.set_asp_pnt
        self.set_asp_orb = apg.set_asp_orb

        self.tab_min_w = 11*self.dim['CellWid'] + 21
        self.tab_min_h = 4*self.dim['CellHgt'] + 21
        self.asp_num = len(self.asp_src)

        self.pg_name = set()
        self.sample = ut.SmartDictJson('%s/Sample.txt' % self.pth[3], 0, self.skw['bltSm'])

        self.ask_ent = ask_ent
        self.edit_asp = ModalBoxEditAsp(apg, self.apply_chg, self.font, loc.get_sample_ase(), conf.get_ase_col())

        self.ent_c_var = tk.StringVar()
        self.acc_var = tk.IntVar()

        self.cont_render = cont_render
        self.pg_valid = ut.factory_valid(3, ext=self.pg_name)
        self.sam_valid = ut.factory_valid(4, ext=self.sample)

    def child_app(self):
        GuiSmartTable.child_app(self)

        self.set_app_chd(3, self.app)
        self.edit_asp.configure(parent=self.app)

        self.set_app_title()
        self.app.geometry('%dx%d+%d+%d' % (self.geo['w'], self.geo['h'], self.geo['x'], self.geo['y']))
        self.app.minsize(self.dim['TreeWid'] + self.tab_min_w, self.tab_min_h)
        self.app.maxsize(self.dim['TreeWid'] + 28*self.dim['CellWid'] + 21, 0)

        self.flag = 1
        self.acc_var.set(self.var[4])

        ft = self.font['AppBsc']
        bg = self.col['BkgCol']
        fg = self.col['FrgCol']

        ttk.Style().configure('treeClean', background=bg, foreground=fg, font=ft)
        ttk.Style().layout('treeClean', [])

        self.tree = ttk.Treeview(self.m_frame, show='tree', style='treeClean')
        self.tree_scr_ver = ttk.Scrollbar(self.m_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree_scr_cap = tk.Label(self.m_frame, text='●')
        self.ent_c = tk.Entry(self.cnv, textvariable=self.ent_c_var, bg=bg, fg=fg, font=ft, justify=tk.CENTER)

        self.tree.configure(yscrollcommand=self.tree_scr_ver.set)
        self.tree_reload(0)

        self.wdg_set_pos(3)
        self.tab_render()

        self.app.bind('<Configure>', self.on_config)
        self.app.bind('<FocusIn>', lambda *args: self.on_focus())
        self.m_frame.bind('<Destroy>', lambda *args: self.on_destroy())
        self.app.bind('<KeyPress>', self.on_ent_c_tab_press)
        self.tree.bind('<Button-1>', self.on_click_tree)
        self.tree.bind('<Button-3>', self.on_click_tree)
        self.cnv.bind('<Double-Button-1>', self.on_click)
        self.cnv.bind('<Button-3>', self.on_click)
        self.cnv.bind('<MouseWheel>', self.on_cnv_mouse_wheel)
        self.cnv.bind('<Motion>', self.on_motion)
        self.cnv.bind('<Leave>', lambda *args: self.cnv.delete('mark'))
        self.ent_c.bind('<Return>', lambda *args: self.on_ent_c_return())

    def tab_upd(self): self.tab_upd_src(self.asp_num + 1, 28, self.dim['TreeWid'])
    def cnv_scr_upd(self): self.cnv_scr_upd_src(self.asp_num + 1, 28, self.dim['TreeWid'])
    def next_ind(self): self.next_ind_src(self.asp_num + 1, 28, 4, 21, 27, self.asp_src[self._iy-1] == 0)

    def apply_cfg(self):
        ft = self.font['AppBsc']
        bg = self.col['BkgCol']
        fg = self.col['FrgCol']
        ttk.Style().configure('treeClean', background=bg, foreground=fg, font=ft)
        self.ent_c.configure(bg=bg, fg=fg, font=ft)
        self.tab_render()

    def on_config(self, event):
        cw = self.dim['CellWid']
        ch = self.dim['CellHgt']
        tw = self.dim['TreeWid']

        if self.app.wm_state() == 'zoomed':
            self.app.wm_state('normal')
            self.app.geometry('%dx%d' % (20*cw + tw + 21, 24*ch + 21))
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
                nw = int((self._w - tw - 20)/cw)
                nh = int((self._h - ch - 20)/ch)
                nw = nw*cw + tw + 20
                nh = (nh + 1)*ch + 20
                self.app.geometry('%dx%d' % (nw, nh))

                self.pre_cleaning()
                self.wdg_set_pos(252)
                self.cnv_scr_upd()
                self.tab_upd()

    def on_focus(self):
        self.set_ord_list(3, 1)
        self.ask_ent.configure(parent=self.app)

    def on_destroy(self):
        self.set_app_chd(3, None)
        self.set_ord_list(3, 0)
        self.set_chd_geo(3, w=self._w, h=self._h, x=self._x, y=self._y)
        self._sx, self._sy = 0, 0
        self._nc, self._nr = 0, 0
        self.dump_apg()
        self.sample.dump()

    def on_motion(self, event):
        if self.flag:
            self.on_motion_src(event, self.col['EntMrk'])

    def on_cnv_scroll(self, *args, mode):
        self.flag = 1
        self.pre_cleaning()
        GuiSmartTable.on_cnv_scroll(self, *args, mode=mode)

    def on_cnv_mouse_wheel(self, event):
        self.flag = 1
        self.pre_cleaning()
        GuiSmartTable.on_cnv_mouse_wheel(self, event)
        self.on_motion(event)

    def on_ent_c_return(self):
        txt, tag = self.ent_c_var_save()
        self.flag = 1

        self.pre_cleaning()
        self.cnv.delete(tag)
        self.set_cell_txt(txt, tag)

    def on_ent_c_tab_press(self, event):
        if 'entry' in str(event.widget).split('.!')[-1] and event.keysym == 'Tab':
            txt, tag = self.ent_c_var_save()
            self.cnv.delete(tag)
            self.set_cell_txt(txt, tag)
            self.next_ind()
            self.ent_c_set()

    def set_cell_txt(self, txt, tag):
        cw = self.dim['CellWid']
        ch = self.dim['CellHgt']
        ft = self.font['AppBsc']
        fg = self.col['FrgCol']

        self.cnv.create_text(
            cw*(self._ix - self._sx + 0.5), ch*(self._iy - self._sy + 0.5),
            text=txt, font=ft, fill=fg, anchor=tk.CENTER, tag=tag)

    def set_app_title(self):
        name = self.get_pg_tit()
        title = (self.skw['title'], name) if name else (self.skw['title'], self.skw['bltPg'])
        self.app.title('%s - %s' % title)

    def pre_cleaning(self):
        self.cnv.delete('mark')
        self.cnv.delete('entMark')
        self.ent_c.place_forget()
        self.app.focus_set()

    def tree_reload(self, mode=1):
        if mode:
            self.tree.delete(*self.tree.get_children())

        self.tree_pg = self.tree.insert('', 1, text=self.skw['treePg'], open=True, tag='pgTitle')
        self.tree_sm = self.tree.insert('', 2, text=self.skw['treeSm'], open=True, tag='smTitle')

        self.pg_name.clear()
        self.pg_name.add(self.skw['bltPg'])
        pg_list = filter(lambda x: x.endswith('.json'), os.listdir(self.pth[3]))

        self.tree.insert(self.tree_pg, 0, text=self.skw['bltPg'], tag='pgList')
        for i in pg_list:
            page = i.split('.')[0]
            self.pg_name.add(page)
            self.tree.insert(self.tree_pg, 'end', text=page, tag='pgList')

        self.tree.insert(self.tree_sm, 0, text=self.skw['bltSm'], tag='smList')
        for i in self.sample.keys():
            if i == self.skw['bltSm']:
                continue
            self.tree.insert(self.tree_sm, 'end', text=i, tag='smList')

    def wdg_set_pos(self, mask):
        cw = self.dim['CellWid']
        ch = self.dim['CellHgt']
        tw = self.dim['TreeWid']

        if mask & 1:
            self.m_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        if mask & 2:
            self.cnv.place(x=tw, y=0, width=28*cw, height=ch*(self.asp_num + 1) + 1)
        if mask & 4:
            self.tree.place(x=2, y=2, width=tw - 22, height=self._h - 4)
        if mask & 8:
            self.tree_scr_ver.place(x=tw - 20, y=0, width=20, height=self._h - 20)
        if mask & 16:
            self.tree_scr_cap.place(x=tw - 20, y=self._h - 20, width=20, height=20)
        if mask & 32:
            self.cnv_scr_ver.place(x=self._w - 20, y=0, width=20, height=self._h - 20)
        if mask & 64:
            self.cnv_scr_hor.place(x=tw, y=self._h - 20, width=self._w - tw - 20, height=20)
        if mask & 128:
            self.cnv_scr_cap.place(x=self._w - 20, y=self._h - 20, width=20, height=20)
        if mask & 256:
            self.ent_c.place(
                x=(self._ix - self._sx)*cw + 1, y=(self._iy - self._sy)*ch + 1, width=cw - 1, height=ch - 1)

    def tab_render(self):
        cw = self.dim['CellWid']
        ch = self.dim['CellHgt']
        ft = [self.font['AppBsc'][0], int(0.75*self.font['AppBsc'][1])]
        px = cw/2
        py = ch/2
        txt = ''
        tag = ''
        asp = 0

        self.cnv.delete('all')

        for i in range(self.asp_num + 1):
            if i > 0:
                asp = self.asp_src[i-1]
            for j in range(28):
                sx, sy = self._sx, self._sy
                font = self.font['AppBsc']
                col = self.col['FrgCol']
                flag = 1
                if i == 0:
                    if 3 < j < 21:
                        font = self.font['AppSym']
                    txt = self.hkw[j]
                    tag = ''
                    if 3 < j < self._sx + 4:
                        flag = 0
                    if j < 4:
                        sx = 0
                    sy = 0
                elif j == 0:
                    if self.asp_ftp[asp] == 0:
                        font = ft
                    else:
                        font = self.font['AppSym']
                    txt = self.asp_sym[asp]
                    tag = ''
                    sx = 0
                    if i < self._sy + 1:
                        flag = 0
                elif j == 1:
                    txt = ut.pr_round(asp, 2)
                    tag = ''
                    sx = 0
                    if i < self._sy + 1:
                        flag = 0
                elif j == 2:
                    flag = 2
                    tag = ''
                    sx = 0
                    if i < self._sy + 1:
                        flag = 0
                elif j == 3:
                    if asp in self.asp_enb:
                        txt = self.skw['enb']
                        col = self.col['AspEnb']
                    else:
                        txt = self.skw['dis']
                        col = self.col['AspDis']
                    tag = 'ED%.2f' % asp
                    sx = 0
                    if i < self._sy + 1:
                        flag = 0
                elif 3 < j < 21:
                    ind = self.pl_src[j-4]
                    txt = ut.pr_round(self.orb_4pl[(asp, ind)], 4)
                    tag = 'a%.2f%d' % (asp, ind)
                    if 3 < j < self._sx + 4:
                        flag = 0
                    if i < self._sy + 1:
                        flag = 0
                elif j == 21:
                    txt = ut.pr_round(self.orb_4cs[asp], 4)
                    tag = 'h%.2f' % asp
                    if i < self._sy + 1:
                        flag = 0
                elif 21 < j < 27:
                    if asp == 0:
                        txt = ut.pr_round(self.orb_4mx[j-22], 4)
                        tag = 'm%d' % (j-22)
                    else:
                        flag = 3
                    if i < self._sy + 1:
                        flag = 0
                elif j == 27:
                    txt = ut.pr_round(self.asp_pnt[asp], 2)
                    tag = 'p%.2f' % asp
                    if i < self._sy + 1:
                        flag = 0

                x = cw * (j - sx)
                y = ch * (i - sy)
                if flag:
                    self.cnv.create_rectangle(
                        x, y, x + cw, y + ch, fill=self.col['BkgCol'], outline=self.col['CellFrm'])
                if flag == 1:
                    self.cnv.create_text(x + px, y + py, text=txt, font=font, fill=col, anchor=tk.CENTER, tag=tag)
                elif flag == 2:
                    x1 = x + 0.2*cw
                    x2 = x + 0.8*cw
                    y1 = y + 0.4*ch
                    for k in range(3):
                        self.cnv.create_line(
                            x1, y1 + k, x2, y1 + k, width=1, fill=self.asp_col[asp], dash=self.asp_dsh[asp])

    def on_click(self, event):
        self.on_click_src(event, 4, 1)

        col = self.col['AspEnb']
        asp = 0
        cw = self.dim['CellWid']
        ch = self.dim['CellHgt']
        ft = self.font['AppBsc']

        if self._iy > 0:
            asp = self.asp_src[self._iy-1]

        if event.num == 1:
            if self._iy == 0:
                self.pre_cleaning()
                if self._ix == 3:
                    txt = self.skw['enb']
                    if self.asp_enb:
                        self.set_asp_enb(mode=0)
                        txt = self.skw['dis']
                        col = self.col['AspDis']
                    else:
                        self.set_asp_enb(mode=1)
                    for i in range(self.asp_num):
                        self.cnv.delete('ED%.2f' % self.asp_src[i])
                        if i >= self._sy:
                            self.cnv.create_text(
                                cw*(self._ix + 0.5), ch*(i - self._sy + 1.5), text=txt,
                                font=ft, fill=col, anchor=tk.CENTER, tag=('ED%.2f' % self.asp_src[i])
                            )
                    self.cont_render(8, 288)
                if self._ix == 0:
                    self.edit_asp.mb(None, event.x_root, event.y_root)
            elif 0 < self._iy < self.asp_num + 1:
                if self._ix < 3:
                    self.pre_cleaning()
                    self.edit_asp.mb(self.asp_src[self._iy-1], event.x_root, event.y_root)
                elif self._ix == 3:
                    self.pre_cleaning()
                    if asp in self.asp_enb:
                        self.set_asp_enb(asp, 0)
                        txt = self.skw['dis']
                        col = self.col['AspDis']
                    else:
                        self.set_asp_enb(asp, 1)
                        txt = self.skw['enb']
                    self.cnv.delete('ED%.2f' % asp)
                    self.cnv.create_text(
                        cw*(self._ix + 0.5), ch*(self._iy - self._sy + 0.5), text=txt,
                        font=ft, fill=col, anchor=tk.CENTER, tag=('ED%.2f' % asp)
                    )
                    self.cont_render(8, 288)
                elif self._iy > 1 and 21 < self._ix < 27:
                    self.pre_cleaning()
                else:
                    self.ent_c_set()
        if event.num == 3:
            self.pre_cleaning()
            pm = tk.Menu(self.app, tearoff=0)
            if self._iy == 0:
                txt = '< %s >' % self.skw['pmTitle']
            else:
                txt = ut.pr_round(self.asp_src[self._iy-1], 2)
            pm.add_command(label=txt, state=tk.DISABLED)
            pm.add_separator()
            pm.add_command(label=self.tkw['new'], command=lambda: self.edit_asp.mb(None, event.x_root, event.y_root))
            if 0 < self._iy < self.asp_num + 1:
                pm.add_command(
                    label=self.tkw['edit'], command=lambda: self.edit_asp.mb(asp, event.x_root, event.y_root))
                pm.add_command(
                    label=self.tkw['delete'],
                    command=lambda: self.ask_ent.mb(asp, 'qwsDel', lambda: self.pm_cnv_del(asp))
                )
            pm.tk_popup(event.x_root, event.y_root)

    def pm_cnv_del(self, asp):
        self.del_asp(asp)
        self.apply_chg(2)

    def ent_c_set(self):
        self.flag = 0
        self.pre_cleaning()
        self.ent_c_var_set()
        self.wdg_set_pos(256)
        self.ent_c.focus_set()
        self.ent_c.icursor(0)
        self.ent_c.selection_range(0, tk.END)

        cw = self.dim['CellWid']
        ch = self.dim['CellHgt']
        mk = self.col['EntMrk']

        self.cnv.create_rectangle(
            cw*(self._ix - self._sx) + 2, 2, cw*(self._ix - self._sx + 1) - 2, ch - 2,
            fill=None, outline=mk, width=3, tag='entMark')
        self.cnv.create_rectangle(
            2, ch*(self._iy - self._sy) + 2, cw - 2, ch*(self._iy - self._sy + 1) - 2,
            fill=None, outline=mk, width=3, tag='entMark')

    def ent_c_var_set(self):
        asp = self.asp_src[self._iy-1]
        if 3 < self._ix < 21:
            ind = self.pl_src[self._ix-4]
            self.ent_c_var.set(self.orb_4pl[(asp, ind)])
        elif self._ix == 21:
            self.ent_c_var.set(self.orb_4cs[asp])
        elif 21 < self._ix < 27 and self._iy == 1:
            self.ent_c_var.set(self.orb_4mx[self._ix-22])
        elif self._ix == 27:
            self.ent_c_var.set(self.asp_pnt[asp])

    def ent_c_var_save(self):
        try:
            val = float(self.ent_c_var.get())
            if val < 0 or val > 10:
                val = None
        except ValueError:
            val = None

        txt, tag = '', ''
        asp = self.asp_src[self._iy-1]

        if 3 < self._ix < 21:
            ind = self.pl_src[self._ix-4]
            if val is not None:
                self.set_asp_orb(asp, ind, val)
            tag = 'a%.2f%d' % (asp, ind)
            txt = ut.pr_round(self.orb_4pl[(asp, ind)], 4)
        elif self._ix == 21:
            if val is not None:
                self.set_asp_orb(asp, val=val)
            tag = 'h%.2f' % asp
            txt = ut.pr_round(self.orb_4cs[asp], 4)
        elif 21 < self._ix < 27:
            if val is not None:
                self.set_asp_orb(ind=(self._ix - 22), val=val)
            tag = 'm%d' % (self._ix - 22)
            txt = ut.pr_round(self.orb_4mx[self._ix-22], 4)
        elif self._ix == 27:
            if val is not None:
                self.set_asp_pnt(asp, val)
            tag = 'p%.2f' % asp
            txt = ut.pr_round(self.asp_pnt[asp], 2)

        return txt, tag

    def apply_chg(self, mode=0):
        if mode == 0:
            self._sx, self._sy = 0, 0
            self._nc, self._nr = 0, 0
            self.set_app_title()
        elif mode == 2:
            if self._sy and self._sy == self._nr:
                self._sy -= 1
        self.asp_num = len(self.asp_src)
        self.wdg_set_pos(2)
        self.tab_render()
        self.cont_render(4, 936)
        self.cnv_scr_upd()

    def on_click_tree(self, event):
        itm = self.tree.identify('item', event.x, event.y)
        row = self.tree.item(itm, 'text')
        tag = self.tree.item(itm, 'tag')

        self.pre_cleaning()

        if event.num == 1:
            if tag and tag[0] == 'smList':
                if row == self.skw['bltSm']:
                    self.set_asp_enb(mode=1)
                else:
                    self.use_sam(self.sample[row])
                self.tab_render()
                self.cont_render(8, 288)
            elif tag and tag[0] == 'pgList':
                flag = 0
                if row == self.skw['bltPg'] and self.get_pg_tit() != '':
                    flag = 1
                    row = ''
                elif row != self.skw['bltPg'] and self.get_pg_tit() != row:
                    flag = 1
                if flag:
                    self.dump_apg()
                    self.load_apg(row)
                    self.apply_chg()
        elif event.num == 3:
            pm = tk.Menu(self.app, tearoff=0)
            pm.add_command(label='< %s >' % row, state=tk.DISABLED)
            pm.add_separator()
            state = tk.DISABLED
            if tag and tag[0] == 'pgTitle':
                pm.add_command(
                    label=self.tkw['new'],
                    command=lambda: self.ask_ent.mb(self.tkw['new'], '', self.pm_apg_new, self.pg_valid)
                )
                pm.tk_popup(event.x_root, event.y_root)
            elif tag and tag[0] == 'pgList':
                if row == self.skw['bltPg']:
                    if self.get_st_flag():
                        pm.add_command(label=self.skw['pmStatOff'], command=lambda: self.pm_apg_apply_stat())
                    else:
                        pm.add_command(label=self.skw['pmStatOn'], command=lambda: self.pm_apg_apply_stat())
                    if self.get_pg_tit() == '':
                        state = tk.NORMAL
                    pm.add_command(label=self.tkw['apply'], state=state, command=lambda: self.cont_render(4, 936))
                    pm.add_command(
                        label=self.tkw['saveAs'], state=state,
                        command=lambda: self.ask_ent.mb(row, '', self.pm_apg_save_as, self.pg_valid)
                    )
                    pm.tk_popup(event.x_root, event.y_root)
                else:
                    if self.get_pg_tit() == self.tree.item(itm, 'text'):
                        state = tk.NORMAL
                    pm.add_command(label=self.tkw['apply'], state=state, command=lambda: self.cont_render(4, 936))
                    pm.add_command(
                        label=self.tkw['rename'],
                        command=lambda: self.ask_ent.mb(
                            self.tkw['rename'], row, self.pm_apg_rename(itm), self.pg_valid)
                    )
                    pm.add_command(
                        label=self.tkw['saveAs'], state=state,
                        command=lambda: self.ask_ent.mb(row, '', self.pm_apg_save_as, self.pg_valid)
                    )
                    pm.add_command(
                        label=self.tkw['delete'],
                        command=lambda: self.ask_ent.mb(row, 'qwsDel', lambda: self.pm_apg_del(itm))
                    )
                    pm.tk_popup(event.x_root, event.y_root)
            elif tag and tag[0] == 'smTitle':
                acc_menu = tk.Menu(self.app, tearoff=0)
                acc_menu.add_radiobutton(
                    label=self.skw['pmAccAll'], value=2, variable=self.acc_var, command=self.pm_sam_acc_change)
                acc_menu.add_radiobutton(
                    label=self.skw['pmAccN'], value=0, variable=self.acc_var, command=self.pm_sam_acc_change)
                acc_menu.add_radiobutton(
                    label=self.skw['pmAcc+'], value=1, variable=self.acc_var, command=self.pm_sam_acc_change)
                acc_menu.add_radiobutton(
                    label=self.skw['pmAcc-'], value=-1, variable=self.acc_var, command=self.pm_sam_acc_change)
                pm.add_command(
                    label=self.tkw['saveAs'],
                    command=lambda: self.ask_ent.mb(self.tkw['saveAs'], '', self.pm_sam_save_as, self.sam_valid)
                )
                pm.add_cascade(label=self.skw['pmAccTit'], menu=acc_menu)
                pm.tk_popup(event.x_root, event.y_root)
            elif tag and tag[0] == 'smList' and row != self.skw['bltSm']:
                pm.add_command(
                    label=self.tkw['rename'],
                    command=lambda: self.ask_ent.mb(self.tkw['rename'], row, self.pm_sam_rename(itm), self.sam_valid)
                )
                pm.add_command(
                    label=self.tkw['delete'],
                    command=lambda: self.ask_ent.mb(row, 'qwsDel', lambda: self.pm_sam_del(itm))
                )
                pm.tk_popup(event.x_root, event.y_root)

    def pm_apg_apply_stat(self):
        self.swi_st_flag()
        if self.get_pg_tit() == '':
            self.apply_stat()
            self.tab_render()
            self.cont_render(4, 936)

    def pm_apg_save_as(self, name):
        buf = self.get_pg_tit()
        self.set_pg_tit(name)
        self.dump_apg()
        self.set_pg_tit(buf)
        self.tree_reload()

    def pm_apg_new(self, name):
        try:
            shutil.copy2('%s/Template.txt' % self.pth[3], '%s/%s.json' % (self.pth[3], name))
        except FileNotFoundError as error:
            ut.error_log(error)
            cont = '["Aspect source",\n"[]",\n"Aspect enable",\n"[]",\n'\
                   '"Orbs table",\n{},\n"For cuspids",\n"[]",\n"For stars",\n"[]",\n"Aspect point",\n"[]",\n'\
                   '"Symbol",\n"[[-1, \\"\\u00f8\\"]]",\n"Color",\n"[[-1, \\"#008000\\"]]",\n'\
                   '"Font type",\n"[[-1, 1]]",\n"Dash",\n"[[-1, null]]"]'
            with open('%s/%s.json' % (self.pth[3], name), 'w') as fp:
                fp.write(cont)
                fp.close()
            shutil.copy2('%s/%s.json' % (self.pth[3], name), '%s/Template.txt' % self.pth[3])
        self.tree_reload()

    def pm_apg_del(self, item):
        name = self.tree.item(item, 'text')
        os.remove('%s/%s.json' % (self.pth[3], name))
        self.pg_name.discard(name)
        self.tree.delete(item)
        if name == self.get_pg_tit():
            self.load_apg()
            self.apply_chg()

    def pm_apg_rename(self, item):
        def rename(new_name):
            old_name = self.tree.item(item, 'text')
            os.rename('%s/%s.json' % (self.pth[3], old_name), '%s/%s.json' % (self.pth[3], new_name))
            self.tree_reload()
            if self.get_pg_tit() == old_name:
                self.set_pg_tit(new_name)
                self.set_app_title()
        return rename

    def pm_sam_rename(self, item):
        def rename(new_name):
            old_name = self.tree.item(item, 'text')
            self.sample[new_name] = self.sample[old_name]
            del self.sample[old_name]
            self.tree_reload()
        return rename

    def pm_sam_save_as(self, name):
        self.sample[name] = self.asp_enb.copy()
        self.tree_reload()

    def pm_sam_acc_change(self):
        self.set_act_var(4, self.acc_var.get())
        self.cont_render(8, 288)

    def pm_sam_del(self, item):
        name = self.tree.item(item, 'text')
        del self.sample[name]
        self.tree.delete(item)


class ModalBoxEditAsp:
    _w, _h = 0, 0
    flag = 0
    cv_w, cv_h = 0, 0
    val_var_r, sym_var_r = None, None
    col_var_r, dsh_var_r = None, None
    mode, mode_r = 0, 0
    app = None
    parent = None
    col_bt, dsh_cnv = None, None
    fnt_bt, sav_bt = None, None
    val_en, sym_en = None, None

    def __init__(self, apg, apply_func, font, kwd, col_seq):
        self.asp_src = apg.get_asp_src()

        self.get_asp_prop = apg.get_asp_prop
        self.upd_asp = apg.upd_asp
        self.del_asp = apg.del_asp

        self.val_var = tk.StringVar()
        self.sym_var = tk.StringVar()
        self.col_var = tk.StringVar()
        self.dsh_var = tk.IntVar()

        self.apply_func = apply_func

        self.sym_valid = ut.factory_valid(4, max_len=4)
        self.ind_valid = ut.factory_valid(2, 0, 180, ext=self.asp_src, ext_mode=1)

        self.kwd = kwd
        self.fnt = font
        self.col_ind = {0: col_seq}
        self.dsh_ind = {0: {1: None, 2: 5, 3: 1, 4: (5, 1, 1)}}
        self.dsh_ind[1] = {self.dsh_ind[0][i]: i for i in self.dsh_ind[0]}

    def mb(self, val=None, cx=None, cy=None):
        self.flag = 1
        self.create_app()

        self.col_ind[1] = {self.col_ind[0][i]: i for i in self.col_ind[0]}
        self._w = self.app.winfo_screenwidth()
        self._h = self.app.winfo_screenheight()

        if val is None:
            self.mode = 0
            val = -1
        else:
            self.mode = 1
        if self.get_asp_prop(val, 3):
            self.mode |= 2

        if self.mode & 1:
            title = self.kwd['editAsp']
            state = {0: tk.DISABLED, 1: tk.NORMAL}
        else:
            title = self.kwd['newAsp']
            state = {0: tk.NORMAL, 1: tk.DISABLED}

        if cx is None:
            cx = 0.5*self._w - 200
        if cy is None:
            cy = 0.5*self._h - 100

        self.app.geometry('+%d+%d' % (cx, cy))
        self.app.resizable(width=False, height=False)
        self.app.title(title)

        fnt = {0: self.fnt['AppBsc'], 1: [self.fnt['AppBsc'][0], int(0.75*self.fnt['AppBsc'][1])]}

        ttk.Style().configure('ase.TButton', font=fnt[0])
        self.app.option_add('*TCombobox*Listbox.font', fnt[0])

        res_bt = ttk.Button(self.app, style='ase.TButton', width=2, text='R', command=self.reset_form)
        val_lb = tk.Label(self.app, font=fnt[0], text=self.kwd['val'])
        self.val_en = ttk.Entry(
            self.app, font=fnt[0], width=6, state=state[0], textvariable=self.val_var, justify=tk.CENTER)
        self.col_bt = tk.Button(
            self.app, width=5, text='       ▼', font=fnt[1], bg=self.get_asp_prop(val, 2), command=self.add_color)
        col_cb = ttk.Combobox(
            self.app, values=list(self.col_ind[0].keys()), textvariable=self.col_var,
            font=fnt[0], width=8, state='readonly', justify=tk.CENTER)

        self.fnt_bt = ttk.Button(self.app, style='ase.TButton', width=2, command=self.chg_font)
        sym_lb = tk.Label(self.app, font=fnt[0], text=self.kwd['sym'])
        self.sym_en = ttk.Entry(self.app, font=fnt[0], width=6, textvariable=self.sym_var, justify=tk.CENTER)
        dsh_cb = ttk.Combobox(
            self.app, values=[1, 2, 3, 4], textvariable=self.dsh_var,
            font=fnt[0], width=3, state='readonly', justify=tk.CENTER)
        self.dsh_cnv = tk.Canvas(self.app, bg='#FFFFFF', bd=2, relief=tk.GROOVE)

        self.sav_bt = ttk.Button(self.app, style='ase.TButton', width=9, text=self.kwd['save'], command=self.transmit)
        del_bt = ttk.Button(
            self.app, style='ase.TButton', width=9, state=state[1], text=self.kwd['delete'], command=self.delete)
        clo_bt = ttk.Button(
            self.app, style='ase.TButton', width=9, text=self.kwd['close'], command=lambda: self.app.destroy())

        px, py = 10, 10
        res_bt.grid(row=0, column=0, padx=px, pady=py)
        val_lb.grid(row=0, column=1, sticky=tk.E)
        self.val_en.grid(row=0, column=2, padx=px, pady=py, sticky=tk.E+tk.W)
        self.col_bt.grid(row=0, column=3, sticky=tk.E+tk.W)
        col_cb.grid(row=0, column=4, padx=px, pady=py)

        self.fnt_bt.grid(row=1, column=0, padx=px, pady=py)
        sym_lb.grid(row=1, column=1, sticky=tk.E)
        self.sym_en.grid(row=1, column=2, padx=px, pady=py)
        dsh_cb.grid(row=1, column=3, sticky=tk.E+tk.W)
        self.dsh_cnv.grid(row=1, column=4, padx=px, pady=py)

        self.sav_bt.grid(row=2, column=0, columnspan=2, padx=px, pady=py)
        del_bt.grid(row=2, column=2, columnspan=2, padx=px, pady=py)
        clo_bt.grid(row=2, column=4, padx=px, pady=py, sticky=tk.E)

        self.val_var.trace_add('write', lambda *args: self.validate())
        self.sym_var.trace_add('write', lambda *args: self.validate())

        key = self.get_asp_prop(val, 2)
        col = self.col_ind[1][key] if key in self.col_ind[1] else key

        if self.mode & 1:
            self.val_var.set(val)
            self.sym_en.focus_set()
        else:
            self.val_var.set('')
            self.val_en.focus_set()
        self.chg_font()
        self.sym_var.set(self.get_asp_prop(val, 1))
        self.col_var.set(col)
        self.dsh_var.set(self.dsh_ind[1][self.get_asp_prop(val, 4)])

        self.val_var_r = self.val_var.get()
        self.sym_var_r = self.sym_var.get()
        self.col_var_r = self.col_var.get()
        self.dsh_var_r = self.dsh_var.get()
        self.mode_r = self.mode ^ 2

        self.app.bind('<Configure>', self.on_config)
        self.app.bind('<Escape>', lambda *args: self.app.destroy())
        self.app.bind('<Return>', lambda *args: self.on_return())
        col_cb.bind('<Configure>', self.dsh_cnv_cfg)
        col_cb.bind('<<ComboboxSelected>>', lambda *args: self.chg_col_dash())
        dsh_cb.bind('<<ComboboxSelected>>', lambda *args: self.chg_col_dash())

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
                y = self._h - event.height - 75 if event.y + event.height > self._h - 75 else event.y
                self.app.geometry('+%d+%d' % (x, y))
                self.flag = 0

    def dsh_cnv_cfg(self, event):
        self.cv_w, self.cv_h = event.width - 3, event.height - 3
        self.dsh_cnv.configure(width=self.cv_w, height=self.cv_h)
        self.chg_col_dash()

    def on_return(self):
        if str(self.sav_bt.cget('state')) == tk.NORMAL:
            self.transmit()

    def chg_col_dash(self):
        key = self.col_var.get()
        col = self.col_ind[0][key] if key in self.col_ind[0] else key
        dsh = self.dsh_ind[0][self.dsh_var.get()]
        y = 0.5 * self.cv_h

        self.col_bt.configure(bg=col)
        self.dsh_cnv.delete('all')
        for i in range(5):
            self.dsh_cnv.create_line(7, y + i, self.cv_w, y + i, fill=col, dash=dsh)

    def chg_font(self):
        if self.mode & 2:
            font = self.fnt['AppSym']
            txt = 'S'
        else:
            font = self.fnt['AppBsc']
            txt = 'T'
        self.mode = self.mode ^ 2
        self.sym_en.configure(font=font)
        self.fnt_bt.configure(text=txt)
        self.sym_en.focus_set()

    def add_color(self):
        key = self.col_var.get()
        ini = self.col_ind[0][key] if key in self.col_ind[0] else key
        col = askcolor(parent=self.app, initialcolor=ini)[1]
        if col:
            self.col_var.set(str(col).upper())
            self.chg_col_dash()

    def reset_form(self):
        self.val_var.set(self.val_var_r)
        self.sym_var.set(self.sym_var_r)
        self.col_var.set(self.col_var_r)
        self.dsh_var.set(self.dsh_var_r)
        self.mode = self.mode_r
        self.chg_col_dash()
        self.chg_font()
        self.sym_en.focus_set() if self.mode & 1 else self.val_en.focus_set()

    def transmit(self):
        val = float(self.val_var.get())
        ftp = 0 if self.mode & 2 else 1
        key = self.col_var.get()
        col = self.col_ind[0][key] if key in self.col_ind[0] else key

        self.upd_asp(val, self.sym_var.get(), ftp, col, self.dsh_ind[0][self.dsh_var.get()])
        self.apply_func(1)
        self.app.destroy()

    def delete(self):
        self.del_asp(float(self.val_var.get()))
        self.apply_func(2)
        self.app.destroy()

    def validate(self):
        if not self.mode & 1:
            if not self.ind_valid(self.val_var.get()):
                self.sav_bt.configure(state=tk.DISABLED)
                return False

        if not self.sym_valid(self.sym_var.get()):
            self.sav_bt.configure(state=tk.DISABLED)
            return False

        self.sav_bt.configure(state=tk.NORMAL)
        return True

# -------------------------------------------------------------------------------------------------------------------- #
