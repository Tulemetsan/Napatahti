# -------------------------------------------------------------------------------------------------------------------- #

import os
import tkinter as tk
import tkinter.filedialog as fd
import core.utilities as ut
from .sa_data_mng import DataMng
from .conf_gui import ConfigGui
from .src_class import ModalBoxAskEntry
from .apg_gui import AspPageGui
from .atb_gui import AspTabGui
from .pcat_gui import PlanCatGui
from .dbs_gui import DataBaseGui, ModalBoxDbaseEdit
from.tmc_gui import TimeCountGui

# @formatter:off


class SubMenu(DataMng):
    txt_type = [('Plain text TXT', '*.txt'), ('All Files', '*.*')]
    _rs = {}
    scw, sch = 0, 0

    def __init__(self):
        DataMng.__init__(self)

        self.ask_ent = ModalBoxAskEntry(self.font, self.loc.get_sample_tkw())
        self.tool_gui[1] = ModalBoxDbaseEdit(self.dbs, self.conf, self.loc, self.cont_render)
        self.tool_gui[2] = DataBaseGui(self.dbs, self.conf, self.loc, self.ask_ent, self.tool_gui[1], self.cont_render)
        self.tool_gui[3] = AspPageGui(self.apg, self.conf, self.loc, self.ask_ent, self.cont_render)
        self.tool_gui[4] = PlanCatGui(self.abo, self.conf, self.loc, self.ask_ent, self.cont_render)
        self.tool_gui[5] = AspTabGui(self.atb, self.apg, self.abo, self.conf, self.loc, self.data, self.cont_render)
        self.tool_gui[6] = TimeCountGui(self.abo, self.conf, self.loc.get_sample_tmc(), self.cont_render)
        self.tool_gui[7] = ConfigGui(self.conf, self.loc, self.cont_render)

        self.cel_enb_var = {
            1: tk.BooleanVar(), 2: tk.BooleanVar(), 4: tk.BooleanVar(), 8: tk.BooleanVar(),
            16: tk.BooleanVar(), 32: tk.BooleanVar(), 64: tk.BooleanVar(), 128: tk.BooleanVar(),
            256: tk.BooleanVar(), 512: tk.BooleanVar(), 1024: tk.BooleanVar(), 2048: tk.BooleanVar()
        }
        self.map_enb_var = {
            1: tk.IntVar(), 2: tk.BooleanVar(), 4: tk.BooleanVar(), 8: tk.BooleanVar(), 16: tk.BooleanVar()
        }
        self.esd_enb_var = {1: tk.BooleanVar(), 2: tk.BooleanVar(), 4: tk.BooleanVar(), 8: tk.BooleanVar()}
        self.acf_enb_var = {1: tk.BooleanVar(), 2: tk.BooleanVar(), 4: tk.BooleanVar()}
        self.cor_enb_var = {1: tk.BooleanVar(), 2: tk.BooleanVar()}

        self.fxs_calc_var = tk.IntVar()
        self.stb_calc_var = tk.IntVar()
        self.stat_det_var = {15: tk.IntVar(), 20: tk.IntVar(), 21: tk.IntVar()}
        self.core_mth_var = tk.IntVar()
        self.moon_mth_var = tk.IntVar()

        self.cfg_var = tk.StringVar()
        self.loc_var = tk.StringVar()

        for i in self.cel_enb_var:
            self.cel_enb_var[i].set(self.var[9] & i)
            if i < 17:
                self.map_enb_var[i].set(self.var[5] & i)
            if i < 9:
                self.esd_enb_var[i].set(self.var[17] & i)
            if i < 5:
                self.acf_enb_var[i].set(self.var[8] & i)
            if i < 3:
                self.cor_enb_var[i].set(self.var[14] & i)

        for i in self.stat_det_var:
            self.stat_det_var[i].set(self.var[i])

        self.stb_calc_var.set(self.var[16])
        self.core_mth_var.set(self.var[11] & 2)
        self.moon_mth_var.set(self.var[19])
        self.fxs_calc_var.set(self.var[22])
        self.cfg_var.set(self.conf.get_cur_cfg())
        self.loc_var.set(self.var[25])

        self.file_menu = tk.Menu(tearoff=0)
        self.file_menu.add_command(label=self.tkw['saveAs'], command=lambda: self.save_img_task(1))
        self.file_menu.add_command(label=self.mkw['quit'], command=self.app.destroy)

        self.view_menu = tk.Menu(tearoff=0)
        self.view_menu.add_checkbutton(
            label=self.mkw['tBar'], onvalue=True, offvalue=False, variable=self.cel_enb_var[64],
            command=lambda: self.swi_app_enb_var(9, 64))
        self.view_menu.add_separator()
        self.view_menu.add_checkbutton(
            label=self.mkw['dtcTit'], onvalue=True, offvalue=False, variable=self.cel_enb_var[2],
            command=lambda: self.swi_app_enb_var(9, 2))
        self.view_menu.add_checkbutton(
            label=self.mkw['edtTit'], onvalue=True, offvalue=False, variable=self.cel_enb_var[4],
            command=lambda: self.swi_app_enb_var(9, 4))
        self.view_menu.add_checkbutton(
            label=self.mkw['recTit'], onvalue=True, offvalue=False, variable=self.cel_enb_var[2048],
            command=lambda: self.swi_app_enb_var(9, 2048))
        self.view_menu.add_checkbutton(
            label=self.mkw['esdTit'], onvalue=True, offvalue=False, variable=self.cel_enb_var[1024],
            command=lambda: self.swi_app_enb_var(9, 1024))
        self.view_menu.add_checkbutton(
            label=self.mkw['mapTit'], onvalue=True, offvalue=False, variable=self.cel_enb_var[1],
            command=lambda: self.swi_app_enb_var(9, 1))
        self.view_menu.add_checkbutton(
            label=self.mkw['crdTit'], onvalue=True, offvalue=False, variable=self.cel_enb_var[16],
            command=lambda: self.swi_app_enb_var(9, 16))
        self.view_menu.add_checkbutton(
            label=self.mkw['stbTit'], onvalue=True, offvalue=False, variable=self.cel_enb_var[32],
            command=lambda: self.swi_app_enb_var(9, 32))
        self.view_menu.add_checkbutton(
            label=self.mkw['acfTit'], onvalue=True, offvalue=False, variable=self.cel_enb_var[256],
            command=lambda: self.swi_app_enb_var(9, 256))
        self.view_menu.add_checkbutton(
            label=self.mkw['astTit'], onvalue=True, offvalue=False, variable=self.cel_enb_var[512],
            command=lambda: self.swi_app_enb_var(9, 512))
        self.view_menu.add_checkbutton(
            label=self.mkw['corTit'], onvalue=True, offvalue=False, variable=self.cel_enb_var[8],
            command=lambda: self.swi_app_enb_var(9, 8))
        self.view_menu.add_separator()
        self.view_menu.add_checkbutton(
            label=self.mkw['fBar'], onvalue=True, offvalue=False, variable=self.cel_enb_var[128],
            command=lambda: self.swi_app_enb_var(9, 128))
        self.view_menu.add_separator()
        self.view_menu.add_command(label=self.mkw['repMap'], command=self.repos_map)
        self.view_menu.add_command(
            label=self.tkw['save'],
            command=lambda: self.ask_ent.mb(
                self.tkw['save'], 'qwsRep', lambda: self.conf.save_repos(self.mf_w, self.mf_h)))

        self.opt_menu = tk.Menu(tearoff=0)
        self.opt_menu.add_cascade(label=self.mkw['edtTit'], menu=self.get_pop_menu(2, 0))
        self.opt_menu.add_cascade(label=self.mkw['esdTit'], menu=self.get_pop_menu(4, 0))
        self.opt_menu.add_cascade(label=self.mkw['mapTit'], menu=self.get_pop_menu(5, 0))
        self.opt_menu.add_cascade(label=self.mkw['crdTit'], menu=self.get_pop_menu(6, 0))
        self.opt_menu.add_cascade(label=self.mkw['stbTit'], menu=self.get_pop_menu(7, 0))
        self.opt_menu.add_cascade(label=self.mkw['acfTit'], menu=self.get_pop_menu(8, 0))
        self.opt_menu.add_cascade(label=self.mkw['corTit'], menu=self.get_pop_menu(10, 0))

        self.tool_menu = tk.Menu(tearoff=0)
        self.tool_menu.add_command(label=self.mkw['dbs'], command=lambda: self.tool_gui_trig(2))
        self.tool_menu.add_command(label=self.mkw['apg'], command=lambda: self.tool_gui_trig(3))
        self.tool_menu.add_command(label=self.mkw['cat'], command=lambda: self.tool_gui_trig(4))
        self.tool_menu.add_command(label=self.mkw['atb'], command=lambda: self.tool_gui_trig(5))
        self.tool_menu.add_command(label=self.mkw['tmc'], command=lambda: self.tool_gui_trig(6))

        self.cfg_menu = tk.Menu(tearoff=0)
        self.cfg_menu.add_command(label=self.tkw['saveAs'], command=self.save_cfg_comm)
        self.cfg_menu.add_separator()
        for i in [i.split('.')[0] for i in filter(lambda x: x.endswith('.json'), os.listdir('Config'))]:
            self.cfg_menu.add_radiobutton(label=i, value=i, variable=self.cfg_var, command=self.sel_cfg_file)

        self.loc_menu = tk.Menu(tearoff=0)
        for i in [i.split('.')[0] for i in filter(lambda x: x.endswith('.json'), os.listdir('Local'))]:
            self.loc_menu.add_radiobutton(label=i, value=i, variable=self.loc_var, command=self.sel_loc_file)

        self.set_menu = tk.Menu(tearoff=0)
        self.set_menu.add_cascade(label=self.tkw['conf'], menu=self.cfg_menu)
        self.set_menu.add_cascade(label=self.tkw['lang'], menu=self.loc_menu)
        self.set_menu.add_command(label=self.tkw['set'], command=lambda: self.tool_gui_trig(7, 11))

        self.cell[1].bind('<Button-3>', lambda event: self.cb_pop_menu(5, event))
        self.cell[2].bind('<Button-3>', lambda event: self.cb_pop_menu(1, event))
        self.cell[4].bind('<Button-3>', lambda event: self.cb_pop_menu(2, event))
        self.cell[8].bind('<Button-3>', lambda event: self.cb_pop_menu(10, event))
        self.cell[16].bind('<Button-3>', lambda event: self.cb_pop_menu(6, event))
        self.cell[32].bind('<Button-3>', lambda event: self.cb_pop_menu(7, event))
        self.cell[256].bind('<Button-3>', lambda event: self.cb_pop_menu(8, event))
        self.cell[512].bind('<Button-3>', lambda event: self.cb_pop_menu(9, event))
        self.cell[1024].bind('<Button-3>', lambda event: self.cb_pop_menu(4, event))
        self.cell[2048].bind('<Button-3>', lambda event: self.cb_pop_menu(3, event))

    def cb_pop_menu(self, ind, event):
        pm = self.get_pop_menu(ind, 1)
        pm.tk_popup(event.x_root, event.y_root)

    def get_pop_menu(self, ind, mode=0):
        menu = tk.Menu(tearoff=0)

        if ind == 1 and mode:
            menu.add_command(label=self.mkw['dtcTit'], state=tk.DISABLED)
        elif ind == 2:
            if mode:
                menu.add_command(label=self.mkw['edtTit'], state=tk.DISABLED)
                menu.add_separator()
            menu.add_radiobutton(
                label=self.mkw['mdWest'], value=0, variable=self.moon_mth_var, command=self.swi_moon_day_mth)
            menu.add_radiobutton(
                label=self.mkw['mdJyot'], value=1, variable=self.moon_mth_var, command=self.swi_moon_day_mth)
        elif ind == 3 and mode:
            menu.add_command(label=self.mkw['recTit'], state=tk.DISABLED)
        elif ind == 4:
            if mode:
                menu.add_command(label=self.mkw['esdTit'], state=tk.DISABLED)
                menu.add_separator()
            menu.add_checkbutton(
                label=self.mkw['sunTit'], onvalue=True, offvalue=False, variable=self.esd_enb_var[8],
                command=lambda: self.swi_app_enb_var(17, 8))
            menu.add_checkbutton(
                label=self.mkw['essTit'], onvalue=True, offvalue=False, variable=self.esd_enb_var[1],
                command=lambda: self.swi_app_enb_var(17, 1))
            menu.add_checkbutton(
                label=self.mkw['r&pTit'], onvalue=True, offvalue=False, variable=self.esd_enb_var[2],
                command=lambda: self.swi_app_enb_var(17, 2))
            menu.add_checkbutton(
                label=self.mkw['d&aTit'], onvalue=True, offvalue=False, variable=self.esd_enb_var[4],
                command=lambda: self.swi_app_enb_var(17, 4))
        elif ind == 5:
            if mode:
                menu.add_command(label=self.mkw['mapTit'], state=tk.DISABLED)
                menu.add_separator()
            menu.add_radiobutton(
                label=self.mkw['zpAri'], value=0, variable=self.map_enb_var[1],
                command=lambda: self.swi_app_enb_var(5, 1))
            menu.add_radiobutton(
                label=self.mkw['zpAsc'], value=1, variable=self.map_enb_var[1],
                command=lambda: self.swi_app_enb_var(5, 1))
            menu.add_checkbutton(
                label=self.mkw['cspEnb'], onvalue=True, offvalue=False, variable=self.map_enb_var[8],
                command=lambda: self.swi_app_enb_var(5, 8))
            menu.add_separator()
            menu.add_checkbutton(
                label=self.mkw['degEnb'], onvalue=True, offvalue=False, variable=self.map_enb_var[2],
                command=lambda: self.swi_app_enb_var(5, 2))
            menu.add_checkbutton(
                label=self.mkw['spdEnb'], onvalue=True, offvalue=False, variable=self.map_enb_var[4],
                command=lambda: self.swi_app_enb_var(5, 4))
            menu.add_checkbutton(
                label=self.mkw['essCol'], onvalue=True, offvalue=False, variable=self.map_enb_var[16],
                command=lambda: self.swi_app_enb_var(5, 16))
        elif ind == 6:
            if mode:
                menu.add_command(label=self.mkw['crdTit'], state=tk.DISABLED)
                menu.add_separator()
            menu.add_checkbutton(
                label=self.mkw['fxs'], onvalue=1, offvalue=0, variable=self.fxs_calc_var, command=self.swi_fxs_calc_var)
        elif ind == 7:
            if mode:
                sm = tk.Menu(tearoff=0)
                sm.add_radiobutton(
                    label=self.mkw['priSt'], value=0, variable=self.stb_calc_var, command=self.swi_stb_calc_mth)
                sm.add_radiobutton(
                    label=self.mkw['csmSt'], value=1, variable=self.stb_calc_var, command=self.swi_stb_calc_mth)
                sm.add_radiobutton(
                    label=self.mkw['ashSt'], value=2, variable=self.stb_calc_var, command=self.swi_stb_calc_mth)

                menu.add_command(label=self.mkw['stbTit'], state=tk.DISABLED)
                menu.add_separator()
                menu.add_cascade(label=self.mkw['stbCalc'], menu=sm)
                if self.var[16] == 2:
                    menu.add_separator()
                    menu.add_radiobutton(
                        label=self.mkw['ashKn'], value=0, variable=self.stat_det_var[21],
                        command=lambda: self.swi_stb_stat_det(21))
                    menu.add_radiobutton(
                        label=self.mkw['ashCr'], value=2, variable=self.stat_det_var[21],
                        command=lambda: self.swi_stb_stat_det(21))
                    menu.add_radiobutton(
                        label=self.mkw['ashDet'], value=1, variable=self.stat_det_var[21],
                        command=lambda: self.swi_stb_stat_det(21))
                elif self.var[16] == 1:
                    menu.add_separator()
                    menu.add_radiobutton(
                        label=self.mkw['csmSum'], value=0, variable=self.stat_det_var[20],
                        command=lambda: self.swi_stb_stat_det(20))
                    menu.add_radiobutton(
                        label=self.mkw['csmDet'], value=1, variable=self.stat_det_var[20],
                        command=lambda: self.swi_stb_stat_det(20))
                else:
                    menu.add_separator()
                    menu.add_radiobutton(
                        label=self.mkw['stbBoth'], value=2, variable=self.stat_det_var[15],
                        command=lambda: self.swi_stb_stat_det(15))
                    menu.add_radiobutton(
                        label=self.mkw['stbCos'], value=0, variable=self.stat_det_var[15],
                        command=lambda: self.swi_stb_stat_det(15))
                    menu.add_radiobutton(
                        label=self.mkw['stbHor'], value=1, variable=self.stat_det_var[15],
                        command=lambda: self.swi_stb_stat_det(15))
            else:
                menu.add_radiobutton(
                    label=self.mkw['priSt'], value=0, variable=self.stb_calc_var, command=self.swi_stb_calc_mth)
                menu.add_radiobutton(
                    label=self.mkw['csmSt'], value=1, variable=self.stb_calc_var, command=self.swi_stb_calc_mth)
                menu.add_radiobutton(
                    label=self.mkw['ashSt'], value=2, variable=self.stb_calc_var, command=self.swi_stb_calc_mth)
            menu.add_separator()
            menu.add_command(label=self.mkw['inv'], command=self.stb_invert)
            menu.add_command(label=self.mkw['sync'], command=self.stb_sync)
        elif ind == 8:
            if mode:
                menu.add_command(label=self.mkw['acfTit'], state=tk.DISABLED)
                menu.add_separator()
            menu.add_checkbutton(
                label=self.mkw['acfCls'], onvalue=False, offvalue=True, variable=self.acf_enb_var[2],
                command=lambda: self.swi_app_enb_var(8, 2)
            )
            menu.add_checkbutton(
                label=self.mkw['acfBnd'], onvalue=True, offvalue=False, variable=self.acf_enb_var[4],
                command=lambda: self.swi_app_enb_var(8, 4)
            )
            menu.add_checkbutton(
                label=self.mkw['acfAst'], onvalue=True, offvalue=False, variable=self.acf_enb_var[1],
                command=lambda: self.swi_app_enb_var(8, 1))
        elif ind == 9 and mode:
            menu.add_command(label=self.mkw['astTit'], state=tk.DISABLED)
        elif ind == 10:
            if mode:
                menu.add_command(label=self.mkw['corTit'], state=tk.DISABLED)
                menu.add_separator()
            menu.add_checkbutton(
                label=self.mkw['stbCos'], onvalue=True, offvalue=False, variable=self.cor_enb_var[1],
                command=lambda: self.swi_app_enb_var(14, 1))
            menu.add_checkbutton(
                label=self.mkw['stbHor'], onvalue=True, offvalue=False, variable=self.cor_enb_var[2],
                command=lambda: self.swi_app_enb_var(14, 2))
            menu.add_separator()
            menu.add_radiobutton(
                label=self.mkw['stMethSch'], value=0, variable=self.core_mth_var, command=self.swi_core_calc_mth)
            menu.add_radiobutton(
                label=self.mkw['stMethGlo'], value=2, variable=self.core_mth_var, command=self.swi_core_calc_mth)
        if mode:
            menu.add_separator()
            if ind in {2, 7, 10}:
                state = tk.DISABLED if ind == 2 and not self.moon_c[self.var[19]] else tk.NORMAL
                menu.add_command(label=self.tkw['saveAs'], state=state, command=lambda: self.save_src_data(ind))
            menu.add_command(label=self.tkw['set'], command=lambda: self.tool_gui_trig(7, ind))

        return menu

    def sel_loc_file(self):
        lang = self.loc_var.get()
        if lang != self.var[25]:
            self.loc.reload(lang)
            self.conf.set_save_flag(1)
            self.cont_render(rend=2015)
            self.ask_ent.mb(self.tkw['lang'], 'qwsLoc', lambda: None)

    def sel_cfg_file(self):
        cfg = self.cfg_var.get()
        if cfg != self.conf.get_cur_cfg():
            self.conf.dump()
            self.conf.reload(cfg)
            self.cont_render(16, 8159)

    def save_cfg_comm(self):
        ext = [i.split('.')[0] for i in filter(lambda x: x.endswith('.json'), os.listdir('Config'))]
        self.ask_ent.mb(self.cfg_var.get(), '', self.save_cfg_func, ut.factory_valid(3, ext=ext))

    def save_cfg_func(self, cfg):
        self.conf.set_save_flag(1)
        self.conf.set_cfg_name(cfg)
        self.conf.dump()
        self.cfg_var.set(cfg)
        self.cfg_menu.add_radiobutton(label=cfg, value=cfg, variable=self.cfg_var, command=self.sel_cfg_file)

    def swi_app_enb_var(self, ind, bit):
        rend_func = {}

        if ind == 5:
            enb = self.map_enb_var[bit].get()
            rend_func[ind] = self.map_render
            if bit == 1 and enb != self.var[ind] & 1:
                self.zp = self.cs_crd[0] if enb else 0
        elif ind == 8:
            enb = self.acf_enb_var[bit].get()
            rend_func[ind] = lambda: self.cont_render(8, 256)
        elif ind == 9:
            enb = self.cel_enb_var[bit].get()
            rend_func[ind] = lambda: self.cell_set_pos(bit, enb)
        elif ind == 14:
            enb = self.cor_enb_var[bit].get()
            rend_func[ind] = lambda: self.cont_render(rend=1024)
        elif ind == 17:
            enb = self.esd_enb_var[bit].get()
            rend_func[ind] = self.ess_data_render
        else:
            return None

        if enb and not self.var[ind] & bit:
            self.conf.set_act_var(ind, self.var[ind] | bit)
            rend_func[ind]()
        elif not enb and self.var[ind] & bit:
            self.conf.set_act_var(ind, self.var[ind] ^ bit)
            rend_func[ind]()

    def swi_fxs_calc_var(self):
        self.conf.set_act_var(22, self.fxs_calc_var.get())
        self.crd_render()

    def swi_stb_stat_det(self, ind):
        self.conf.set_act_var(ind, self.stat_det_var[ind].get())
        self.stb_render()

    def swi_stb_calc_mth(self):
        self.conf.set_act_var(16, self.stb_calc_var.get())
        self.cont_render(rend=136)

    def swi_moon_day_mth(self):
        self.conf.set_act_var(19, self.moon_mth_var.get())
        self.edt_render()

    def swi_core_calc_mth(self):
        if self.var[11] != self.core_mth_var.get():
            self.conf.set_act_var(11, self.var[11] ^ 2)
            if self.apg.get_st_flag() and self.apg.get_pg_tit() == '':
                calc = 14
                rend = 1952
            else:
                calc = 6
                rend = 1152
            self.cont_render(calc, rend)

    def save_img_task(self, mode=0):
        self.app.attributes('-topmost', 1)
        self._rs[0] = 0
        self._rs[5] = 1 if mode else 0
        if self.app.state() == 'normal':
            if self._rs[1] + self._rs[3] > self.scw or self._rs[2] + self._rs[4] > self.sch:
                self.app.geometry('+-8+%d' % self.app_dim['PyFrmTop'])

    def tool_gui_trig(self, ind, mode=1):
        if ind in {1, 2}:
            k = 1 if ind == 2 else 2
            if k and self.child[k]:
                self.child[k].wm_state('normal')
                self.child[k].focus_set()
                return None

        if self.child[ind]:
            self.child[ind].wm_state('normal')
            self.child[ind].focus_set()
        else:
            if ind == 1:
                if mode:
                    cur = self.dbs.get_cur_ind(self.data)
                    self.data[0] = cur if cur else self.var[6]
                    self.tool_gui[ind].mb(self.data, 150, 150, 0)
                else:
                    self.tool_gui[ind].mb(self.dbs.get_record(), 150, 150, 0)
            elif ind == 7:
                self.tool_gui[ind].child_app(mode)
            else:
                self.tool_gui[ind].child_app()

    def save_src_data(self, mode=1):
        if mode == 2:
            mnc = self.moon_c[self.var[19]]
            fmn = self.moon_c[1][16]
            if self.var[19]:
                sys = self.mkw['mdJyot']
                crd = ''
            else:
                sys = self.mkw['mdWest']
                lat = self.data[1]['lat']
                lon = self.data[1]['lon']
                crd = ', %d%s%02d %d%s%02d' % (lat[0], lat[3].lower(), lat[1], lon[0], lon[3].lower(), lon[1])

            buf = '%s [ %s%s ]:\n\n' % (self.ckw['mdFull'], sys, crd)
            for i in range(1, len(mnc) - 1):
                beg = '%d %s %d %2d:%02d:%02d' % (
                    mnc[i][2], self.month[mnc[i][1]], mnc[i][0], mnc[i][3], mnc[i][4], mnc[i][5])
                if self.var[19]:
                    j = i + 1
                else:
                    j = i + 1 if i != 29 else 30 if 30 in mnc else 31
                end = '%d %s %d %2d:%02d:%02d' % (
                    mnc[j][2], self.month[mnc[j][1]], mnc[j][0], mnc[j][3], mnc[j][4], mnc[j][5])
                add = '*' if i == 1 else ' '
                buf += '%2d %30s %s %30s\n' % (i, beg, add, end)
            buf = buf[:-1]
            buf += ' *\n\n%s: %d %s %d %2d:%02d:%02d' % (
                self.ckw['fullMon'], fmn[2], self.month[fmn[1]], fmn[0], fmn[3], fmn[4], fmn[5])
        elif mode == 7:
            if self.var[16] == 2:
                buf = '%s' % self.ash
            elif self.var[16] == 1:
                buf = '%s' % self.cst
            else:
                buf = '%s\n\n%s\n\n' % (self.pr_cos.__str__(1), self.pr_hor.__str__(1))
                buf += 'Fiction planets status:\n\n'
                for i in [11, 23, 56, 12]:
                    add = '*' if self.fic_st[i][1] == 1 else ''
                    buf += '%10s %+3d %s\n' % (self.abo.get_pl_name(i), self.fic_pr[i], add)
                buf = buf[:-1]
        elif mode == 10:
            buf = '%s\n\n%s' % (self.pr_cos, self.pr_hor)
        else:
            return None

        file = fd.asksaveasfile(initialfile=self.data[1]['name'], filetypes=self.txt_type, defaultextension='*.txt')
        if file:
            file.write(buf)
            file.close()

# -------------------------------------------------------------------------------------------------------------------- #
